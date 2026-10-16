#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3:4 直式海報 Hero 圖產生器（多客戶版）
------------------------------------------------
畫布 1080x1440（LINE aspectRatio 3:4）、座標原點左上
文字直接「烤」進圖中（卡片 1、5 的 body 不放文案）

換客戶只改 client.json（brand / theme / images 三段），不要改本檔。
用法：python gen_cards.py
執行長形象照放 photo.jpg 進 repo 根目錄就會自動置入（否則顯示虛線預留框）。
"""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).parent
CLIENT = json.loads((HERE / "client.json").read_text(encoding="utf-8"))
B = CLIENT["brand"]
C = CLIENT["contact"]
TH = CLIENT["theme"]
IMG = CLIENT["images"]

W, H = 1080, 1440
OUT = HERE / "img"
OUT.mkdir(exist_ok=True)
ROOT = HERE

F = pathlib.Path(r"C:\Windows\Fonts")
BOLD, REG = str(F / "msjhbd.ttc"), str(F / "msjh.ttc")
EMOJI = str(F / "seguiemj.ttf")   # 彩色 emoji（烤圖用；Flex 端是 LINE 自己畫的）


def rgb(hexstr):
    s = hexstr.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


LOGO = B.get("logo")                 # client.json: brand.logo（白色去背 PNG，選用）
LOGO_W = int(B.get("logo_width", 440))
LOGO_W_OG = int(B.get("logo_width_og", 380))
LOGO_SCRIM = float(B.get("logo_scrim", 0.5))   # 左上角局部壓暗強度（0 = 不壓）


def brand_lockup(im, x=80, y=80, width=None):
    """左上角品牌鎖定圖：client.json 有 brand.logo 就貼白色 logo，
    否則退回文字版（英文名＋中文名）。回傳底部 y，方便後續排版。

    貼之前先在左上角壓一層柔和的暗階：白色 logo 疊在實拍照上時，
    遇到亮部（反光玻璃、天空）會整片糊掉，這層 scrim 是為了讓它穩定可讀。"""
    w = width or LOGO_W
    if LOGO_SCRIM > 0:
        sc = Image.new("RGBA", im.size, (0, 0, 0, 0))
        rx, ry, blur = int(w * 1.9), int(w * 1.2), int(w * 0.3)
        ImageDraw.Draw(sc).ellipse([-rx // 2 + x, -ry // 2 + y, x + rx, y + ry],
                                   fill=NAVY_D + (int(255 * LOGO_SCRIM),))
        im.alpha_composite(sc.filter(ImageFilter.GaussianBlur(blur)))
    if LOGO and (ROOT / LOGO).exists():
        lg = Image.open(ROOT / LOGO).convert("RGBA")
        lg = lg.resize((w, max(1, round(lg.height * w / lg.width))), Image.LANCZOS)
        im.alpha_composite(lg, (x, y))
        return y + lg.height
    d = ImageDraw.Draw(im)
    d.text((x, y), B["en"], font=font(BOLD, 34), fill=WHITE + (245,))
    d.text((x, y + 44), B["name"], font=font(REG, 26), fill=BEIGE + (240,))
    return y + 72


def lighten(c, k):  # k=0 原色、k=1 純白
    return tuple(int(c[i] + (255 - c[i]) * k) for i in range(3))


NAVY, NAVY_D = rgb(TH["NAVY"]), rgb(TH["NAVY_D"])
COPPER, BEIGE = rgb(TH["COPPER"]), rgb(TH["BEIGE"])
WHITE, MUTED = rgb(TH["WHITE"]), rgb(TH["MUTED"])
DIVIDE = rgb(TH["DIVIDE"])
HERO_TOP, HERO_BOT = rgb(TH["HERO_GRAD"][0]), rgb(TH["HERO_GRAD"][1])
OG_TOP, OG_BOT = rgb(TH["OG_GRAD"][0]), rgb(TH["OG_GRAD"][1])


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


def poster(path_out, art, name, en="", role="", slogan=(),
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
    brand_lockup(lay, 80, 80)

    # 人名 + 英文名
    fo = font(BOLD, name_size)
    for i, line in enumerate(name.split("\n")):
        y = name_y + i * int(name_size * 1.12)
        d.text((80, y), line, font=fo, fill=WHITE + (255,))
        if en and i == 0:
            d.text((80 + fo.getlength(line) + 26, y + int(name_size * 0.42)),
                   en, font=font(BOLD, int(name_size * 0.5)), fill=lighten(COPPER, 0.5) + (255,))

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

    img.save(path_out, "JPEG", quality=90, optimize=True)
    return path_out


# ═══════════ 內容海報（第 2／3／4 張）═══════════
# LINE Flex 的 box 背景只支援 linearGradient，沒有圖片背景（官方 spec 確認），
# 所以「實拍照當卡片底」只能在烤進圖裡做：把標題與內容排在這張實拍底圖上。
# 字級 = Flex 字級 × 3.6（Flex 卡寬約 300px，畫布 1080px）。
FLEX = CLIENT["flex"]
S3 = {"xxs": 36, "xs": 43, "sm": 50, "md": 58, "lg": 65, "xl": 72, "4xl": 115}
# 壓在實拍照上的銅金要提亮一階：原 COPPER(#C4835A) 在暗底上對比不足（實測偏濁）
COPPER_T = lighten(COPPER, 0.32)
CELL_LINE = lighten(NAVY_D, 0.22)   # 深色卡片在暗底上會糊掉，加一圈淡邊分離


def rr(lay, x, y, w, h, fill=None, outline=None, width=0, radius=40):
    ImageDraw.Draw(lay).rounded_rectangle([x, y, x + w, y + h], radius=radius,
                                          fill=fill, outline=outline, width=width)


def wrap_lines(d, s, fo, maxw):
    lines, cur = [], ""
    for ch in s:
        if d.textlength(cur + ch, font=fo) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def content_poster(out_path, art, layout, canvas_h=H):
    h = canvas_h
    img = art.convert("RGB")
    lay = layer((W, h))
    d = ImageDraw.Draw(lay)
    brand_lockup(lay, 80, 80)

    def head(txt, sub=""):
        y = 250
        d.text((80, y), txt, font=font(BOLD, S3["xl"]), fill=COPPER_T + (255,))
        y += int(S3["xl"] * 1.55)
        if sub:
            d.text((80, y), sub, font=font(REG, S3["sm"]), fill=WHITE + (255,))
            y += int(S3["sm"] * 1.5)
        return y + 36

    if layout == "pains":
        y = head(FLEX["titles"][1])
        pw, gap = (W - 160 - 2 * 26) // 3, 26
        for r in range(2):
            for i in range(3):
                x = 80 + i * (pw + gap)
                rr(lay, x, y, pw, 96, outline=COPPER_T + (255,), width=4, radius=48)
                lab = FLEX["audiences"][r * 3 + i]
                fo = font(BOLD, S3["xxs"])
                d.text((x + (pw - fo.getlength(lab)) / 2, y + 30), lab, font=fo, fill=WHITE + (255,))
            y += 96 + 20
        y += 44
        ph = 152 + len(FLEX["pains"]) * 108
        rr(lay, 80, y, W - 160, ph, fill=BEIGE + (255,), radius=40)
        d.text((120, y + 46), FLEX["pain_title"], font=font(BOLD, S3["xs"]), fill=NAVY + (255,))
        d.line([(120, y + 116), (W - 120, y + 116)], fill=DIVIDE + (255,), width=3)
        ty = y + 148
        for p in FLEX["pains"]:
            d.text((120, ty), "📌", font=font(EMOJI, S3["xs"]), fill=COPPER + (255,),
                   embedded_color=True)
            d.text((196, ty), p, font=font(REG, S3["xs"]), fill=NAVY + (255,))
            ty += 108

    elif layout == "services":
        y = head(FLEX["services_title"], FLEX["services_sub"])
        cw, gap = (W - 160 - 36) // 2, 36
        for r in range(2):
            for i in range(2):
                s = FLEX["services"][r * 2 + i]
                x = 80 + i * (cw + gap)
                rr(lay, x, y, cw, 380, fill=NAVY_D + (240,),
                   outline=CELL_LINE + (255,), width=3, radius=32)
                d.text((x + 44, y + 44), s["icon"], font=font(EMOJI, S3["lg"]),
                       fill=COPPER + (255,), embedded_color=True)
                d.text((x + 44, y + 176), s["name"], font=font(BOLD, S3["sm"]), fill=WHITE + (255,))
                d.text((x + 44, y + 258), s["desc"], font=font(REG, S3["xs"]), fill=MUTED + (255,))
            y += 380 + 40

    elif layout == "stats":
        y = head(f"{FLEX['why_prefix']}{B['short_name']}？") + 20
        for s in FLEX["stats"]:
            rr(lay, 80, y, W - 160, 268, fill=NAVY_D + (240,),
               outline=CELL_LINE + (255,), width=3, radius=32)
            d.text((130, y + 62), s["big"], font=font(BOLD, S3["4xl"]), fill=COPPER_T + (255,))
            bx = 130 + int(S3["4xl"] * 1.9)
            for i, ln in enumerate(s["small"].split("\n")):
                d.text((bx, y + 88 + i * int(S3["sm"] * 1.5)), ln,
                       font=font(BOLD, S3["sm"]), fill=WHITE + (255,))
            y += 268 + 56
    else:
        raise SystemExit(f"✗ 未知的 layout：{layout}")

    img = over(img, lay)
    img.save(out_path, "JPEG", quality=90, optimize=True)
    return out_path


def render(p, h=H, out=None, name_y=None):
    """依 client.json 的 images.posters 設定產生一張海報
    name_y：比例 0~1，優先序 參數 → p["name_y"] → None（poster 預設 0.47）"""
    if name_y is None:
        name_y = p.get("name_y")
    if p["art"] == "bg":
        bg = photo_or_none(p.get("photo", "card_bg.jpg"), h)
        art = bg if bg else gradient((W, h), HERO_TOP, HERO_BOT)
        return content_poster(OUT / (out or p["out"]), art, p["layout"], h)
    if p["art"] == "photo":
        ph = photo_or_none(p.get("photo", "photo.jpg"), h)
        if ph:
            art = bottom_mask(ph, start=int(h * 0.42), strength=0.9)
        else:
            art = gradient((W, h), HERO_TOP, HERO_BOT)
            art = placeholder(art, (330, int(h * 0.10), W - 90, int(h * 0.46)),
                              p.get("placeholder", "形象照"))
    else:
        art = glass_art((W, h))
    return poster(OUT / (out or p["out"]), art, p["name"], en=p.get("en", ""),
                  role=p.get("role", ""), slogan=tuple(p.get("slogan", [])),
                  name_size=int(p["name_size"] * (h / H) ** 0.6),
                  name_y=int(h * name_y) if name_y is not None else None,
                  show_quote=p.get("show_quote", True), canvas_h=h)


def make_og():
    w, h = 1200, 630
    img = gradient((w, h), OG_TOP, OG_BOT)
    lay = layer((w, h))
    d = ImageDraw.Draw(lay)
    d.ellipse([w - 560, -300, w + 300, 420], fill=COPPER + (60,))
    img = over(img, lay.filter(ImageFilter.GaussianBlur(100)))
    d = ImageDraw.Draw(img)
    img = img.convert("RGBA")
    brand_lockup(img, 80, 60, width=LOGO_W_OG)
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((80, 196), B["owner_display"], font=font(BOLD, 76), fill=WHITE)
    d.text((80, 292), B["role"], font=font(REG, 32), fill=MUTED)
    d.line([(80, 362), (1120, 362)], fill=COPPER + (220,), width=2)
    d.text((80, 392), f"{B['slogan1']}，", font=font(BOLD, 50), fill=COPPER)
    d.text((80, 456), B["slogan2"], font=font(BOLD, 50), fill=WHITE)
    d.text((80, 545), f"{B['services_line']}　{C['phone']}",
           font=font(REG, 26), fill=MUTED)
    p = ROOT / IMG["og"]["out"]
    img.save(p, "JPEG", quality=90, optimize=True)
    return p


if __name__ == "__main__":
    for p in IMG["posters"]:
        print("✓", render(p).name, f"（第 {p['page']} 張）")
    for v in IMG["variants"]:
        base = next(p for p in IMG["posters"] if p["page"] == v["page"])
        print("✓", render(base, h=v["h"], out=v["out"], name_y=v.get("name_y")).name, "（較矮版）")
    print("✓", make_og().name)
