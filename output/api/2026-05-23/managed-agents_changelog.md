# Claude API Documentation Changes — 2026-05-23

## Summary

One page was modified: the Managed Agents events and streaming reference. All four PHP `streamStream()` code examples were simplified by removing the explicit `requestOptions: ['transporter' => $streamingClient]` argument, indicating the PHP SDK no longer requires a custom transporter to be passed when opening a streaming session.

## Significant Changes

### Managed Agents — PHP SDK

- **`streamStream()` no longer requires explicit transporter configuration**: All four PHP examples in the events-and-streaming documentation were updated to remove the `requestOptions: ['transporter' => $streamingClient]` parameter from `streamStream()` calls.

  Before:
  ```php
  $stream = $client->beta->sessions->events->streamStream(
      $session->id,
      requestOptions: ['transporter' => $streamingClient],
  );
  ```
  After:
  ```php
  $stream = $client->beta->sessions->events->streamStream($session->id);
  ```

  > `$stream = $client->beta->sessions->events->streamStream($session->id);`

  - *Implication*: PHP developers using the Managed Agents SDK can simplify their streaming setup — the SDK now handles transport internally. Existing code passing a custom `$streamingClient` transporter should be updated to omit the `requestOptions` argument.
  - *Source*: [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming.md)

## Minor Changes

- **`en/managed-agents/events-and-streaming.md`**: Simplified PHP `streamStream()` call signature across 4 code examples by removing `requestOptions: ['transporter' => ...]` (+4/-16 lines)

## Changes by Page

| Page | Type | Triage | Lines Changed | Summary |
|------|------|--------|---------------|---------|
| `docs/api/en/managed-agents/events-and-streaming.md` | Modified | SIGNIFICANT | +4/-16 | PHP `streamStream()` examples simplified — `requestOptions` transporter argument removed |

---
*Generated from Claude API documentation changes detected on 2026-05-23*
