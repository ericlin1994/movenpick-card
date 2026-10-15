#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把去背後的人像合成為名片第 1 頁的形象照（1080x1440，3:4）。

產出：photo.jpg（gen_cards.py 會自動置入 card1）
- 人物底部貼齊畫布下緣（不懸空），頭頂留白給左上品牌字
- 邊緣內縮 1px 去除去背灰白邊
- 背景＝深藍漸層＋銅金柔光＋極淡玻璃斜切面＋底噪，與卡片主色一致
"""
import pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = pathlib.Path(__file__).parent
W, H = 1080, 1440

HERO_TOP, HERO_BOT = (0x1A, 0x26, 0x36), (0x34, 0x4A, 0x5C)
COPPER = (0xC4, 0x83, 0x5A)
NAVY_D = (0x1E, 0x28, 0x38)

HEAD_TOP_Y = 176
BOTTOM_FADE = 0      # 貼齊下緣，不留硬切線


def gradient(size, top, bot):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
    return img


def background():
    img = gradient((W, H), HERO_TOP, HERO_BOT).convert("RGBA")

    # 1) 玻璃斜切面：極淡，只留氛圍（降對比、加大模糊，避免「數位感」）
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, x in enumerate(range(-300, W + 400, 210)):
        d.line([(x, H), (x + 560, 0)], fill=(255, 255, 255, 9), width=40 - (i % 4) * 8)
    for i, x in enumerate(range(-140, W + 320, 300)):
        d.line([(x, H), (x + 320, 0)], fill=COPPER + (10,), width=18)
    img = Image.alpha_composite(img, lay.filter(ImageFilter.GaussianBlur(26)))

    # 2) 右上銅金柔光
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W - 640, -440, W + 340, 380], fill=COPPER + (70,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(150)))

    # 3) 左下壓暗
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(vig).ellipse([-520, H - 920, 640, H + 400], fill=NAVY_D + (105,))
    img = Image.alpha_composite(img, vig.filter(ImageFilter.GaussianBlur(160)))

    # 4) 細微底噪，避免漸層出現色帶（banding）
    rgb = np.array(img).astype(np.float32)
    rng = np.random.default_rng(7)
    rgb[:, :, :3] += rng.normal(0, 2.1, (H, W, 1))
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGBA")


def fix_grid_remnant(rgba):
    """修掉衣襬與手臂夾縫間漏去背的金屬菱格網（低飽和的灰白像素）。"""
    arr = np.array(rgba).astype(np.float32)
    hsv = np.array(Image.fromarray(arr[:, :, :3].astype(np.uint8)).convert("HSV")).astype(np.float32)
    x1, y1, x2, y2 = 534, 804, 582, 898
    box = (slice(y1, y2), slice(x1, x2))
    kill = (hsv[:, :, 1][box] / 255.0) < 0.24
    alpha = arr[:, :, 3][box]
    before = int((alpha > 128).sum())
    alpha[kill] = 0
    arr[:, :, 3][box] = alpha
    print(f"  夾縫殘留清除：{before} → {int((alpha > 128).sum())} px")
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def defringe(rgba, shrink=1.2):
    """內縮 alpha 一圈再羽化，去掉去背留下的灰白邊。"""
    a = np.array(rgba.split()[-1]).astype(np.float32) / 255.0
    m = a >= 0.5
    if shrink > 0:
        m = ndimage.binary_erosion(m, np.ones((3, 3), bool), iterations=max(1, int(round(shrink))))
    a2 = ndimage.gaussian_filter(np.where(m, 1.0, 0.0).astype(np.float32), 0.9)
    arr = np.array(rgba).astype(np.float32)
    arr[:, :, 3] = np.clip(a2, 0, 1) * 255
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def main():
    cut = Image.open(HERE / "benson_cut_u2net_clean.png").convert("RGBA")
    cut = fix_grid_remnant(cut)
    cut = defringe(cut)

    a = np.array(cut)[:, :, 3]
    ys, xs = np.where(a > 128)
    subj = cut.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

    # 底部貼齊下緣、頭頂落在 HEAD_TOP_Y
    s = (H - HEAD_TOP_Y) / subj.height
    subj = subj.resize((max(1, round(subj.width * s)), max(1, round(subj.height * s))), Image.LANCZOS)
    x, y = (W - subj.width) // 2, HEAD_TOP_Y
    print(f"  人物框 {subj.size}  貼上 x={x} y={y}  底部={y + subj.height}")

    bg = background()
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.paste(COPPER + (130,), (x, y), subj.split()[-1])
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(46)))
    bg.alpha_composite(subj, (x, y))

    if BOTTOM_FADE:
        arr = np.array(bg).astype(np.float32)
        k = np.ones(H, np.float32)
        k[H - BOTTOM_FADE:] = np.linspace(1, 0, BOTTOM_FADE)
        arr[:, :, 3] *= k[:, None]
        bg = Image.fromarray(arr.astype(np.uint8), "RGBA")

    out = bg.convert("RGB")
    out.save(HERE / "photo.jpg", "JPEG", quality=93, optimize=True)
    print(f"✓ photo.jpg {out.size}")


if __name__ == "__main__":
    main()
