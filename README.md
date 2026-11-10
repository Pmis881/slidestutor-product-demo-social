# SlidesTutor 社媒素材 Skill

一个可复用的 Agent Skill：把 SlidesTutor 的真实产品录屏或截图，制作成适合小红书和其他社交平台的产品展示素材。

支持两种主要输出：

- 竖版 MP4 产品功能演示视频
- 静态 PNG 功能介绍图 / 轮播页

## Included

- `SKILL.md` — 使用场景、品牌规范和制作流程
- `scripts/render_product_demo.py` — 1080×1440 MP4 渲染器
- `scripts/render_static_product_demo.py` — 1080×1440 静态 PNG 渲染器
- `references/xiaohongshu-spec.md` — 小红书规格与检查标准
- `agents/openai.yaml` — Codex skill 元信息

默认品牌名是 `SlidesTutor`，左上角全大写标识必须写成 `SLIDESTUTOR`，官网是 `slidestutor.com`。

## 视频：快速开始

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

输出为静音 H.264 MP4，尺寸 1080×1440、24 fps，默认最长 10 秒。

## 静态图：快速开始

```bash
python3 scripts/render_static_product_demo.py \
  --input screenshot.png \
  --output out/slidestutor-feature.png \
  --title "PDF 翻译，手写也能识别" \
  --subtitle "扫描件、数学公式、课件内容都能处理" \
  --caption "手写内容和公式也能识别、整理与翻译"
```

输出为 1080×1440 PNG，适合小红书首图、功能介绍页和轮播图。

## 设计原则

始终使用真实产品画面；统一使用 SlidesTutor / SLIDESTUTOR；保持浅色背景、紫色强调色、清晰的利益点标题；不要为了“好看”虚构产品界面或功能结果。
