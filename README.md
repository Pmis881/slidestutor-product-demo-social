# SlideTutor Product Demo Social

Reusable Agent Skill for turning a real product screen recording into a polished vertical MP4 showcase for Xiaohongshu and other social feeds.

## Included

- `SKILL.md` — workflow and production constraints
- `scripts/render_product_demo.py` — deterministic 1080×1440 MP4 renderer
- `references/xiaohongshu-spec.md` — platform sizing and review checklist
- `agents/openai.yaml` — optional Codex skill metadata

The default visible brand is `SlidesTutor`; the all-caps logo label is `SLIDESTUTOR`.

## Quick start

```bash
python3 scripts/render_product_demo.py \
  --input demo.mp4 \
  --output out/slidestutor-demo.mp4 \
  --title "一张图，理清整门课" \
  --subtitle "课件内容自动生成思维导图" \
  --caption "知识结构一目了然，复习不再东翻西找" \
  --eyebrow "SLIDESTUTOR · AI 学习空间" \
  --device auto
```

The renderer outputs a muted H.264 MP4 at 1080×1440 and 24 fps, capped at 10 seconds by default.
