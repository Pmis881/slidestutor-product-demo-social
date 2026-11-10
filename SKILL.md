---
name: product-demo-social
description: Turn a real product screen recording into a polished, templated vertical MP4 showcase for 小红书/Xiaohongshu and other social feeds. Use for product feature demos, app walkthrough cards, and reusable branded screen-recording layouts. Do not use for Live Photo, GIF conversion, or static covers.
metadata:
  version: 1.0.0
---

# Product Demo Social

Create a short, legible product showcase using the supplied screen recording as the focal point. Preserve the real UI and do not fabricate product behavior. The only deliverable is a vertical MP4 unless the user explicitly asks for additional ordinary video sizes.

## Required inputs

Obtain or infer:

- a screen recording (`.mp4`, `.mov`, `.webm`, or `.gif`)
- one headline describing the user benefit
- optional subtitle or proof line
- optional logo, mascot, brand color, or eyebrow label
- output directory

If a URL is supplied instead of a recording, ask which interaction should be demonstrated before operating the site. Never enter credentials, publish, purchase, or submit consequential forms without explicit authorization.

## Default production choices

- Deliver `1080x1440` (3:4), H.264 MP4, 24 fps, normally 6–10 seconds, muted.
- Use `SlidesTutor` as the public-facing brand name in visible branding. The all-caps logo text is `SLIDESTUTOR` (including the `s` after `slide`). Do not output `SlideTutor`, `SLIDETUTOR`, `FriesAI`, or `薯塔AI` unless the user explicitly requests an exception.
- Use a warm off-white background, near-black typography, and one restrained blue-violet accent unless brand colors are supplied.
- Keep headline and subtitle in the top quarter. Use left alignment, a clear hierarchy, and generous margins.
- Use one feature and one visual action per asset. Prefer a tight crop and readable UI over showing the entire page.
- Preserve the recording's aspect ratio. Landscape recordings use a thin browser-card treatment; never place them inside a thick black tablet shell or add black letterboxing.
- Put the supporting claim in a separate light card below the demo rather than floating decorative quote text.
- Avoid random confetti, large empty lower areas, neon gradients, and centered title stacks unless the brand system calls for them.

## Workflow

1. Inspect the recording dimensions, duration, and first/middle/last frames. Trim dead time, loading states, notifications, personal information, and accidental cursor travel.
2. Draft a benefit-led headline, normally no more than 16 Chinese characters, and an optional support line no more than 24 Chinese characters. Preserve user-supplied copy unless asked to rewrite it.
3. Render with `scripts/render_product_demo.py`. Use `--device auto` unless the user specifies the presentation style. Add a mascot only if supplied or requested.
4. Inspect the first, middle, and last frames. Verify the screen is not stretched or letterboxed, typography is balanced, the product card has a thin border, and no copy is clipped.
5. Deliver the MP4 and state its dimensions, duration, and file size.

Example:

```bash
python3 scripts/render_product_demo.py \
  --input demo.mp4 \
  --output out/product-demo.mp4 \
  --title "手写笔记也能看懂？" \
  --subtitle "遇到不会的问题直接问 AI" \
  --caption "适配各种格式文档，学习更轻松" \
  --eyebrow "SLIDESTUTOR · AI 学习空间" \
  --device auto
```

For platform sizing, copy guidance, and review criteria, read [references/xiaohongshu-spec.md](references/xiaohongshu-spec.md).
