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


def glass_art(sz=(W, H)):
    """玻璃質感替代視覺（尚未有實拍照時）"""
    img = gradient(sz, (20, 34, 48), (40, 74, 88))
    lay = layer(sz)
    d = ImageDraw.Draw(lay)
    for i, x in enumerate(range(-260, W + 340, 150)):
        d.line([(x, H), (x + 520, 0)], fill=(255, 255, 255, 20), width=30 - (i % 4) * 6)
    for i, x in enumerate(range(-120, W + 300, 220)):
        d.line([(x, H), (x + 300, 0)], fill=(196, 131, 90, 16), width=16)
    return over(img, lay.filter(ImageFilter.GaussianBlur(10)))


def photo_or_none(name):
    p = ROOT / name
    if not p.exists():
        return None
    im = Image.open(p).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def poster(path_out, art, name, en="", role="", slogan=(), pager="1 / 6",
           name_size=120, name_y=700, show_quote=True):
    img = art
    img = bottom_mask(img, start=int(H * 0.44))
    lay = layer((W, H))
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

    y = name_y + int(name_size * 1.12) * len(name.split("\n")) + 6
    if role:
        d.text((80, y), role, font=font(REG, 40), fill=BEIGE + (240,)); y += 62
    if show_quote and slogan:
        d.text((80, y + 8), "“", font=font(BOLD, 96), fill=COPPER + (255,)); y += 96
    for line in slogan:
        d.text((80, y), line, font=font(BOLD, 78), fill=WHITE + (255,)); y += 96

    img = over(img, lay)

    # 頁碼膠囊（底部置中、米白 80%）
    pw, ph = 160, 50
    px, py = (W - pw) // 2, 1320
    lay2 = layer((W, H))
    ImageDraw.Draw(lay2).rounded_rectangle([px, py, px + pw, py + ph], radius=25,
                                           fill=BEIGE + (204,))
    img = over(img, lay2)
    d2 = ImageDraw.Draw(img)
    fo2 = font(REG, 26)
    d2.text((px + (pw - fo2.getlength(pager)) / 2, py + 9), pager, font=fo2, fill=NAVY)

    img.save(path_out, "JPEG", quality=90, optimize=True)
    return path_out


def card1(pager="1 / 6"):
    ph = photo_or_none("photo.jpg")
    if ph:
        art = bottom_mask(ph, start=int(H * 0.42), strength=0.9)
    else:
        art = gradient((W, H), (26, 38, 54), (52, 74, 92))
        art = placeholder(art, (330, 150, W - 90, 660), "形象照（3:4 直式）")
    return poster(OUT / "card1.jpg", art, "李柏融", en="Benson",
                  role="友泰京玻璃工程　執行長",
                  slogan=("讓藝術融入玻璃，", "讓隔熱成為空間美學"), pager=pager,
                  name_size=118, name_y=690)


def card5(pager="5 / 6"):
    art = glass_art()
    return poster(OUT / "card5.jpg", art, "品質落在實處", en="",
                  role="工藝藏在細節，滿足高標準設計",
                  slogan=("藝術工藝 · 機能選材", "精準加工 · 施工細節"), pager=pager,
                  name_size=96, name_y=700, show_quote=False)


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
    for mk, n in ((card1, 1), (card5, 5)):
        print("✓", mk(f"{n} / 6").name)
    print("✓", make_og().name)
