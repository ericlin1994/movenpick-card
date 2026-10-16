#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把客戶提供的彩色 logo（藍字＋橘三角、白底）轉成「白色去背 PNG」，並收緊
盾牌與公司名之間的距離。

- 白色版用在深色照片／深藍底上（名片卡片左上角）。
- alpha 用「離白色的距離」算（d = 255 - min(R,G,B)），不是亮度：
  這樣藍色字（藍通道高、紅通道低）與橘色三角都會得到相同的實心 alpha，
  不會出現橘色比藍色淡的問題。
- 原圖盾牌與文字的間距是 119px（以 126px 高的盾牌來說太開），
  這裡自動偵測兩者之間的空白欄並重排成 GAP。
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
GAP = 38           # 盾牌與文字之間要留的寬度（px，原圖尺度）


def split_blocks(im):
    """回傳 (左塊, 右塊)：用整欄全空白的區段切開盾牌與文字。"""
    col = (np.array(im)[:, :, 3] > 40).sum(axis=0)
    runs, s = [], None
    for i, c in enumerate(col):
        if c == 0 and s is None:
            s = i
        elif c != 0 and s is not None:
            runs.append((s, i - 1))
            s = None
    if s is not None:
        runs.append((s, len(col) - 1))
    gaps = [r for r in runs if r[1] - r[0] >= 2]
    if not gaps:
        raise SystemExit("✗ 找不到盾牌與文字之間的空白區段，無法重排間距")
    g0, g1 = max(gaps, key=lambda r: r[1] - r[0])       # 最寬的空白 = 兩塊之間
    return im.crop((0, 0, g0, im.height)), im.crop((g1 + 1, 0, im.width, im.height))


def main():
    im = Image.open(SRC).convert("RGB")
    arr = np.array(im).astype(np.float32)
    d = 255.0 - arr.min(axis=2)                      # 離白色的距離
    a = np.clip((d - T0) / (T1 - T0), 0, 1) * 255
    out = Image.fromarray(np.dstack([np.full_like(a, 255.0)] * 3 + [a]).astype(np.uint8), "RGBA")
    out = out.crop(out.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox())

    mark, text = split_blocks(out)
    print(f"  盾牌 {mark.size}　文字 {text.size}　"
          f"原間距 {out.width - mark.width - text.width}px → {GAP}px")

    new = Image.new("RGBA", (mark.width + GAP + text.width, out.height), (0, 0, 0, 0))
    new.alpha_composite(mark, (0, 0))
    new.alpha_composite(text, (mark.width + GAP, 0))
    new.save(OUT)
    print(f"✓ {OUT.name} {new.size}（原圖 {im.size}，裁切後 {out.size}）")


if __name__ == "__main__":
    main()
