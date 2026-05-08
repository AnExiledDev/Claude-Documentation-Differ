#!/usr/bin/env python3
"""Playwright-based documentation fetcher.

Fetches documentation from various sources using their llms.txt index file
to discover all available pages.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page

# Minimum content length (bytes) to consider a fetched page valid
MIN_CONTENT_LENGTH = 100

# Default retry attempts per page fetch
DEFAULT_RETRIES = 3

# Playwright navigation timeout (ms)
PAGE_TIMEOUT_MS = 30_000

# Failure rate threshold — warn when exceeded
FAILURE_RATE_ALERT_THRESHOLD = 0.20


@dataclass
class FetchResult:
    """Result of fetching a single page."""

    url: str
    relative_path: (
        str  # Relative path under the docs directory (e.g., "en/overview.md")
    )
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


def extract_relative_path(url: str, base_url: str) -> str:
    """Extract relative path from URL.

    For https://code.claude.com/docs/en/overview.md with base https://code.claude.com/docs
    returns "en/overview.md"

    For https://platform.claude.com/docs/en/api/messages/create.md with base https://platform.claude.com
    returns "docs/en/api/messages/create.md" -> we want just "en/api/messages/create.md"

    We always want the path starting from "en/" for consistency.
    """
    # Parse the URL to get the path
    parsed = urlparse(url)
    path = parsed.path

    # Find the "en/" part and take everything from there
    en_match = re.search(r"(en/.*)", path)
    if en_match:
        return en_match.group(1)

    # Fallback: preserve path structure relative to base_url
    parsed_base = urlparse(base_url)
    base_path = parsed_base.path.rstrip("/")
    if path.startswith(base_path) and len(path) > len(base_path):
        return path[len(base_path) :].lstrip("/")

    # Last resort: full path without leading slash
    return path.lstrip("/")


async def fetch_index(page: Page, index_url: str, url_pattern: str) -> list[str]:
    """Fetch and parse llms.txt to get all page URLs.

    Args:
        page: Playwright page instance
        index_url: URL to the llms.txt index file
        url_pattern: Regex pattern to match page URLs

    Returns:
        List of full URLs to .md files
    """
    response = await page.goto(index_url, timeout=PAGE_TIMEOUT_MS)
    if not response or response.status != 200:
        raise RuntimeError(
            f"Failed to fetch index: HTTP {response.status if response else 'no response'}"
        )

    content = await page.content()

    # Extract URLs matching the pattern
    urls = re.findall(url_pattern, content)

    if not urls:
        raise RuntimeError(
            f"No documentation URLs found matching pattern: {url_pattern}"
        )

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


async def fetch_page(
    page: Page, url: str, base_url: str, retries: int = DEFAULT_RETRIES
) -> FetchResult:
    """Fetch a single markdown page.

    Args:
        page: Playwright page instance
        url: Full URL to the .md file
        base_url: Base URL for extracting relative paths
        retries: Number of retry attempts

    Returns:
        FetchResult with content or error
    """
    relative_path = extract_relative_path(url, base_url)

    for attempt in range(retries):
        try:
            response = await page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT_MS)

            if not response:
                continue

            if response.status == 404:
                return FetchResult(
                    url=url,
                    relative_path=relative_path,
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
                    relative_path=relative_path,
                    content=None,
                    success=False,
                    error=f"HTTP {response.status}",
                )

            # Get the raw text content
            content = await page.inner_text("body")

            # Validate it looks like markdown
            if not content or len(content) < MIN_CONTENT_LENGTH:
                if attempt < retries - 1:
                    await asyncio.sleep(1)
                    continue
                return FetchResult(
                    url=url,
                    relative_path=relative_path,
                    content=None,
                    success=False,
                    error="Content too short or empty",
                )

            return FetchResult(
                url=url,
                relative_path=relative_path,
                content=content.strip(),
                success=True,
            )

        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)
                continue
            return FetchResult(
                url=url,
                relative_path=relative_path,
                content=None,
                success=False,
                error=str(e),
            )

    return FetchResult(
        url=url,
        relative_path=relative_path,
        content=None,
        success=False,
        error="Max retries exceeded",
    )


async def fetch_all_pages(
    output_dir: Path,
    index_url: str,
    url_pattern: str,
    base_url: str,
    rate_limit: float = 1.0,
    progress_callback: Callable[[int, int, str], None] | None = None,
    dry_run: bool = False,
) -> FetchSummary:
    """Fetch all documentation pages.

    Args:
        output_dir: Directory to write .md files to (source-specific, e.g., docs/claude-code)
        index_url: URL to the llms.txt index file
        url_pattern: Regex pattern to match page URLs
        base_url: Base URL for the documentation site
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

            urls = await fetch_index(page, index_url, url_pattern)
            total = len(urls)

            if progress_callback:
                progress_callback(0, total, f"Found {total} pages")

            # Fetch each page
            for i, url in enumerate(urls):
                relative_path = extract_relative_path(url, base_url)
                display_name = relative_path.split("/")[-1]  # Just filename for display

                if progress_callback:
                    progress_callback(i + 1, total, display_name)

                result = await fetch_page(page, url, base_url)
                results.append(result)

                # Write to file if successful and not dry run
                if result.success and result.content and not dry_run:
                    output_path = output_dir / result.relative_path
                    # Create parent directories for nested paths (e.g., en/api/messages/)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
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


async def fetch_single_page(url: str, base_url: str) -> FetchResult:
    """Fetch a single page (convenience function for testing)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            return await fetch_page(page, url, base_url)
        finally:
            await browser.close()
