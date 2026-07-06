#!/usr/bin/env python3
"""
RakyatHub Hero Banner Generator — v1
Generates OG-image-style banners: gradient background + overlay text.

Called when Tier 1 (screenshot) & Tier 2 (portal logo) are unavailable.
Generates a gradient background via Pollinations, then composites
the article title on top using Pillow.

Usage:
  python3 scripts/generate-hero-banner.py <slug> <title> [--category <cat>]

Output:
  src/assets/images/hero-<slug>.jpg  (1200×630 banner)
"""

import sys
import os
import json
import tempfile
import urllib.request
import urllib.parse

# Pillow
from PIL import Image, ImageDraw, ImageFont, ImageFilter

###############################################################################
# Category colour palettes
###############################################################################
PALETTES = {
    "bof_tutorial":      ("#0D9488", "#042F2E", "teal"),
    "kerajaan_cukai":    ("#1E40AF", "#1E3A5F", "navy"),
    "umum_kesihatan":    ("#0F766E", "#134E4A", "teal-green"),
    "kerjaya_bisnes":    ("#1E3A5F", "#B8860B", "navy-gold"),
    "pendidikan_student":("#4F46E5", "#1E1B4B", "indigo"),
    "hartanah_sewa":     ("#C2410C", "#431407", "orange"),
    "insurans":          ("#0891B2", "#164E63", "cyan"),
    "teknologi":         ("#7C3AED", "#2E1065", "purple"),
    "gaya_hidup":        ("#059669", "#064E3B", "emerald"),
    "default":           ("#0F766E", "#1E3A5F", "teal-navy"),
}

# Fallback gradient colours if Pollinations fails
FALLBACK_COLORS = [
    ("#0F766E", "#134E4A"),
    ("#1E40AF", "#1E3A5F"),
    ("#7C3AED", "#2E1065"),
    ("#C2410C", "#431407"),
    ("#4F46E5", "#1E1B4B"),
]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def generate_gradient(width, height, color1, color2):
    """Generate a vertical gradient image (Pillow)."""
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(c1[0] + (c2[0] - c1[0]) * y / height)
        g = int(c1[1] + (c2[1] - c1[1]) * y / height)
        b = int(c1[2] + (c2[2] - c1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def fetch_pollinations_bg(prompt):
    """Fetch a gradient background from Pollinations. Returns bytes or None."""
    url = (
        "https://image.pollinations.ai/prompt/"
        + urllib.parse.quote(prompt)
        + "?width=1200&height=630&nofeed=true"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RakyatHub/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception:
        return None


def find_best_font(size):
    """Try to find a suitable bold font."""
    candidates = [
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/ARIALBD.TTF",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/times.ttf",
        # Git Bash / MSYS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    # Last resort: default PIL font (tiny)
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width. Returns list of lines."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0, 0), test, font=font)
        tw = bbox[2] - bbox[0]
        if tw <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines if lines else [text]


def build_banner(slug, title, category="default", width=1200, height=630):
    """Main entry: build a banner image and save to assets."""
    pal = PALETTES.get(category, PALETTES["default"])
    color1, color2, _ = pal

    # 1) Try Pollinations for a gradient background
    poll_prompt = f"abstract gradient background {color2} to {color1}, smooth blur, no text, no objects, minimalist banner"
    bg_data = fetch_pollinations_bg(poll_prompt)

    if bg_data:
        # Use Pollinations image as background
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.write(bg_data)
        tmp.close()
        bg_img = Image.open(tmp.name).resize((width, height), Image.LANCZOS)
        os.unlink(tmp.name)
    else:
        # Fallback: generate gradient locally
        bg_img = generate_gradient(width, height, color1, color2)

    # 2) Darken the background slightly so text pops
    overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, 80))
    bg_img = bg_img.convert("RGBA")
    bg_img = Image.alpha_composite(bg_img, overlay)

    # 3) Composite text
    draw = ImageDraw.Draw(bg_img)

    # Category tag (small pill top-left)
    tag_font = find_best_font(28)
    tag_text = category.replace("_", " ").upper()
    tag_padding = (12, 6)
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0] + tag_padding[0] * 2
    tag_h = tag_bbox[3] - tag_bbox[1] + tag_padding[1] * 2
    tag_x, tag_y = 40, 40
    # Draw pill background
    pill_color = hex_to_rgb(color1)
    draw.rounded_rectangle(
        [tag_x, tag_y, tag_x + tag_w, tag_y + tag_h],
        radius=6, fill=(*pill_color, 220)
    )
    # Tag text
    draw.text(
        (tag_x + tag_padding[0], tag_y + tag_padding[1]),
        tag_text, font=tag_font, fill=(255, 255, 255)
    )

    # Title (centered, wrapped)
    title_font = find_best_font(52)
    max_text_width = width - 120
    lines = wrap_text(title, title_font, max_text_width, draw)

    # If too many lines, try smaller font
    if len(lines) > 4:
        title_font = find_best_font(40)
        lines = wrap_text(title, title_font, max_text_width, draw)
    if len(lines) > 5:
        title_font = find_best_font(32)
        lines = wrap_text(title, title_font, max_text_width, draw)

    # Calculate total text block height
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lh = bbox[3] - bbox[1]
        line_heights.append(lh)
    total_text_h = sum(line_heights) + (len(lines) - 1) * 12  # 12px gap

    # Vertical center for text block
    text_y_start = (height - total_text_h) // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        # Drop shadow for readability
        shadow_offset = 3
        draw.text((tx + shadow_offset, text_y_start + shadow_offset),
                  line, font=title_font, fill=(0, 0, 0, 120))
        # Main white text
        draw.text((tx, text_y_start), line, font=title_font, fill=(255, 255, 255))
        text_y_start += line_heights[i] + 12

    # 4) "RakyatHub" branding bottom-right
    brand_font = find_best_font(20)
    brand_text = "RakyatHub.my"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    bx = width - bw - 40
    by = height - bh - 30
    # Semi-transparent background for brand
    draw.rounded_rectangle(
        [bx - 10, by - 5, bx + bw + 10, by + bh + 5],
        radius=4, fill=(0, 0, 0, 100)
    )
    draw.text((bx, by), brand_text, font=brand_font, fill=(255, 255, 255, 200))

    # 5) Save
    out_path = os.path.join(
        os.path.dirname(__file__),
        "..", "src", "assets", "images",
        f"hero-{slug}.jpg"
    )
    out_path = os.path.normpath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bg_img = bg_img.convert("RGB")
    bg_img.save(out_path, "JPEG", quality=88)
    return out_path


###############################################################################
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate hero banner for article")
    parser.add_argument("slug", help="Article slug (e.g. cara-jimat-cashback)")
    parser.add_argument("title", help="Article title")
    parser.add_argument("--category", default="default", help="Category key from PALETTES")
    args = parser.parse_args()

    path = build_banner(args.slug, args.title, args.category)
    result = {
        "slug": args.slug,
        "title": args.title,
        "category": args.category,
        "output": path,
        "status": "ok"
    }
    print(json.dumps(result))
