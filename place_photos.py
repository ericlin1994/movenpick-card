#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把客戶給的照片放進名片網頁與卡片的圖片版位。

輸出尺寸：
  craft1~4 / case1~N  4:3（CSS: .craft img{aspect-ratio:4/3;object-fit:cover}）
  gallery1~N          1:1（CSS: .wall  img{aspect-ratio:1/1;object-fit:cover}）
  card5_hero.jpg      1080x1440（卡片第 5 頁主視覺）

每張可指定：
  fv    = 裁切的垂直重心（0=留上方、1=留下方）
  fh    = 裁切的水平重心（0=留左方、1=留右方）
  max_w = 輸出寬度上限（來源太小就不要硬放大，避免糊掉）
"""
import pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
SRC = HERE / "photos_raw"

WEB_W, WEB_H = 1200, 900          # 4:3
CARD_W, CARD_H = 1080, 1440       # 3:4

# slot -> (來源, fv, fh, max_w)
PLAN = {
    # ── 工藝特寫（4:3）──
    "craft1.jpg":     ("p01.jpg", 0.50, 0.50, 1200),  # 鑲嵌複合玻璃面板（工作台）
    "craft2.jpg":     ("p10.jpg", 0.45, 0.50, 1200),  # 冰花壓花玻璃＋金屬嵌條（透光不透視）
    "craft3.jpg":     ("p23.jpg", 0.50, 0.50, 1200),  # 彩色厚板疊層＋金屬收邊
    "craft4.jpg":     ("p12.jpg", 0.50, 0.50, 1200),  # 金色心經＋彌勒噴砂雕刻玻璃
    # ── 施作案例（4:3）──
    "case1.jpg":      ("p04.jpg", 0.50, 0.50, 1200),  # 聖明堂外觀（黃昏全景）
    "case2.jpg":      ("p17.jpg", 0.50, 0.50, 1200),  # 和室書法雕刻霧面玻璃隔屏
    "case3.jpg":      ("p08.jpg", 0.50, 0.50, 1200),  # 十二星座鑲嵌彩繪穹頂
    "case4.jpg":      ("p20.jpg", 0.50, 0.50, 950, (0, 0, 800, 510)),   # 室內幾何鑲嵌玻璃隔屏實景（切掉底部型號資訊列＋商標）
    "case5.jpg":      ("p05.jpg", 0.50, 0.50, 1200),  # 聖明堂鳳凰深雕玻璃門
    "case6.jpg":      ("p18.jpg", 0.50, 0.85, 1200),  # 室內木作立體浮雕玻璃隔屏（裁右側，避開左邊走道）
    # ── 作品牆（1:1）──
    "gallery1.jpg":   ("p11.jpg", 0.50, 0.50, 700),   # 彩色抽象幾何紋理藝術玻璃
    "gallery2.jpg":   ("p22.jpg", 0.50, 0.50, 700, (0, 90, 430, 520)),  # 木框幾何複合鑲嵌藝術玻璃門（切掉下方後製倒影）
    "gallery3.jpg":   ("p16.jpg", 0.50, 0.50, 700),   # 層疊造型藝術玻璃與流動光影
    "gallery4.jpg":   ("p21.jpg", 0.50, 0.50, 700),   # 古典雙開木門鑲嵌藝術玻璃
    "gallery5.jpg":   ("p13.jpg", 0.40, 0.50, 700),   # 歐式豪宅鍛鐵玻璃大門與彩色雨遮
    "gallery6.jpg":   ("p07.jpg", 0.42, 0.50, 700),   # 飯店大廳彩繪穹頂
    "gallery7.jpg":   ("p06.jpg", 0.00, 0.50, 700, (0, 0, 910, 620)),  # 佛堂彩雕藝術玻璃背牆（切掉下方後製倒影）
    "gallery8.jpg":   ("p02.jpg", 0.40, 0.50, 700),   # 住宅玄關發光雕刻屏風
    "gallery9.jpg":   ("p09.jpg", 0.50, 0.50, 700),   # 歐式豪宅入口彩繪玻璃雨遮
    # ── 卡片第 5 頁主視覺（3:4）──
    "card5_hero.jpg": ("p10.jpg", 0.50, 0.50, 1080),  # 鑲嵌菱形斜邊玻璃特寫（稜鏡折射彩光）
}


def fit(img, tw, th, fv=0.5, fh=0.5):
    r = max(tw / img.width, th / img.height)
    im = img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS)
    l = int(round((im.width - tw) * fh))
    t = int(round((im.height - th) * fv))
    return im.crop((l, t, l + tw, t + th))


def brighten(img, gain=1.0, gamma=1.0):
    """線性增益 + gamma 提亮（gamma < 1 拉中間調，高光不易爆掉）"""
    import numpy as np
    a = np.array(img).astype(np.float32) / 255.0
    a = (a ** gamma) * gain
    return Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8))


def bake_scrim(img, start=0.28, mid=0.50, k_mid=0.40, k_bot=0.30):
    """先把下半部烤暗，讓之後疊上去的白字有對比。

    卡片產生器自己疊的暗階從 0.44h 才開始、在 0.47h 只降 12%，
    所以標題正好落在最亮的地方（實測：白字壓在發光魚群上讀不清楚）。
    """
    import numpy as np
    h = img.height
    k = np.ones(h, np.float32)
    for y in range(h):
        r = y / h
        if r <= start:
            kk = 1.0
        elif r <= mid:
            kk = 1.0 + (k_mid - 1.0) * (r - start) / (mid - start)
        else:
            kk = k_mid + (k_bot - k_mid) * (r - mid) / (1 - mid)
        k[y] = kk
    arr = np.array(img).astype(np.float32) * k[:, None, None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))


# 卡片第 5 頁主視覺：這張特寫原圖偏暗（金屬框吃掉中間調），
# 提亮到能看見玻璃紋理與稜鏡彩光，但底部暗階不能一起提亮，否則白字會糊掉。
CARD5_GAIN, CARD5_GAMMA = 1.08, 0.92
CARD5_SCRIM = dict(start=0.30, mid=0.55, k_mid=0.58, k_bot=0.46)


def main():
    for out, spec in PLAN.items():
        src, fv, fh, max_w = spec[:4]
        src_crop = spec[4] if len(spec) > 4 else None
        im = Image.open(SRC / src).convert("RGB")
        if src_crop:
            x1, y1, x2, y2 = src_crop
            im = im.crop((x1, y1, min(x2, im.width), min(y2, im.height)))
            print(f"    ↳ {out} 先切掉來源後製框 → {im.size}")
        if out.startswith("card"):
            tw = min(CARD_W, max_w)
            th = round(tw * 4 / 3)
        elif out.startswith("gallery"):
            # 方形縮圖：不要放大超過原圖短邊，避免糊掉
            side = min(max_w, im.width, im.height)
            tw = th = side
        else:
            tw = min(WEB_W, max_w)
            th = round(tw * 3 / 4)
        res = fit(im, tw, th, fv, fh)
        if out == "card5_hero.jpg":
            res = brighten(res, CARD5_GAIN, CARD5_GAMMA)
            res = bake_scrim(res, **CARD5_SCRIM)
        up = tw / im.width
        res.save(HERE / out, "JPEG", quality=90, optimize=True)
        warn = "  ⚠ 放大超過 1.45x" if up > 1.45 else ""
        print(f"✓ {out:16s} {im.size} → {res.size}  x{up:.2f}{warn}")


if __name__ == "__main__":
    main()
