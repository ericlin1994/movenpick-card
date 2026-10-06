#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
莫凡彼沙發工藝｜7 張輪播卡圖 + og 分享圖 產生器
------------------------------------------------
產出 img/card1.jpg ~ img/card7.jpg（1040x676，LINE hero 20:13）與 og.jpg（1200x630）

用法：python gen_cards.py
之後 Steve 給了正式形象照／工藝照，直接換掉 img/ 裡的檔案即可（檔名不變）。
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1040, 676
OUT = pathlib.Path(__file__).with_name("img")
OUT.mkdir(exist_ok=True)

FONT_DIR = pathlib.Path(r"C:\Windows\Fonts")
BOLD = str(FONT_DIR / "msjhbd.ttc")
REG  = str(FONT_DIR / "msjh.ttc")

NAVY_TOP, NAVY_BOT = (15, 27, 51), (34, 53, 92)
GOLD, GOLD_2 = (201, 162, 39), (227, 200, 120)
WHITE, GREY, BROWN = (255, 255, 255), (200, 210, 228), (185, 122, 71)


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
    d.text((x, y), "M O V E N P I C K", font=f(BOLD, 26), fill=GOLD_2)
    d.text((x, y + 38), "莫凡彼沙發工藝", font=f(REG, 24), fill=GREY)


def draw_pager(d, idx, total=7):
    label = f"{idx} / {total}"
    font = f(BOLD, 26)
    tw = font.getlength(label)
    x2, y2 = W - 46, H - 40
    x1, y1 = x2 - tw - 40, y2 - 46
    d.rounded_rectangle([x1, y1, x2, y2], radius=23, fill=(255, 255, 255, 28))
    d.text((x1 + 20, y1 + 8), label, font=font, fill=WHITE)


def make_card(idx, title, sub, bullets, accent=None):
    img = gradient((W, H), NAVY_TOP, NAVY_BOT)
    glow(img, (int(W * 0.85), int(H * -0.1)), 420, GOLD, 70)
    d = ImageDraw.Draw(img, "RGBA")
    draw_brand(d)

    y = 190
    if idx == 1:                       # 主卡：標語為主
        d.text((56, y), "“", font=f(BOLD, 90), fill=GOLD_2)
        y += 70
        for ln in wrap(title, f(BOLD, 62), W - 130):
            d.text((56, y), ln, font=f(BOLD, 62), fill=WHITE); y += 82
        y += 8
        for ln in wrap(sub, f(REG, 34), W - 130):
            d.text((56, y), ln, font=f(REG, 34), fill=GOLD_2); y += 46
    else:
        for ln in wrap(title, f(BOLD, 50), W - 130):
            d.text((56, y), ln, font=f(BOLD, 50), fill=WHITE); y += 66
        if sub:
            y += 6
            for ln in wrap(sub, f(REG, 30), W - 130):
                d.text((56, y), ln, font=f(REG, 30), fill=GOLD_2); y += 42
        y += 14
        d.line([(56, y), (W - 56, y)], fill=(255, 255, 255, 45), width=2)
        y += 20
        for b in bullets:
            for i, ln in enumerate(wrap(b, f(REG, 27), W - 140)):
                d.text((56 + (0 if i == 0 else 26), y), ("· " + ln) if i == 0 else ln,
                       font=f(REG, 27), fill=GREY)
                y += 36
            y += 6
            if y > H - 90:
                break

    draw_pager(d, idx)
    p = OUT / f"card{idx}.jpg"
    img.save(p, "JPEG", quality=88, optimize=True)
    return p


CARDS = [
    ("生活沒有標準尺寸，沙發也不該只有標準答案", "沙發訂製　·　展售批發　·　專業諮詢", []),
    ("我們專為這些人打造沙發", "新成屋｜換屋族｜豪宅｜設計師｜商業空間｜家具通路",
     ["沙發坐起來不舒服，久坐腰酸背痛", "尺寸不合，空間總是差一點點",
      "想換皮革／布料／顏色卻不知道怎麼選", "找不到符合風格又耐用的沙發",
      "設計師提案需要特殊尺寸款式", "坐感可客製：柔軟／適中／扎實自由選擇"]),
    ("我們能為你做什麼", "從需求到落地，一次搞定",
     ["沙發訂製　尺寸·材質·坐感", "展售批發　現場體驗·合作供應", "專業諮詢　配置·選材·需求評估"]),
    ("為什麼選擇 莫凡彼？", "40+年三代經驗｜200+合作通路｜100,000+組｜800坪自有廠",
     ["01 需求　了解空間／需求、使用習慣", "02 選材　皮革、布料、填充、五金",
      "03 設計　設計討論", "04 製造　台灣工廠、精工製造", "05 交付　專人安裝、售後服務"]),
    ("好坐感，來自我們對細節的堅持", "嚴選牛皮｜實木骨架｜高密度泡棉｜台灣製椅腳",
     ["嚴選牛皮　細緻柔韌、透氣耐用，越坐越舒適", "實木骨架　結構穩固耐用，使用壽命更長",
      "高密度泡棉　多層結構、支撐性佳，久坐不易塌陷", "台灣製椅腳　穩固耐重、不易晃動"]),
    ("Google 真實案例與好評", "精選 Google 評論",
     ["吳ＯＯ ★★★★★", "　和親友都一同選擇莫凡彼的沙發！老闆專業且耐心溝通，做工質感都非常好！",
      "Amber ★★★★★", "　質感很好的沙發！從參觀到下訂都講解得很詳細；小狗喜歡，主人也喜歡。"]),
    ("想換沙發卻不知道怎麼選？", "我幫你免費初步評估最適合你的沙發",
     ["拍下你的空間照片 ＋ 尺寸，LINE 傳給我", "電話　03-397-2191",
      "地址　桃園市龜山區大湖路249號", "　　　林口長庚　近警察大學"]),
]


def make_og():
    img = gradient((1200, 630), NAVY_TOP, NAVY_BOT)
    glow(img, (1020, -60), 520, GOLD, 80)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((80, 70), "M O V E N P I C K", font=f(BOLD, 30), fill=GOLD_2)
    d.text((80, 116), "莫凡彼沙發工藝", font=f(REG, 28), fill=GREY)
    d.text((80, 210), "吳明憲  Steve", font=f(BOLD, 78), fill=WHITE)
    d.text((80, 310), "莫凡彼沙發工藝　負責人", font=f(REG, 36), fill=GREY)
    d.line([(80, 380), (1120, 380)], fill=(255, 255, 255, 50), width=2)
    d.text((80, 410), "生活沒有標準尺寸", font=f(BOLD, 54), fill=GOLD_2)
    d.text((80, 480), "沙發也不該只有標準答案", font=f(BOLD, 54), fill=WHITE)
    d.text((80, 560), "沙發訂製・展售・批發・諮詢　03-397-2191", font=f(REG, 28), fill=GREY)
    p = pathlib.Path(__file__).with_name("og.jpg")
    img.save(p, "JPEG", quality=90, optimize=True)
    return p


if __name__ == "__main__":
    for i, (t, s, b) in enumerate(CARDS, 1):
        print("✓", make_card(i, t, s, b).name)
    print("✓", make_og().name)
