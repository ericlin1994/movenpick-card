#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""卡片 2／3／4 的背景圖：把客戶提供的玻璃實拍照壓成「深藍底紋」。

為什麼要壓這麼暗：
  這三張卡的文字是 Flex 文字（不是烤進圖裡的），顏色固定為白／銅金／
  米白底深藍字。實拍照左側是米白牆、右上與地板有大面積爆亮，白字直接壓上去
  會整片消失，所以背景必須壓到跟品牌 NAVY (#253043) 相近的暗度，
  只留下玻璃的紋理與光斑。

用法：python make_bg.py        → card_bg.jpg（1080x1440）
"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
SRC = HERE / "card_bg_src.jpg"
OUT = HERE / "card_bg.jpg"
W, H = 1080, 1440

TOP_FRAC = 0.40      # 垂直裁切位置（0.5 = 置中；照片下方是爆亮地板，略往上取）
BRIGHT = 0.40        # 整體亮度（1.0 = 原圖）
DESAT = 0.58         # 降飽和比例
NAVY = (0x25, 0x30, 0x43)
NAVY_K = 0.30        # 疊上品牌深藍的比例
BLUR = 1.6           # 輕微模糊，讓背景退到後面
FLOOR_DARK = 0.26    # 底部再加暗（讓下方的文字更穩）


def build(bright=BRIGHT, desat=DESAT, navy_k=NAVY_K, blur=BLUR, top_frac=TOP_FRAC):
    im = Image.open(SRC).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = max(0, min(int((im.height - H) * top_frac), im.height - H))
    im = im.crop((x, y, x + W, y + H))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))

    a = np.array(im).astype(np.float32)
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    a = a * (1 - desat) + lum[..., None] * desat          # 降飽和
    a = a * bright                                        # 壓暗
    a = a * (1 - navy_k) + np.array(NAVY, np.float32) * navy_k   # 混品牌深藍
    k = np.ones((H, 1), np.float32)
    k[int(H * 0.55):] = np.linspace(1, 1 - FLOOR_DARK, H - int(H * 0.55))[:, None]
    a = a * k[:, :, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


if __name__ == "__main__":
    im = build()
    im.save(OUT, "JPEG", quality=92, optimize=True)
    print(f"✓ {OUT.name} {im.size}")
