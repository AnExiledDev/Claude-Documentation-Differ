# Claude API Documentation Changes — 2026-04-07

## Summary

The `max` effort level is now available on both Claude Opus 4.6 and Claude Sonnet 4.6, expanding what was previously an Opus-only feature. Response prefilling has been clarified as unsupported (returning a 400 error) on Opus 4.6 and Sonnet 4.6, with Claude Sonnet 4.5 removed from the restriction list and code examples updated accordingly. The `llms-full.txt` resource link was removed from the resources overview page.

## Significant Changes

### Models

- **`max` effort level expanded to Claude Sonnet 4.6**: The `max` effort and adaptive thinking level previously restricted to Opus 4.6 is now also available on Sonnet 4.6. The prior restriction that non-Opus requests would return an error has been removed.
  > `max` | Absolute maximum capability with no constraints on token spending. Available on Claude Opus 4.6 and Claude Sonnet 4.6.
  - *Implication*: Developers using Sonnet 4.6 can now set `effort: "max"` or use unconstrained adaptive thinking without receiving an error.
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md), [Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md)

- **`max` effort added to Sonnet 4.6 use-case guidance**: A new bullet was added to the Sonnet 4.6 effort recommendations section.
  > **Max effort:** For tasks requiring the absolute highest capability with no constraints on token spending.
  - *Implication*: Guidance now explicitly covers all four effort levels for Sonnet 4.6 deployments.
  - *Source*: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort.md)

### API

- **Prefilling clarified: hard error on Opus 4.6 and Sonnet 4.6, Sonnet 4.5 no longer restricted**: The warning around response prefilling has been sharpened. It now states that prefilling is "not supported" (returning a 400 error) specifically on Opus 4.6 and Sonnet 4.6. The previous wording called it "deprecated" and also listed Sonnet 4.5 as unsupported — both of those characterizations have been removed.
  > Prefilling is not supported on Claude Opus 4.6 and Claude Sonnet 4.6. Requests using prefill with these models return a 400 error. Use [structured outputs](/docs/en/build-with-claude/structured-outputs) or system prompt instructions instead. See the [migration guide](/docs/en/about-claude/models/migration-guide) for migration patterns.
  - *Implication*: Sonnet 4.5 is no longer called out as unsupported for prefilling. Code examples in the prefill section were updated from `claude-opus-4-6` to `claude-sonnet-4-5` across all SDK languages (Shell, Python, TypeScript, C#, Go, Java, PHP, Ruby), confirming Sonnet 4.5 is the recommended model for prefill use cases. Requests to Opus 4.6 or Sonnet 4.6 with prefill will now explicitly receive a 400 error rather than undocumented behavior.
  - *Source*: [Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages.md)

- **Guardrails docs updated to reflect prefill model scope change**: The increase-consistency and reduce-prompt-leak guardrail pages were updated in parallel with the prefill warning change, dropping the "deprecated" language and removing Sonnet 4.5 from the list of unsupported models.
  - *Source*: [Increase Consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency.md), [Reduce Prompt Leak](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md)

### Resources

- **`llms-full.txt` card removed from resources overview**: The card linking to `/llms-full.txt` ("Complete LLM-optimized documentation") was removed from the resources overview page. The `llms.txt` card remains.
  - *Implication*: Automated tooling or scripts that relied on `/llms-full.txt` for complete documentation ingestion should be updated.
  - *Source*: [Resources Overview](https://platform.claude.com/docs/en/resources/overview.md)

## New Pages

- **[en_api_terraform_beta_skills_list.md]** — Placeholder page indicating a temporary Claude Console service disruption for the Terraform beta skills list endpoint. Contains only a service-disruption notice. [View](https://platform.claude.com/docs/en/api/terraform/beta/skills/list.md)

## Migration Guidance

**Prefilling with Opus 4.6 and Sonnet 4.6 now returns a 400 error.** If you are sending requests with an `assistant` prefill turn to either of these models, they will fail. Migrate to [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) or enforce format via system prompt instructions. The documentation now links to a [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide) for common patterns. Sonnet 4.5 remains a supported option if you need to continue using prefilling.

## Notable Details

- The prefill code examples throughout the "Working with Messages" page were updated from `claude-opus-4-6` to `claude-sonnet-4-5` across all eight SDK language tabs (Shell, Python, TypeScript, C#, Go, Java, PHP, Ruby) and in the sample JSON response block. This makes Sonnet 4.5 the canonical example model for demonstrating prefill behavior.
- The `metadata.json` crawl count moved from 483 successful / 137 failed to 484 successful / 136 failed, indicating one previously-failing page is now being successfully fetched (the new Terraform skills list page).

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `build-with-claude/working-with-messages.md` | Modified | +10 / -10 | Prefill warning clarified (hard 400 error, Sonnet 4.5 no longer restricted); code examples updated from `claude-opus-4-6` to `claude-sonnet-4-5` across all SDK tabs |
| `build-with-claude/effort.md` | Modified | +3 / -2 | `max` effort extended to Sonnet 4.6; new guidance bullet added for max effort on Sonnet 4.6 |
| `build-with-claude/adaptive-thinking.md` | Modified | +1 / -1 | `max` thinking level extended to Sonnet 4.6 |
| `resources/overview.md` | Modified | +0 / -4 | Removed `llms-full.txt` card |
| `test-and-evaluate/strengthen-guardrails/increase-consistency.md` | Modified | +1 / -1 | Prefill note updated: removed "deprecated", removed Sonnet 4.5 from unsupported list |
| `test-and-evaluate/strengthen-guardrails/reduce-prompt-leak.md` | Modified | +1 / -1 | Prefill note updated: removed "deprecated", removed Sonnet 4.5 from unsupported list |
| `api/terraform/beta/skills/list.md` | New | +3 / -0 | Temporary service disruption placeholder for Terraform beta skills list |
