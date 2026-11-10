#!/usr/bin/env python3
"""Render a real product screenshot as a reusable SlidesTutor social card."""
import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


W, H = 1080, 1440
FONT = "/System/Library/Fonts/PingFang.ttc"


def font(size):
    return ImageFont.truetype(FONT, size=size, index=0)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--caption", default="")
    ap.add_argument("--eyebrow", default="SLIDESTUTOR · AI 学习空间")
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), "#F8F8F6")
    px = img.load()
    for y in range(H):
        for x in range(W):
            a = max(0, 1 - math.hypot(x - 130, y - 100) / 650)
            b = max(0, 1 - math.hypot(x - 970, y - 430) / 650)
            px[x, y] = (int(248 - 8 * a + 4 * b), int(248 - 7 * a + 5 * b), int(246 + 8 * a + 4 * b))
    d = ImageDraw.Draw(img)
    rounded(d, (70, 70, 432, 116), 23, "#EEEAFE")
    d.text((88, 77), args.eyebrow, font=font(22), fill="#6750D9")
    d.text((70, 154), args.title, font=font(58), fill="#191721")
    if args.subtitle:
        d.text((70, 232), args.subtitle, font=font(29), fill="#686473")

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((60, 350, 1020, 1070), radius=34, fill=(45, 35, 75, 42))
    img.paste(shadow.filter(ImageFilter.GaussianBlur(24)), (0, 12), shadow.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(img)
    rounded(d, (60, 340, 1020, 1060), 34, "#FFFFFF", "#E5E2EC", 2)
    for x, color in [(84, "#FF7068"), (108, "#FFBD4A"), (132, "#50C777")]:
        d.ellipse((x, 361, x + 12, 373), fill=color)
    rounded(d, (177, 358, 992, 377), 10, "#F0F1F2")

    src = Image.open(args.input).convert("RGB")
    x0, y0, x1, y1 = 80, 398, 1000, 1038
    tw, th = x1 - x0, y1 - y0
    scale = min(tw / src.width, th / src.height)
    nw, nh = int(src.width * scale), int(src.height * scale)
    screen = Image.new("RGB", (tw, th), "#F7F7F8")
    screen.paste(src.resize((nw, nh), Image.Resampling.LANCZOS), ((tw - nw) // 2, (th - nh) // 2))
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw, th), radius=16, fill=255)
    img.paste(screen, (x0, y0), mask)

    if args.caption:
        d = ImageDraw.Draw(img)
        rounded(d, (70, 1110, 1010, 1260), 30, "#FFFFFF", "#E6E2EE", 2)
        rounded(d, (94, 1136, 150, 1192), 17, "#7655EE")
        d.line((110, 1164, 134, 1164), fill="#FFFFFF", width=5)
        d.line((122, 1152, 122, 1176), fill="#FFFFFF", width=5)
        d.text((174, 1150), args.caption, font=font(30), fill="#25212C")
    d.text((70, 1330), "SlidesTutor · AI 学习空间", font=font(23), fill="#7655EE")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    img.save(args.output, quality=96)
    print(args.output)


if __name__ == "__main__":
    main()
