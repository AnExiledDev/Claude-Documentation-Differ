# Claude API Documentation Changes — 2026-04-23

## Summary

Two pages in the "Build with Claude" section were updated. The embeddings guide received a substantial update adding the Voyage 4 model family (four new text embedding models and a new multimodal model with video support), retiring `voyage-3.5` as the recommended default. The vision guide gained a new best-practice note on image compression trade-offs.

## Significant Changes

### Embeddings — Voyage 4 Model Family

- **New recommended text embedding models (`voyage-4`, `voyage-4-large`, `voyage-4-lite`, `voyage-4-nano`)**: The Voyage 4 generation replaces `voyage-3.5` as the documented recommended default. The documentation now groups models into "Voyage 4 (latest generation)" and "Previous generation" sections.

  > **Voyage 4 (latest generation)**
  >
  > | Model | Context Length | Embedding Dimension | Description |
  > | --- | --- | --- | --- |
  > | `voyage-4-large` | 32,000 | 1024 (default), 256, 512, 2048 | The best general-purpose and multilingual retrieval quality. |
  > | `voyage-4` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for general-purpose and multilingual retrieval quality. Balances quality and efficiency. |
  > | `voyage-4-lite` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for latency and cost. |
  > | `voyage-4-nano` | 32,000 | 1024 (default), 256, 512, 2048 | Open-weight model (Apache 2.0 license) available on Hugging Face. |

  - *Implication*: All four models share the same 32,000-token context length and support the same four embedding dimension options (256, 512, 1024, 2048). `voyage-4-nano` is notable as an Apache 2.0 open-weight model available via Hugging Face — suitable for on-premises or air-gapped deployments.
  - *Source*: [Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings.md)

- **New multimodal model `voyage-multimodal-3.5` with video support**: Added alongside the existing `voyage-multimodal-3`. Described as the first production-grade video embedding model.

  > `voyage-multimodal-3.5` — Rich multimodal embedding model that can vectorize interleaved text, images, and videos. Includes video support as the first production-grade video embedding model.

  - *Implication*: Developers building video search or retrieval pipelines can now use a Voyage-hosted embedding model directly rather than custom solutions. The new model also adds variable output dimensions (256, 512, 1024, 2048) absent from `voyage-multimodal-3` (which was fixed at 1024).
  - *Source*: [Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings.md)

- **Code examples and FAQ updated to use `voyage-4`**: All Python and cURL snippet references to `voyage-3.5` have been updated to `voyage-4`. The FAQ "which model should I use?" answer now recommends `voyage-4-large` (best quality), `voyage-4-lite` (lowest latency/cost), and `voyage-4` (balanced) — replacing the prior `voyage-3-large`, `voyage-3.5-lite`, `voyage-3.5` recommendations.
  - *Implication*: Copy-pasting documentation examples will now target the Voyage 4 generation by default. Existing integrations using `voyage-3.5` continue to work but are now documented as "previous generation."
  - *Source*: [Embeddings](https://platform.claude.com/docs/en/build-with-claude/embeddings.md)

### Vision — Image Compression Guidance

- **New best-practice note on image compression trade-offs**: A new bullet was added to the "Ensuring image quality" section explaining the latency vs. fidelity trade-off when using lossy image compression before sending images to the API.

  > **Image compression**: Compressing images before sending them, using a lossy format such as JPEG or WebP (lossy mode), can reduce latency by reducing the size of requests. However, this can introduce artifacts that are detrimental to model performance, especially when multiple compression passes are applied. For example, heavy JPEG compression can make text difficult to read. Confirm your compression settings are appropriate for the task by inspecting the actual images sent to the API.

  - *Implication*: Developers optimizing for speed by compressing images should verify the compressed output is still legible to the model, particularly for text-heavy documents. Multiple re-compression passes (e.g., compress → upload → re-encode → re-upload) are called out as a specific risk.
  - *Source*: [Vision](https://platform.claude.com/docs/en/build-with-claude/vision.md)

## Changes by Page

| Page | Type | Lines Changed | Summary |
|------|------|---------------|---------|
| `build-with-claude/embeddings.md` | Modified | +22 / -10 | Added Voyage 4 model family (4 text + 1 multimodal model); updated code examples from `voyage-3.5` to `voyage-4`; reorganized models into "latest generation" vs. "previous generation" |
| `build-with-claude/vision.md` | Modified | +1 / -0 | Added image compression trade-off guidance to best-practices section |

---
*Generated from Claude API documentation changes detected on 2026-04-23*
