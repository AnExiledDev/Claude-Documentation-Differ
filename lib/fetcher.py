#!/usr/bin/env python3
"""Playwright-based documentation fetcher for Claude Code docs.

Fetches documentation from https://code.claude.com/docs/en/ using the
llms.txt index file to discover all available pages.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from playwright.async_api import async_playwright, Page, Browser

BASE_URL = "https://code.claude.com/docs"
INDEX_URL = f"{BASE_URL}/llms.txt"


@dataclass
class FetchResult:
    """Result of fetching a single page."""

    url: str
    filename: str
    content: str | None
    success: bool
    error: str | None = None


@dataclass
class FetchSummary:
    """Summary of a full fetch operation."""

    total_pages: int
    successful: int
    failed: int
    results: list[FetchResult]

    @property
    def all_successful(self) -> bool:
        return self.failed == 0


async def fetch_index(page: Page) -> list[str]:
    """Fetch and parse llms.txt to get all page URLs.

    Returns list of full URLs to .md files.
    """
    response = await page.goto(INDEX_URL)
    if not response or response.status != 200:
        raise RuntimeError(
            f"Failed to fetch index: HTTP {response.status if response else 'no response'}"
        )

    content = await page.content()

    # Extract URLs from the page content
    # The llms.txt contains URLs like https://code.claude.com/docs/en/overview.md
    urls = re.findall(r"https://code\.claude\.com/docs/en/[\w-]+\.md", content)

    if not urls:
        raise RuntimeError("No documentation URLs found in llms.txt")

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


async def fetch_page(page: Page, url: str, retries: int = 3) -> FetchResult:
    """Fetch a single markdown page.

    Args:
        page: Playwright page instance
        url: Full URL to the .md file
        retries: Number of retry attempts

    Returns:
        FetchResult with content or error
    """
    filename = url.split("/")[-1]

    for attempt in range(retries):
        try:
            response = await page.goto(url, wait_until="networkidle")

            if not response:
                continue

            if response.status == 404:
                return FetchResult(
                    url=url,
                    filename=filename,
                    content=None,
                    success=False,
                    error="Page not found (404)",
                )

            if response.status != 200:
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                return FetchResult(
                    url=url,
                    filename=filename,
                    content=None,
                    success=False,
                    error=f"HTTP {response.status}",
                )

            # Get the raw text content
            content = await page.inner_text("body")

            # Validate it looks like markdown
            if not content or len(content) < 100:
                if attempt < retries - 1:
                    await asyncio.sleep(1)
                    continue
                return FetchResult(
                    url=url,
                    filename=filename,
                    content=None,
                    success=False,
                    error="Content too short or empty",
                )

            return FetchResult(
                url=url,
                filename=filename,
                content=content.strip(),
                success=True,
            )

        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)
                continue
            return FetchResult(
                url=url,
                filename=filename,
                content=None,
                success=False,
                error=str(e),
            )

    return FetchResult(
        url=url,
        filename=filename,
        content=None,
        success=False,
        error="Max retries exceeded",
    )


async def fetch_all_pages(
    output_dir: Path,
    rate_limit: float = 1.0,
    progress_callback: Callable[[int, int, str], None] | None = None,
    dry_run: bool = False,
) -> FetchSummary:
    """Fetch all documentation pages.

    Args:
        output_dir: Directory to write .md files to
        rate_limit: Seconds to wait between requests
        progress_callback: Called with (current, total, filename) for progress
        dry_run: If True, fetch but don't write files

    Returns:
        FetchSummary with results
    """
    results: list[FetchResult] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Fetch the index
            if progress_callback:
                progress_callback(0, 0, "Fetching index...")

            urls = await fetch_index(page)
            total = len(urls)

            if progress_callback:
                progress_callback(0, total, f"Found {total} pages")

            # Fetch each page
            for i, url in enumerate(urls):
                filename = url.split("/")[-1]

                if progress_callback:
                    progress_callback(i + 1, total, filename)

                result = await fetch_page(page, url)
                results.append(result)

                # Write to file if successful and not dry run
                if result.success and result.content and not dry_run:
                    output_path = output_dir / filename
                    output_path.write_text(result.content)

                # Rate limiting
                if i < len(urls) - 1:
                    await asyncio.sleep(rate_limit)

        finally:
            await browser.close()

    successful = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    return FetchSummary(
        total_pages=len(results),
        successful=successful,
        failed=failed,
        results=results,
    )


async def fetch_single_page(url: str) -> FetchResult:
    """Fetch a single page (convenience function for testing)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            return await fetch_page(page, url)
        finally:
            await browser.close()
