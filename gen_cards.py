#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜輪播卡圖 + og 分享圖 產生器
------------------------------------------------
產出 img/card1.jpg ~ img/card6.jpg（1040x676，LINE hero 20:13）與 og.jpg（1200x630）

用法：python gen_cards.py
Benson 給了正式形象照／工藝照／案例照後，直接換掉 img/ 裡的檔案即可（檔名不變）。
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1040, 676
OUT = pathlib.Path(__file__).with_name("img")
OUT.mkdir(exist_ok=True)

FONT_DIR = pathlib.Path(r"C:\Windows\Fonts")
BOLD = str(FONT_DIR / "msjhbd.ttc")
REG  = str(FONT_DIR / "msjh.ttc")

# 玻璃產業配色：深墨藍→藍綠漸層 + 冷青光暈
TOP, BOT = (9, 30, 44), (20, 62, 78)
GLOW_C = (110, 200, 220)
ACCENT = (108, 205, 222)
WHITE, GREY = (255, 255, 255), (198, 218, 226)


def f(path, size):
    return ImageFont.truetype(path, size)


def gradient(size, top, bot):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img


def glow(img, center, radius, color, alpha=90):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.45))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))


def wrap(text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        NO_START = "。，、！？；：）」』】…"
        if font.getlength(cur + ch) <= max_w or (ch in NO_START and cur):
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_brand(d, x=56, y=44):
    d.text((x, y), "T C  F E Z   G L A S S", font=f(BOLD, 26), fill=ACCENT)
    d.text((x, y + 38), "友泰京玻璃工程", font=f(REG, 24), fill=GREY)


def draw_pager(d, idx, total=6):
    label = f"{idx} / {total}"
    font = f(BOLD, 26)
    tw = font.getlength(label)
    x2, y2 = W - 46, H - 40
    x1, y1 = x2 - tw - 40, y2 - 46
    d.rounded_rectangle([x1, y1, x2, y2], radius=23, fill=(255, 255, 255, 28))
    d.text((x1 + 20, y1 + 8), label, font=font, fill=WHITE)


def make_card(idx, title, sub, bullets):
    img = gradient((W, H), TOP, BOT)
    glow(img, (int(W * 0.86), int(H * -0.12)), 430, GLOW_C, 62)
    glow(img, (int(W * 0.1), int(H * 1.05)), 330, (60, 140, 170), 45)
    d = ImageDraw.Draw(img, "RGBA")
    draw_brand(d)

    y = 186
    if idx == 1:                       # 主卡：姓名 + 職稱 + 標語
        for ln in wrap(title, f(BOLD, 60), W - 130):
            d.text((56, y), ln, font=f(BOLD, 60), fill=WHITE); y += 80
        for ln in wrap(sub, f(REG, 32), W - 130):
            d.text((56, y), ln, font=f(REG, 32), fill=GREY); y += 44
        y += 16
        for b in bullets:
            for ln in wrap(b, f(BOLD, 30), W - 130):
                d.text((56, y), ln, font=f(BOLD, 30), fill=ACCENT); y += 42
    else:
        for ln in wrap(title, f(BOLD, 50), W - 130):
            d.text((56, y), ln, font=f(BOLD, 50), fill=WHITE); y += 64
        if sub:
            y += 4
            for ln in wrap(sub, f(REG, 28), W - 130):
                d.text((56, y), ln, font=f(REG, 28), fill=ACCENT); y += 40
        y += 14
        d.line([(56, y), (W - 56, y)], fill=(255, 255, 255, 45), width=2)
        y += 20
        for b in bullets:
            for i, ln in enumerate(wrap(b, f(REG, 26), W - 146)):
                d.text((56 + (0 if i == 0 else 26), y), ("· " + ln) if i == 0 else ln,
                       font=f(REG, 26), fill=GREY)
                y += 34
            y += 5
            if y > H - 84:
                break

    draw_pager(d, idx)
    p = OUT / f"card{idx}.jpg"
    img.save(p, "JPEG", quality=88, optimize=True)
    return p


CARDS = [
    ("李柏融  Benson Lee", "友泰京玻璃工程　執行長",
     ["讓藝術融入玻璃，讓隔熱成為空間美學",
      "以藝術玻璃工藝，打造節能舒適新視界",
      "藝術玻璃 · 空間玻璃 · 工程整合 · 外牆高空作業"]),
    ("我們專為誰服務", "設計師｜建築師｜建商｜營造｜商業空間｜住宅業主",
     ["想做有質感的藝術玻璃，卻只拿到大圖輸出的方案，缺少工藝層次",
      "玻璃與鐵件扶手由不同廠商施作，尺寸、固定與收邊難以整合",
      "設計圖很漂亮，卻找不到能實際製作與施工的玻璃廠商",
      "特殊造型、彎曲或異材質搭配，詢問多家仍找不到合適方案",
      "希望玻璃兼顧美感、採光與隔熱，卻不知道該如何選材",
      "玻璃種類與報價差異大，難以判斷品質及工法是否符合需求"]),
    ("我們能為你做什麼", "從設計規劃到現場施作，實現空間想像",
     ["藝術玻璃　結合工藝、色彩與光影，打造獨特的玻璃作品",
      "空間玻璃　隔間、門窗、淋浴拉門與欄杆，兼顧美感與機能",
      "工程整合　整合玻璃、鋁框與鐵件，尺寸、固定與收邊到位",
      "外牆高空作業　外牆檢測、修繕、防水及矽膠更新"]),
    ("為什麼選擇 友泰京？", "30+ 年產業經驗｜第三代工藝傳承｜4 大服務整合",
     ["30+ 年　累積藝術玻璃與各式玻璃工程的實務經驗",
      "第三代　延續工藝底蘊，結合現代設計與空間需求",
      "4 大服務　藝術玻璃、空間玻璃、工程整合、外牆高空作業",
      "五步交付　需求確認→場勘丈量→方案定案→製作安裝→驗收交付"]),
    ("工藝藏在細節，品質落在實處", "藝術工藝｜機能選材｜精準加工｜施工細節",
     ["藝術工藝　鑲嵌、紋理與複合工藝，呈現立體層次與光影美感",
      "機能選材　安全玻璃、Low-E 或中空複合結構，美感兼顧機能",
      "精準加工　特殊尺寸、彎曲造型及異材質搭配符合設計需求",
      "施工細節　固定、接合及矽膠收邊，穩固俐落且便於維護"]),
    ("讓我們聊聊你的空間", "拍下現場照片 ＋ 尺寸，LINE 傳給我，免費初步評估",
     ["電話　0938-111-822",
      "地址　新北市中和區連城路518巷8號（中和高中旁巷）",
      "營業時間　週一～五 08:00-17:00",
      "LINE　@fez86488989　·　IG　tc_fez_glass_team"]),
]


def make_og():
    img = gradient((1200, 630), TOP, BOT)
    glow(img, (1030, -70), 540, GLOW_C, 72)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((80, 66), "T C  F E Z   G L A S S", font=f(BOLD, 30), fill=ACCENT)
    d.text((80, 112), "友泰京玻璃工程", font=f(REG, 28), fill=GREY)
    d.text((80, 206), "李柏融  Benson Lee", font=f(BOLD, 76), fill=WHITE)
    d.text((80, 302), "友泰京玻璃工程　執行長", font=f(REG, 34), fill=GREY)
    d.line([(80, 372), (1120, 372)], fill=(255, 255, 255, 50), width=2)
    d.text((80, 402), "讓藝術融入玻璃", font=f(BOLD, 52), fill=ACCENT)
    d.text((80, 470), "讓隔熱成為空間美學", font=f(BOLD, 52), fill=WHITE)
    d.text((80, 552), "藝術玻璃・空間玻璃・工程整合・外牆高空作業　0938-111-822",
           font=f(REG, 27), fill=GREY)
    p = pathlib.Path(__file__).with_name("og.jpg")
    img.save(p, "JPEG", quality=90, optimize=True)
    return p


if __name__ == "__main__":
    for i, (t, s, b) in enumerate(CARDS, 1):
        print("✓", make_card(i, t, s, b).name)
    print("✓", make_og().name)
