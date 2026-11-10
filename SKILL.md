---
name: product-demo-social
description: Create polished, reusable SlidesTutor social assets from real product recordings or screenshots, including vertical MP4 demos and static Xiaohongshu feature cards. Use for product feature demos, app walkthroughs, social carousels, and branded product visuals. Do not fabricate product UI.
metadata:
  version: 1.1.0
---

# SlideTutor Social Assets

Create short, legible product assets using real product recordings or screenshots as the focal point. Preserve the real UI and do not fabricate product behavior. Choose the output format from the user's request: vertical MP4 for motion demos, or a static PNG for feature cards and carousel pages.

## Required inputs

Obtain or infer:

- a screen recording (`.mp4`, `.mov`, `.webm`, or `.gif`) for video, or a screenshot (`.png`, `.jpg`, `.webp`) for static output
- one headline describing the user benefit
- optional subtitle or proof line
- optional logo, mascot, brand color, or eyebrow label
- output directory

If a URL is supplied instead of a recording, ask which interaction should be demonstrated before operating the site. Never enter credentials, publish, purchase, or submit consequential forms without explicit authorization.

## Default production choices

- Deliver `1080x1440` (3:4). For video, use H.264 MP4, 24 fps, normally 6–10 seconds, muted. For static assets, use PNG.
- Use `SlidesTutor` as the public-facing brand name in visible branding. The all-caps logo text is `SLIDESTUTOR` (including the `s` after `slide`). Do not output `SlideTutor`, `SLIDETUTOR`, `FriesAI`, or `薯塔AI` unless the user explicitly requests an exception.
- Use a warm off-white background, near-black typography, and one restrained blue-violet accent unless brand colors are supplied.
- Keep headline and subtitle in the top quarter. Use left alignment, a clear hierarchy, and generous margins.
- Use one feature and one visual action per asset. Prefer a tight crop and readable UI over showing the entire page.
- Preserve the recording's aspect ratio. Landscape recordings use a thin browser-card treatment; never place them inside a thick black tablet shell or add black letterboxing.
- Put the supporting claim in a separate light card below the demo rather than floating decorative quote text.
- Avoid random confetti, large empty lower areas, neon gradients, and centered title stacks unless the brand system calls for them.

## Workflow

1. Identify the output mode. For video, inspect recording dimensions, duration, and first/middle/last frames. For static output, inspect the screenshot and choose the most informative crop.
2. Draft a benefit-led headline, normally no more than 16 Chinese characters, and an optional support line no more than 24 Chinese characters. Preserve user-supplied copy unless asked to rewrite it.
3. Render video with `scripts/render_product_demo.py`; use `--device auto` unless the user specifies the presentation style. Render static cards with `scripts/render_static_product_demo.py`.
4. Inspect the output. For video, check first/middle/last frames. For static cards, check the full PNG at 100% and a phone-sized preview. In both modes, verify no stretching, clipping, black letterboxing, or incorrect branding.
5. Deliver the requested files and state dimensions, duration (video only), and file size.

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
