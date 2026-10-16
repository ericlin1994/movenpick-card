#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""名片第 1 頁形象照：**不去背**，整張照片滿版當底（1080x1440, 3:4）。

產出：photo.jpg（gen_cards.py 會自動置入 card1）

- benson_raw.jpg 是 9:16 直幅，cover 到 3:4 必須垂直裁切；人物頭頂約在 7.5%，
  因此採「上緣貼齊」裁切（t=0），只切掉下方牛仔褲，頭頂留約 10% 空間給左上品牌字。
- 照片上緣是反光玻璃（偏亮），會壓掉左上角品牌字 → 烤一層很淡的頂部暗階。
- 底部文字區的暗階由 gen_cards.py 統一處理（共用邏輯，不在這裡重複）。
- 整體做輕微冷色調（降飽和 + 偏藍），避免鏡面反射的綠意與品牌深藍/銅金打架。
"""
import pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).parent
W, H = 1080, 1440

SRC = HERE / "benson_raw.jpg"
NAVY_D = (0x1E, 0x28, 0x38)

# 可調參數
CROP_TOP_FRAC = 0.0     # 從原圖上緣切掉的比例（0 = 完整保留頭頂留白）
ZOOM = 1.0              # >1 稍微放大（裁掉一點邊緣的爆亮反射）
DESAT = 0.14            # 降飽和比例
COOL = (0.97, 1.00, 1.05)   # RGB 冷色增益
TOP_SCRIM = 0.45        # 頂部暗階強度（給品牌字）
TOP_SCRIM_H = 0.26      # 暗階覆蓋高度比例
CORNER = 0.62           # 左上角局部壓暗（品牌字壓在反光玻璃上時用）


def cover_crop(im, w, h, top_frac=0.0, zoom=1.0):
    r = max(w / im.width, h / im.height) * zoom
    im = im.resize((max(1, int(round(im.width * r))), max(1, int(round(im.height * r)))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int(round((im.height - h) * top_frac))
    y = max(0, min(y, im.height - h))
    return im.crop((x, y, x + w, y + h))


def grade(im, desat=DESAT, cool=COOL):
    arr = np.array(im).astype(np.float32)
    lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)
    arr = arr * (1 - desat) + lum[..., None] * desat
    arr = arr * np.array(cool, np.float32)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def top_scrim(im, strength=TOP_SCRIM, height_frac=TOP_SCRIM_H, color=NAVY_D):
    h = im.height
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    n = int(h * height_frac)
    for y in range(n):
        a = int(255 * strength * (1 - y / max(1, n - 1)) ** 1.6)
        d.line([(0, y), (im.width, y)], fill=color + (a,))
    return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")


def corner_scrim(im, strength=0.6, rx=680, ry=460, blur=120, color=NAVY_D):
    """左上角局部壓暗：品牌字（80,80）壓在反光玻璃上會看不清楚。
    只暗左上角，人物臉部（畫面中央）不受影響。"""
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([-rx // 2, -ry // 2, rx, ry], fill=color + (int(255 * strength),))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")


def build(top_frac=CROP_TOP_FRAC, zoom=ZOOM, desat=DESAT, cool=COOL,
          scrim=TOP_SCRIM, scrim_h=TOP_SCRIM_H, corner=CORNER):
    im = Image.open(SRC).convert("RGB")
    im = cover_crop(im, W, H, top_frac, zoom)
    if desat or any(abs(c - 1) > 1e-6 for c in cool):
        im = grade(im, desat, cool)
    if scrim > 0:
        im = top_scrim(im, scrim, scrim_h)
    if corner > 0:
        im = corner_scrim(im, corner)
    return im


def main():
    im = build()
    im.save(HERE / "photo.jpg", "JPEG", quality=93, optimize=True)
    print(f"✓ photo.jpg {im.size}（整張照片滿版，未去背）")


if __name__ == "__main__":
    main()
