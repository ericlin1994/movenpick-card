#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜Hero 卡圖產生器（Gemini 設計規格 C 節實作）
------------------------------------------------
畫布 1040x676（LINE hero 20:13）、安全邊距 56px、原點左上
共同元素：左上品牌字、右下頁碼膠囊、可選右上大字浮水印
用法：python gen_cards.py
Benson 給了真實照片後，把 img/cardN.jpg 換掉即可（檔名不變），或改這裡的 PHOTOS。
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1040, 676
MARGIN = 56
OUT = pathlib.Path(__file__).with_name("img")
OUT.mkdir(exist_ok=True)

F = pathlib.Path(r"C:\Windows\Fonts")
BOLD, REG = str(F / "msjhbd.ttc"), str(F / "msjh.ttc")

PRIMARY, SECOND, ACCENT = (14, 42, 58), (46, 125, 143), (184, 134, 11)
DARK_T, DARK_B = (9, 30, 44), (20, 62, 78)
WHITE, CYAN_L = (255, 255, 255), (155, 215, 228)

# 真實照片放這裡就會自動套用（沒有檔案時用程式生成的替代視覺）
PHOTOS = {1: "photo.jpg", 5: "craft1.jpg", 6: "case1.jpg"}


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(size, top, bot, horizontal=False):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    n = w if horizontal else h
    for i in range(n):
        k = i / max(1, n - 1)
        col = tuple(int(top[j] + (bot[j] - top[j]) * k) for j in range(3))
        if horizontal:
            d.line([(i, 0), (i, h)], fill=col)
        else:
            d.line([(0, i), (w, i)], fill=col)
    return img


def layer(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def overlay(img, lay):
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def pill(img, text, x2=None, y2=None, fill=(0, 0, 0, 128), fg=WHITE, pad=40, height=48):
    """右下頁碼膠囊（圓角 16px、黑 50%）"""
    fo = font(REG, 24)
    tw = fo.getlength(text)
    w, h = int(tw + pad), height
    x2 = x2 if x2 is not None else W - MARGIN
    y2 = y2 if y2 is not None else H - MARGIN
    lay = layer((W, H))
    ImageDraw.Draw(lay).rounded_rectangle([x2 - w, y2 - h, x2, y2], radius=16, fill=fill)
    lay = overlay(img, lay)
    d = ImageDraw.Draw(lay)
    d.text((x2 - w + pad / 2, y2 - h + 10), text, font=fo, fill=fg)
    return lay


def brand(img, label_en="TC FEZ GLASS", label_zh="友泰京玻璃工程", color=WHITE, alpha=235):
    lay = layer((W, H))
    d = ImageDraw.Draw(lay)
    d.text((MARGIN, MARGIN - 8), label_en, font=font(BOLD, 32), fill=color + (alpha,))
    d.text((MARGIN, MARGIN + 34), label_zh, font=font(REG, 22), fill=CYAN_L + (200,))
    return overlay(img, lay)


def watermark(img, text, size=80, pos="right-top", alpha=52, color=WHITE, cx=None, cy=None):
    lay = layer((W, H))
    d = ImageDraw.Draw(lay)
    fo = font(BOLD, size)
    tw = fo.getlength(text)
    if cx is not None and cy is not None:
        d.text((cx - tw / 2, cy - size / 2), text, font=fo, fill=color + (alpha,))
    elif pos == "right-top":
        d.text((W - MARGIN - tw, MARGIN - 10), text, font=fo, fill=color + (alpha,))
    elif pos == "left-bottom":
        d.text((MARGIN, H - MARGIN - size - 6), text, font=fo, fill=color + (alpha,))
    else:
        d.text((MARGIN, H - MARGIN - size - 6), text, font=fo, fill=color + (alpha,))
    return overlay(img, lay)


def photo_or_none(idx):
    p = OUT.parent / PHOTOS[idx] if idx in PHOTOS else None
    if p and p.exists():
        im = Image.open(p).convert("RGB")
        ratio = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * ratio), int(im.height * ratio)), Image.LANCZOS)
        left = (im.width - W) // 2
        top = (im.height - H) // 2
        return im.crop((left, top, left + W, top + H))
    return None


def dark_gradient_mask(img, strength=0.72):
    """底部往上疊黑色漸層，確保疊字對比（Gemini C-1）"""
    lay = layer((W, H))
    d = ImageDraw.Draw(lay)
    for y in range(H):
        a = 0 if y < 338 else int(255 * strength * (y - 338) / (H - 338))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    return overlay(img, lay)


def glass_texture(size=(W, H), base=DARK_B, streaks=True):
    """無照片時的玻璃質感替代視覺"""
    img = gradient(size, DARK_T, base)
    if streaks:
        lay = layer(size)
        d = ImageDraw.Draw(lay)
        for i, x in enumerate(range(-200, W + 300, 130)):
            d.line([(x, H), (x + 420, 0)], fill=(255, 255, 255, 16), width=26 - (i % 4) * 5)
        lay = lay.filter(ImageFilter.GaussianBlur(9))
        img = overlay(img, lay)
    return img


def placeholder_box(img, box, label):
    """預留照片位置：虛線框 + 標籤"""
    lay = layer((W, H))
    d = ImageDraw.Draw(lay)
    x1, y1, x2, y2 = box
    for x in range(x1, x2, 26):
        d.line([(x, y1), (min(x + 14, x2), y1)], fill=(255, 255, 255, 120), width=3)
        d.line([(x, y2), (min(x + 14, x2), y2)], fill=(255, 255, 255, 120), width=3)
    for y in range(y1, y2, 26):
        d.line([(x1, y), (x1, min(y + 14, y2))], fill=(255, 255, 255, 120), width=3)
        d.line([(x2, y), (x2, min(y + 14, y2))], fill=(255, 255, 255, 120), width=3)
    fo = font(BOLD, 28)
    tw = fo.getlength(label)
    d.text(((x1 + x2 - tw) / 2, (y1 + y2) / 2 - 16), label, font=fo, fill=(255, 255, 255, 175))
    return overlay(img, lay)


# ═══════════ 各卡視覺（Gemini C-3） ═══════════
def card1(pg="1 / 6"):
    img = gradient((W, H), (9, 30, 44), (20, 62, 78))
    img = brand(img)
    img = placeholder_box(img, (500, 140, W - MARGIN, H - 158), "形象照")
    img = watermark(img, "HANDCRAFT", size=76, alpha=30, pos="left-bottom")
    return pill(img, pg)


def card2(pg="2 / 6"):
    img = glass_texture()
    img = watermark(img, "PAIN POINTS", size=96, cx=W / 2, cy=H / 2 + 30, alpha=26, color=WHITE)
    img = brand(img)
    img = watermark(img, "GLASS", size=76, alpha=30)
    return pill(img, pg)


def card3(pg="3 / 6"):
    img = Image.new("RGB", (W, H), PRIMARY)
    d = ImageDraw.Draw(img)
    quads = [(0, 0, SECOND), (W // 2, 0, PRIMARY),
             (0, H // 2, ACCENT), (W // 2, H // 2, (26, 74, 88))]
    labels = ["藝術玻璃", "空間玻璃", "工程整合", "外牆高空作業"]
    for (x, y, col), lab in zip(quads, labels):
        d.rectangle([x, y, x + W // 2, y + H // 2], fill=col)
    img = brand(img, color=WHITE, alpha=245)
    lay = layer((W, H))
    dl = ImageDraw.Draw(lay)
    for (x, y, _), lab in zip(quads, labels):
        fo = font(BOLD, 30)
        dl.text((x + MARGIN - 8, y + H // 2 - 70), lab, font=fo, fill=(255, 255, 255, 210))
    img = overlay(img, lay)
    return pill(img, pg)


def card4(pg="4 / 6"):
    img = gradient((W, H), (10, 26, 38), PRIMARY)
    img = watermark(img, "30+", size=240, cx=W / 2, cy=H / 2 + 14, alpha=210, color=ACCENT)
    img = brand(img)
    img = watermark(img, "SINCE 1990s", size=70, alpha=32)
    return pill(img, pg)


def card5(pg="5 / 6"):
    ph = photo_or_none(5)
    if ph is not None:
        img = dark_gradient_mask(ph, 0.55)
    else:
        img = glass_texture(base=(38, 86, 102))
        img = watermark(img, "照片待補", size=52, cx=W / 2, cy=H / 2 + 40, alpha=110)
    img = brand(img)
    img = watermark(img, "CRAFT", size=76, alpha=30)
    return pill(img, pg)


def card6(pg="6 / 6"):
    ph = photo_or_none(6)
    if ph is not None:
        img = overlay(ph, layer((W, H)) and Image.new("RGBA", (W, H), PRIMARY + (128,)))
    else:
        img = gradient((W, H), PRIMARY, (16, 52, 66))
        lay = layer((W, H))
        d = ImageDraw.Draw(lay)
        for y in range(0, H, 52):
            d.line([(0, y), (W, y)], fill=(255, 255, 255, 14), width=1)
        for x in range(0, W, 52):
            d.line([(x, 0), (x, H)], fill=(255, 255, 255, 14), width=1)
        img = overlay(img, lay)
        img = watermark(img, "施工照待補", size=52, cx=W / 2, cy=H / 2 + 40, alpha=110)
    img = brand(img)
    return pill(img, pg)


MAKERS = [card1, card2, card3, card4, card5, card6]


def make_og():
    w, h = 1200, 630
    img = gradient((w, h), DARK_T, DARK_B)
    lay = layer((w, h))
    d = ImageDraw.Draw(lay)
    d.ellipse([w - 520, -260, w + 260, 380], fill=CYAN_L + (40,))
    img = overlay(img, lay.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(img)
    d.text((80, 66), "TC FEZ GLASS", font=font(BOLD, 30), fill=CYAN_L)
    d.text((80, 112), "友泰京玻璃工程", font=font(REG, 26), fill=(200, 218, 226))
    d.text((80, 200), "李柏融  Benson Lee", font=font(BOLD, 76), fill=WHITE)
    d.text((80, 296), "友泰京玻璃工程　執行長", font=font(REG, 32), fill=(200, 218, 226))
    d.line([(80, 366), (1120, 366)], fill=(255, 255, 255, 60), width=2)
    d.text((80, 396), "讓藝術融入玻璃", font=font(BOLD, 52), fill=(217, 180, 74))
    d.text((80, 464), "讓隔熱成為空間美學", font=font(BOLD, 52), fill=WHITE)
    d.text((80, 548), "藝術玻璃・空間玻璃・工程整合・外牆高空作業　0938-111-822",
           font=font(REG, 27), fill=(200, 218, 226))
    p = pathlib.Path(__file__).with_name("og.jpg")
    img.save(p, "JPEG", quality=90, optimize=True)
    return p


if __name__ == "__main__":
    for i, mk in enumerate(MAKERS, 1):
        img = mk(f"{i} / {len(MAKERS)}")
        p = OUT / f"card{i}.jpg"
        img.convert("RGB").save(p, "JPEG", quality=88, optimize=True)
        print("✓", p.name)
    print("✓", make_og().name)
