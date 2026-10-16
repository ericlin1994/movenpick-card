#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把客戶提供的彩色 logo（藍字＋橘三角、白底）轉成「白色去背 PNG」。

- 白色版用在深色照片／深藍底上（名片卡片左上角）。
- alpha 用「離白色的距離」算（d = 255 - min(R,G,B)），不是亮度：
  這樣藍色字（藍通道高、紅通道低）與橘色三角都會得到相同的實心 alpha，
  不會出現橘色比藍色淡的問題。
- 輸出會自動裁掉白邊，讓貼圖時的定位與尺寸可控。

用法：python make_logo.py            → brand_logo_white.png
"""
import pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).parent
SRC = HERE / "brand_logo.jpg"
OUT = HERE / "brand_logo_white.png"

T0, T1 = 40, 200   # d 低於 T0 視為背景、高於 T1 視為實心


def main():
    im = Image.open(SRC).convert("RGB")
    arr = np.array(im).astype(np.float32)
    d = 255.0 - arr.min(axis=2)                      # 離白色的距離
    a = np.clip((d - T0) / (T1 - T0), 0, 1) * 255
    rgba = np.dstack([np.full_like(a, 255.0)] * 3 + [a]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
    out = out.crop(bbox)
    out.save(OUT)
    print(f"✓ {OUT.name} {out.size}（原圖 {im.size}，裁切框 {bbox}）")


if __name__ == "__main__":
    main()
