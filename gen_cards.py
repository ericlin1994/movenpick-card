#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜3:4 直式海報 Hero 圖產生器（精品工程版）
------------------------------------------------
畫布 1080x1440（LINE aspectRatio 3:4）、座標原點左上
文字直接「烤」進圖中（卡片 1、5 的 body 不放文案）
用法：python gen_cards.py
執行長形象照放 photo.jpg 進 repo 根目錄就會自動置入（否則顯示虛線預留框）。
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1440
OUT = pathlib.Path(__file__).with_name("img")
OUT.mkdir(exist_ok=True)
ROOT = pathlib.Path(__file__).parent

F = pathlib.Path(r"C:\Windows\Fonts")
BOLD, REG = str(F / "msjhbd.ttc"), str(F / "msjh.ttc")

NAVY, NAVY_D = (37, 48, 67), (30, 40, 56)
COPPER, BEIGE = (196, 131, 90), (245, 241, 232)
WHITE, MUTED = (255, 255, 255), (160, 170, 184)


def font(p, s):
    return ImageFont.truetype(p, s)


def gradient(size, top, bot):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)))
    return img


def layer(size=(W, H)):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def over(img, lay):
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def bottom_mask(img, start=640, strength=0.86, color=(0, 0, 0)):
    """底部往上疊暗色漸層，讓烤上去的文字清楚浮現"""
    lay = layer(img.size)
    d = ImageDraw.Draw(lay)
    for y in range(img.size[1]):
        a = 0 if y < start else int(255 * strength * (y - start) / (img.size[1] - start))
        d.line([(0, y), (img.size[0], y)], fill=color + (a,))
    return over(img, lay)


def placeholder(img, boxrect, label="形象照"):
    lay = layer(img.size)
    d = ImageDraw.Draw(lay)
    x1, y1, x2, y2 = boxrect
    for x in range(x1, x2, 28):
        d.line([(x, y1), (min(x + 15, x2), y1)], fill=(255, 255, 255, 120), width=3)
        d.line([(x, y2), (min(x + 15, x2), y2)], fill=(255, 255, 255, 120), width=3)
    for y in range(y1, y2, 28):
        d.line([(x1, y), (x1, min(y + 15, y2))], fill=(255, 255, 255, 120), width=3)
        d.line([(x2, y), (x2, min(y + 15, y2))], fill=(255, 255, 255, 120), width=3)
    fo = font(BOLD, 34)
    d.text(((x1 + x2 - fo.getlength(label)) / 2, (y1 + y2) / 2 - 18), label, font=fo,
           fill=(255, 255, 255, 170))
    return over(img, lay)


def glass_art(sz=None):
    sz = sz or (W, H)
    """玻璃質感替代視覺（尚未有實拍照時）"""
    img = gradient(sz, (20, 34, 48), (40, 74, 88))
    lay = layer(sz)
    d = ImageDraw.Draw(lay)
    for i, x in enumerate(range(-260, W + 340, 150)):
        d.line([(x, H), (x + 520, 0)], fill=(255, 255, 255, 20), width=30 - (i % 4) * 6)
    for i, x in enumerate(range(-120, W + 300, 220)):
        d.line([(x, H), (x + 300, 0)], fill=(196, 131, 90, 16), width=16)
    return over(img, lay.filter(ImageFilter.GaussianBlur(10)))


def photo_or_none(name, h=H):
    p = ROOT / name
    if not p.exists():
        return None
    im = Image.open(p).convert("RGB")
    r = max(W / im.width, h / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - h) // 2
    return im.crop((l, t, l + W, t + h))


def poster(path_out, art, name, en="", role="", slogan=(), pager="1 / 6",
           name_size=120, name_y=None, show_quote=True, canvas_h=None, size_k=1.0):
    """canvas_h / unit：同一組文案可套在 3:4（1440）與 4:3（810）兩種畫布"""
    h = canvas_h or H
    size_k = size_k * (h / H) ** 0.35   # 矮版字級略縮，避免擠
    if name_y is None:
        name_y = int(h * 0.47)
    img = art
    img = bottom_mask(img, start=int(h * 0.44))
    lay = layer((W, h))
    d = ImageDraw.Draw(lay)

    # 品牌（左上 80,80）
    d.text((80, 80), "TC FEZ GLASS", font=font(BOLD, 34), fill=WHITE + (245,))
    d.text((80, 124), "友泰京玻璃工程", font=font(REG, 26), fill=BEIGE + (240,))

    # 人名 + 英文名
    fo = font(BOLD, name_size)
    for i, line in enumerate(name.split("\n")):
        y = name_y + i * int(name_size * 1.12)
        d.text((80, y), line, font=fo, fill=WHITE + (255,))
        if en and i == 0:
            d.text((80 + fo.getlength(line) + 26, y + int(name_size * 0.42)),
                   en, font=font(BOLD, int(name_size * 0.5)), fill=COPPER + (255,))

    y = name_y + int(name_size * 1.12) * len(name.split("\n")) + int(h * 0.004)
    if role:
        d.text((80, y), role, font=font(REG, int(40 * size_k)), fill=BEIGE + (240,))
        y += int(62 * size_k)
    if show_quote and slogan:
        d.text((80, y + 8), "“", font=font(BOLD, int(96 * size_k)), fill=COPPER + (255,))
        y += int(96 * size_k)
    for line in slogan:
        d.text((80, y), line, font=font(BOLD, int(78 * size_k)), fill=WHITE + (255,))
        y += int(96 * size_k)

    img = over(img, lay)

    # 頁碼膠囊（底部置中、米白 80%）
    pw, ph = 160, 50
    px, py = (W - pw) // 2, int(h - 120)
    lay2 = layer((W, h))
    ImageDraw.Draw(lay2).rounded_rectangle([px, py, px + pw, py + ph], radius=25,
                                           fill=BEIGE + (204,))
    img = over(img, lay2)
    d2 = ImageDraw.Draw(img)
    fo2 = font(REG, 26)
    d2.text((px + (pw - fo2.getlength(pager)) / 2, py + 9), pager, font=fo2, fill=NAVY)

    img.save(path_out, "JPEG", quality=90, optimize=True)
    return path_out


def card1(pager="1 / 6", h=H, out="card1.jpg"):
    ph = photo_or_none("photo.jpg", h)
    if ph:
        art = bottom_mask(ph, start=int(h * 0.42), strength=0.9)
    else:
        art = gradient((W, h), (26, 38, 54), (52, 74, 92))
        art = placeholder(art, (330, int(h * 0.10), W - 90, int(h * 0.46)), "形象照")
    return poster(OUT / out, art, "李柏融", en="Benson",
                  role="友泰京玻璃工程　執行長",
                  slogan=("讓藝術融入玻璃，", "讓隔熱成為空間美學"), pager=pager,
                  name_size=int(118 * (h / H) ** 0.6), canvas_h=h)


def card5(pager="5 / 6", h=H, out="card5.jpg"):
    art = glass_art((W, h))
    return poster(OUT / out, art, "品質落在實處", en="",
                  role="工藝藏在細節，滿足高標準設計",
                  slogan=("藝術工藝 · 機能選材", "精準加工 · 施工細節"), pager=pager,
                  name_size=int(96 * (h / H) ** 0.6), show_quote=False, canvas_h=h)


def make_og():
    w, h = 1200, 630
    img = gradient((w, h), (30, 40, 56), (52, 74, 92))
    lay = layer((w, h))
    d = ImageDraw.Draw(lay)
    d.ellipse([w - 560, -300, w + 300, 420], fill=COPPER + (60,))
    img = over(img, lay.filter(ImageFilter.GaussianBlur(100)))
    d = ImageDraw.Draw(img)
    d.text((80, 66), "TC FEZ GLASS", font=font(BOLD, 32), fill=BEIGE)
    d.text((80, 112), "友泰京玻璃工程", font=font(REG, 26), fill=MUTED)
    d.text((80, 196), "李柏融  Benson Lee", font=font(BOLD, 76), fill=WHITE)
    d.text((80, 292), "友泰京玻璃工程　執行長", font=font(REG, 32), fill=MUTED)
    d.line([(80, 362), (1120, 362)], fill=(196, 131, 90, 220), width=2)
    d.text((80, 392), "讓藝術融入玻璃，", font=font(BOLD, 50), fill=COPPER)
    d.text((80, 456), "讓隔熱成為空間美學", font=font(BOLD, 50), fill=WHITE)
    d.text((80, 545), "藝術玻璃・空間玻璃・工程整合・外牆高空作業　0938-111-822",
           font=font(REG, 26), fill=MUTED)
    p = ROOT / "og.jpg"
    img.save(p, "JPEG", quality=90, optimize=True)
    return p


if __name__ == "__main__":
    print("✓", card1("1 / 6").name, "（3:4）")
    print("✓", card5("5 / 6").name, "（3:4）")
    print("✓", card1("1 / 6", h=810, out="card1_43.jpg").name, "（4:3 較矮）")
    print("✓", card5("5 / 6", h=810, out="card5_43.jpg").name, "（4:3 較矮）")
    print("✓", make_og().name)
