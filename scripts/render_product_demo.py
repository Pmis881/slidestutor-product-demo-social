#!/usr/bin/env python3
"""Render a screen recording in a clean, reusable vertical product showcase."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,duration:format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    duration = float(stream.get("duration") or data.get("format", {}).get("duration") or 0)
    return {"width": int(stream["width"]), "height": int(stream["height"]), "duration": duration}


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    pingfang = Path("/System/Library/Fonts/PingFang.ttc")
    if pingfang.exists():
        index = {"regular": 2, "medium": 5, "semibold": 8}.get(weight, 2)
        return ImageFont.truetype(str(pingfang), size=size, index=index)
    alternatives = [
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for candidate in alternatives:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def parse_hex(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("Color must be a six-digit hex value")
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Invalid hex color") from exc


def wrap(draw: ImageDraw.ImageDraw, value: str, face: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines, current = [], ""
    for char in value:
        candidate = current + char
        if current and draw.textbbox((0, 0), candidate, font=face)[2] > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def left_text(draw, value, x, y, face, color, max_width, spacing=10):
    for line in wrap(draw, value, face, max_width):
        box = draw.textbbox((0, 0), line, font=face)
        draw.text((x, y), line, font=face, fill=color)
        y += box[3] - box[1] + spacing
    return y


def ease_out(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


def background(width: int, height: int, accent: tuple[int, int, int]) -> Image.Image:
    canvas = Image.new("RGB", (width, height), (248, 248, 245))
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((-230, -250, 540, 520), fill=(*accent, 26))
    draw.ellipse((760, 780, 1370, 1450), fill=(115, 92, 255, 22))
    draw.ellipse((640, -180, 1240, 370), fill=(126, 231, 217, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    return Image.alpha_composite(canvas.convert("RGBA"), glow)


def make_product_card(frame: Image.Image, content_size: tuple[int, int], browser: bool) -> Image.Image:
    content_w, content_h = content_size
    outer_pad = 10
    chrome = 46 if browser else 0
    card_w = content_w + outer_pad * 2
    card_h = content_h + outer_pad * 2 + chrome
    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(card)
    if browser:
        for i, color in enumerate(((255, 101, 92), (255, 190, 70), (52, 201, 92))):
            x = 24 + i * 24
            draw.ellipse((x, 18, x + 11, 29), fill=color)
        draw.rounded_rectangle((120, 13, card_w - 26, 34), radius=10, fill=(243, 244, 246, 255))
    card.alpha_composite(frame.convert("RGBA"), (outer_pad, outer_pad + chrome))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, card_w - 1, card_h - 1), radius=26, fill=255)
    card.putalpha(mask)
    return card


def paste_with_shadow(canvas: Image.Image, item: Image.Image, position: tuple[int, int], radius: int = 28) -> None:
    x, y = position
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.rounded_rectangle((x + 4, y + 18, x + item.width + 4, y + item.height + 18),
                           radius=radius, fill=(31, 41, 55, 52))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(item, (x, y))


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--caption", default="")
    parser.add_argument("--eyebrow", default="PRODUCT DEMO")
    parser.add_argument("--device", choices=("auto", "browser", "tablet", "phone", "plain"), default="auto")
    parser.add_argument("--mascot", type=Path)
    parser.add_argument("--accent", type=parse_hex, default=(88, 77, 230))
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=0, help="0 keeps input duration, capped at 10 seconds")
    return parser.parse_args()


def main():
    args = arguments()
    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required")
    meta = probe(args.input)
    duration = min(args.duration or meta["duration"] or 8, 10)
    ratio = meta["width"] / meta["height"]
    device = args.device
    if device == "auto":
        device = "phone" if ratio < 0.78 else "browser"
    browser = device in ("browser", "tablet")

    if ratio >= 1.15:
        content_w = 936
        content_h = max(360, round(content_w / ratio))
    elif ratio < 0.78:
        content_h = 760
        content_w = round(content_h * ratio)
    else:
        content_w = 760
        content_h = round(content_w / ratio)
    if content_h > 760:
        content_h = 760
        content_w = round(content_h * ratio)

    chrome = 46 if browser else 0
    card_size = (content_w + 20, content_h + 20 + chrome)
    card_x = (args.width - card_size[0]) // 2
    card_y = 382 if ratio >= 1.15 else 350

    decode = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-stream_loop", "-1", "-i", str(args.input), "-t", str(duration),
         "-vf", f"fps={args.fps},scale={content_w}:{content_h}:flags=lanczos",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    encode = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{args.width}x{args.height}", "-r", str(args.fps), "-i", "-", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(args.output)],
        stdin=subprocess.PIPE,
    )

    raw_size = content_w * content_h * 3
    eyebrow_face = font(22, "semibold")
    title_face = font(72, "semibold")
    subtitle_face = font(34, "regular")
    caption_face = font(34, "medium")
    small_face = font(22, "medium")
    mascot = Image.open(args.mascot).convert("RGBA") if args.mascot else None
    if mascot:
        mascot.thumbnail((220, 220), Image.Resampling.LANCZOS)

    total = math.ceil(duration * args.fps)
    try:
        for index in range(total):
            raw = decode.stdout.read(raw_size)
            if len(raw) != raw_size:
                break
            source = Image.frombytes("RGB", (content_w, content_h), raw)
            canvas = background(args.width, args.height, args.accent)

            intro = ease_out(index / max(1, args.fps * 0.45))
            copy_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(copy_layer)
            copy_y = round(76 - (1 - intro) * 14)
            label = args.eyebrow.upper()
            label_box = draw.textbbox((0, 0), label, font=eyebrow_face)
            pill_w = label_box[2] - label_box[0] + 34
            draw.rounded_rectangle((70, copy_y, 70 + pill_w, copy_y + 40), radius=20,
                                   fill=(*args.accent, round(26 * intro)))
            draw.text((87, copy_y + 7), label, font=eyebrow_face, fill=(*args.accent, round(255 * intro)))
            title_y = copy_y + 62
            title_y = left_text(draw, args.title, 70, title_y, title_face, (20, 25, 38, round(255 * intro)), 940, 4)
            if args.subtitle:
                left_text(draw, args.subtitle, 72, title_y + 14, subtitle_face,
                          (89, 96, 112, round(255 * intro)), 920, 7)
            canvas = Image.alpha_composite(canvas, copy_layer)

            card = make_product_card(source, (content_w, content_h), browser)
            card_intro = ease_out(max(0.0, index / args.fps - 0.08) / 0.48)
            animated_y = card_y + round((1 - card_intro) * 24)
            card.putalpha(card.getchannel("A").point(lambda value: round(value * card_intro)))
            paste_with_shadow(canvas, card, (card_x, animated_y))

            caption_y = card_y + card_size[1] + 62
            if args.caption and caption_y < args.height - 120:
                caption_intro = ease_out(max(0.0, index / args.fps - 0.18) / 0.45)
                caption_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
                cd = ImageDraw.Draw(caption_layer)
                card_left, card_right = 70, args.width - 70
                cap_lines = wrap(cd, args.caption, caption_face, card_right - card_left - 126)
                cap_h = max(122, 46 + len(cap_lines) * 46)
                cy = caption_y + round((1 - caption_intro) * 14)
                cd.rounded_rectangle((card_left, cy, card_right, cy + cap_h), radius=30,
                                     fill=(255, 255, 255, round(235 * caption_intro)),
                                     outline=(225, 227, 234, round(255 * caption_intro)), width=2)
                cd.rounded_rectangle((94, cy + 30, 146, cy + 82), radius=16,
                                     fill=(*args.accent, round(255 * caption_intro)))
                cd.line((110, cy + 56, 130, cy + 56), fill=(255, 255, 255, round(255 * caption_intro)), width=4)
                cd.line((120, cy + 46, 120, cy + 66), fill=(255, 255, 255, round(255 * caption_intro)), width=4)
                ty = cy + 27
                for line in cap_lines:
                    cd.text((170, ty), line, font=caption_face, fill=(36, 42, 56, round(255 * caption_intro)))
                    ty += 46
                cd.text((170, cy + cap_h - 30), "核心功能演示", font=small_face,
                        fill=(*args.accent, round(210 * caption_intro)))
                canvas = Image.alpha_composite(canvas, caption_layer)

            if mascot:
                canvas.alpha_composite(mascot, (args.width - mascot.width - 35, args.height - mascot.height - 24))
            encode.stdin.write(canvas.convert("RGB").tobytes())
    finally:
        if encode.stdin:
            encode.stdin.close()
        encode.wait()
        decode.kill()

    if encode.returncode:
        raise SystemExit(f"Video encoding failed with code {encode.returncode}")
    print(json.dumps({
        "output": str(args.output), "duration": duration, "fps": args.fps,
        "size": [args.width, args.height], "template": "clean-card-v2",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
