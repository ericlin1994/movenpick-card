#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜LINE 電子名片 Flex Message 產生器 v3
------------------------------------------------
風格：雜誌海報感（3:4 直式 Hero 烤字）+ 精品配色（深藍 / 玫瑰銅 / 奶油白）
設計來源：Gemini 第二版 Design Tokens（精品工程）
用法：python build_flex.py
"""
import json, pathlib, urllib.parse

IMG = "https://ericlin1994.github.io/movenpick-card/img"
LIFF_URL = "https://liff.line.me/2011897701-TrLfDuwi"
ADDR = "新北市中和區連城路518巷8號"
LINKS = {
    "line":  "https://line.me/ti/p/@fez86488989",
    "line2": "https://line.me/ti/p/~benson911",
    "ig":    "https://www.instagram.com/tc_fez_glass_team/",
    "fb":    "https://www.facebook.com/profile.php?id=100079776776531",
    "tel":   "tel:+886938111822",
    "map":   "https://www.google.com/maps/search/?api=1&query="
             + urllib.parse.quote("友泰京玻璃工程 " + ADDR),
    "share": LIFF_URL + "?share=1&v=2026-10-07-0700",
}

# ═══════════ Design Tokens（精品工程版） ═══════════
NAVY   = "#253043"   # 主底色 深邃海軍藍
NAVY_D = "#1E2838"   # 卡片內層深色
COPPER = "#C4835A"   # 強調色 玫瑰銅
BEIGE  = "#F5F1E8"   # 介面底色 奶油米白
WHITE  = "#FFFFFF"
MUTED  = "#A0AAB8"   # 深底上的次要文字
DIVIDE = "#DCD4C5"   # 米白底上的分隔線

# padding / cornerRadius 用 px（cornerRadius 支援關鍵字，但 px 最不會出錯）


def t(s, size="xs", weight="regular", color=WHITE, wrap=True, margin=None,
      align=None, flex=None):
    o = {"type": "text", "text": s, "size": size, "weight": weight, "color": color, "wrap": wrap}
    if margin: o["margin"] = margin
    if align: o["align"] = align
    if flex is not None: o["flex"] = flex
    return o


def box(contents, layout="vertical", spacing="md", margin=None, padding=None, bg=None,
        radius=None, flex=None, border=None, align_items=None, action=None):
    o = {"type": "box", "layout": layout, "contents": contents, "spacing": spacing}
    if margin: o["margin"] = margin
    if padding: o["paddingAll"] = padding
    if bg: o["backgroundColor"] = bg
    if radius: o["cornerRadius"] = radius
    if flex is not None: o["flex"] = flex
    if border: o["borderWidth"] = border[0]; o["borderColor"] = border[1]
    if align_items: o["alignItems"] = align_items
    if action: o["action"] = action
    return o


def _mk(contents):
    """允許 box(a, b, c) 或 box([a, b, c]) 兩種寫法"""
    if len(contents) == 1 and isinstance(contents[0], list):
        return contents[0]
    return list(contents)


def vbox(*contents, spacing="md", **k): return box(_mk(contents), spacing=spacing, **k)
def hbox(*contents, spacing="sm", **k):
    return box(_mk(contents), layout="horizontal", spacing=spacing, **k)
def sep(margin="md", color=DIVIDE): return {"type": "separator", "margin": margin, "color": color}


def pill(label, uri, bg, fg=WHITE):
    """圓角膠囊按鈕：用 box + action 做（LINE 預設 button 無法自訂圓角與底色）。
    標籤要短、字級 xxs、允許換行——三顆膠囊各佔 1/3 寬，字太長會被裁掉。"""
    return box([t(label, size="xxs", weight="bold", color=fg, align="center", wrap=True)],
               spacing="none", padding="10px", bg=bg, radius="100px", flex=1,
               action={"type": "uri", "label": label[:20], "uri": uri})


def control_row():
    """共用底部操作區：米白圓角底 + 三顆膠囊（IG / LINE / 導航）"""
    return box([hbox(pill("📷 IG 作品", LINKS["ig"], NAVY),
                     pill("💬 LINE", LINKS["line"], COPPER),
                     pill("📍 導航", LINKS["map"], NAVY), spacing="sm")],
               spacing="none", padding="10px", bg=BEIGE, radius="20px")


def tag_pill(label):
    return box([t(label, size="xxs", weight="bold", color=WHITE, align="center", wrap=False)],
               spacing="none", padding="8px", radius="100px", flex=1,
               border=("1px", COPPER))


# ═══════════ 逐卡 body ═══════════
def body1():
    """雜誌封面款：主文案烤進 Hero 圖；body 保留一行保險文字 + 操作列"""
    return vbox([t("友泰京玻璃工程　藝術玻璃・空間玻璃・工程整合・外牆高空作業",
                   size="xxs", color=MUTED, margin="none"),
                 control_row()], spacing="md", padding="14px", bg=NAVY)


def body2():
    aud = ["設計師", "建築師", "建商", "營造", "商空", "住宅"]
    pains = ["大圖輸出缺工藝，難達藝術質感",
             "玻璃鐵件分包，尺寸收邊難整合",
             "設計圖美，卻找不到廠家實作",
             "特殊彎曲或異材質，找不到方案",
             "兼顧採光與隔熱，不知如何選材"]
    return vbox([
        t("我們專為誰服務", size="xl", weight="bold", color=COPPER, margin="none"),
        vbox([hbox(*[tag_pill(x) for x in aud[:3]], spacing="xs"),
              hbox(*[tag_pill(x) for x in aud[3:]], spacing="xs")], spacing="xs", margin="md"),
        box([t("你是不是也遇過這些問題？", size="xs", weight="bold", color=NAVY, margin="none"),
             sep("sm", DIVIDE)] +
            [hbox(t("📌", size="xs", color=COPPER, flex=1, wrap=False),
                  t(p, size="xs", color=NAVY, flex=6, margin="none"), spacing="sm",
                  margin="sm")
             for p in pains],
            spacing="sm", padding="18px", bg=BEIGE, radius="20px", margin="md"),
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body3():
    svcs = [("🎨", "藝術玻璃", "工藝與色彩結合"), ("🪟", "空間玻璃", "美感實用隔間窗"),
            ("🏗️", "工程整合", "鋁框鐵件一條龍"), ("🧗", "高空作業", "外牆檢測與防水")]
    def cell(ic, name, desc):
        return box([t(ic, size="md", color=COPPER, margin="none", wrap=False),
                    t(name, size="sm", weight="bold", color=WHITE, margin="sm", wrap=False),
                    t(desc, size="xs", color=MUTED, margin="xs")],
                   spacing="none", padding="16px", bg=NAVY_D, radius="16px", flex=1)
    return vbox([
        t("我們能為你做什麼", size="xl", weight="bold", color=COPPER, margin="none"),
        t("從設計規劃到現場施作，實現空間想像", size="sm", color=WHITE, margin="xs"),
        hbox(cell(*svcs[0]), cell(*svcs[1]), spacing="md", margin="md"),
        hbox(cell(*svcs[2]), cell(*svcs[3]), spacing="md", margin="md"),
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body4():
    stats = [("30+", "年玻璃產業\n服務經驗"), ("3", "代工藝傳承\n品質保證"), ("4", "大服務項目\n專業整合")]
    return vbox([
        t("為什麼選擇友泰京？", size="xl", weight="bold", color=COPPER, margin="none"),
    ] + [hbox(t(big, size="4xl", weight="bold", color=COPPER, flex=2, wrap=False),
              t(small, size="sm", weight="bold", color=WHITE, flex=3, margin="none"),
              spacing="md", align_items="center", margin="xl" if i == 0 else "md")
         for i, (big, small) in enumerate(stats)] + [
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body5():
    """工藝：主文案烤進 3:4 Hero 圖；body 保留一行保險文字 + 操作列"""
    return vbox([t("藝術工藝・機能選材・精準加工・施工細節",
                   size="xxs", color=MUTED, margin="none"),
                 control_row()], spacing="md", padding="14px", bg=NAVY)


def body6():
    def row(ic, txt, size="sm", weight="bold", color=WHITE):
        return hbox(t(ic, size="sm", color=COPPER, flex=1, wrap=False),
                    t(txt, size=size, weight=weight, color=color, flex=6, margin="none"),
                    spacing="sm", margin="sm")
    return vbox([
        t("讓我們聊聊你的空間", size="xl", weight="bold", color=NAVY, margin="none"),
        t("拍下現場照片＋尺寸，LINE 傳給我免費評估", size="xs", weight="bold", color=COPPER, margin="xs"),
        box([row("📞", "0938-111-822"),
             row("💬", "LINE：@fez86488989"),
             row("📍", "新北市中和區連城路518巷8號（中和高中旁巷）", size="xs", weight="regular"),
             row("⏰", "週一～五 08:00-17:00", size="xs", weight="regular")],
            spacing="sm", padding="18px", bg=NAVY, radius="20px", margin="md"),
        control_row(),
    ], spacing="md", padding="18px", bg=BEIGE)


BODIES = [body1, body2, body3, body4, body5, body6]
HEROES = {1: f"{IMG}/card1.jpg", 5: f"{IMG}/card5.jpg"}   # 只有這兩張有 3:4 Hero
BG_COLOR = {1: NAVY, 2: NAVY, 3: NAVY, 4: NAVY, 5: NAVY, 6: BEIGE}
TITLES = ["李柏融  Benson Lee", "我們專為誰服務", "我們能為你做什麼",
          "為什麼選擇友泰京？", "品質落在實處", "讓我們聊聊你的空間"]
SUMMARIES = [
    ["李柏融 Benson Lee｜執行長", "讓藝術融入玻璃，讓隔熱成為空間美學"],
    ["我們專為誰服務", "設計師｜建築師｜建商｜營造｜商空｜業主",
     "大圖輸出缺工藝，難達藝術質感", "玻璃鐵件分包，尺寸收邊難整合",
     "設計圖美，卻找不到廠家實作", "特殊彎曲或異材質，找不到方案", "兼顧採光與隔熱，不知如何選材"],
    ["我們能為你做什麼", "藝術玻璃 工藝與色彩結合", "空間玻璃 美感實用隔間窗",
     "工程整合 鋁框鐵件一條龍", "高空作業 外牆檢測與防水"],
    ["為什麼選擇友泰京？", "30+ 年玻璃產業服務經驗", "3 代工藝傳承", "4 大服務項目"],
    ["品質落在實處", "玻璃光影特寫（文案烤進圖內）"],
    ["讓我們聊聊你的空間", "電話 0938-111-822", "LINE @fez86488989",
     "新北市中和區連城路518巷8號", "週一～五 08:00-17:00"],
]


def build_bubble(i):
    b = {
        "type": "bubble", "size": "mega",
        # 深色卡片背景用 bubble styles（官方做法），body 區塊才會整片滿版
        "styles": {"body": {"backgroundColor": BG_COLOR[i]}},
        "body": BODIES[i - 1](),
    }
    if i in HEROES:
        b["hero"] = {"type": "image", "url": HEROES[i], "size": "full",
                     "aspectRatio": "3:4", "aspectMode": "cover",
                     "action": {"type": "uri", "label": "開啟名片", "uri": LIFF_URL}}
    return b


# ═══════════ 備援版（結構最簡） ═══════════
def build_candidate(with_hero: bool):
    bubbles = []
    for i in range(6):
        n = i + 1
        body = vbox([t(TITLES[i], size="sm", weight="bold", color=WHITE, margin="none"),
                     t("\n".join("· " + s for s in SUMMARIES[i]), size="xs", color=MUTED, margin="xs")],
                    spacing="none")
        b = {"type": "bubble", "styles": {"body": {"backgroundColor": NAVY}}, "body": body,
             "footer": vbox([box([t("LINE 諮詢", size="xs", weight="bold", color=WHITE,
                                    align="center", wrap=False)], padding="12px", bg=COPPER,
                                 radius="100px", action={"type": "uri", "label": "LINE 諮詢",
                                                         "uri": LINKS["line"]})],
                            spacing="none", padding="12px", bg=NAVY)}
        if with_hero and n in HEROES:
            b["hero"] = {"type": "image", "url": HEROES[n], "size": "full",
                         "aspectRatio": "3:4", "aspectMode": "cover"}
        bubbles.append(b)
    return {"type": "flex", "altText": ("F2 有圖版" if with_hero else "F1 無圖版"),
            "contents": {"type": "carousel", "contents": bubbles}}


def inject_into_page(payload_json: str):
    import re
    page = pathlib.Path(__file__).with_name("index.html")
    html = page.read_text(encoding="utf-8")
    s_mark = "/* ═══════ FLEX_PAYLOAD_START"
    e_mark = "/* ═══════ FLEX_PAYLOAD_END"
    i, j = html.index(s_mark), html.index(e_mark)
    line_end = html.index("\n", i) + 1
    html = html[:line_end] + "const INLINE_FLEX = " + payload_json + ";\n" + html[j:]
    html = re.sub(r"(const BUILD = 'b)(\d+)(')",
                  lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", html, count=1)
    page.write_text(html, encoding="utf-8")
    print("已內嵌進 index.html，頁面大小", len(html.encode()), "bytes")


def inject_candidates():
    import subprocess, sys
    here = pathlib.Path(__file__).parent
    for name, payload in (("f1", build_candidate(False)), ("f2", build_candidate(True))):
        p = here / f"{name}.json"
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        r = subprocess.run([sys.executable, str(here / "validate_flex.py"), str(p)],
                           capture_output=True, text=True, encoding="utf-8")
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode != 0:
            raise SystemExit("候選版本結構驗證失敗，中止部署")
    page = here / "index.html"
    html = page.read_text(encoding="utf-8")
    s, e = "/* ═══════ F_CANDIDATE_START", "/* ═══════ F_CANDIDATE_END"
    i, j = html.index(s), html.index(e)
    line_end = html.index("\n", i) + 1
    js = "const INLINE_F1 = " + json.dumps(build_candidate(False), ensure_ascii=False, separators=(",", ":")) + ";\n"
    js += "const INLINE_F2 = " + json.dumps(build_candidate(True), ensure_ascii=False, separators=(",", ":")) + ";\n"
    page.write_text(html[:line_end] + js + html[j:], encoding="utf-8")
    print("已注入 F1（無圖）／F2（有圖）到 index.html")


def main():
    bubbles = [build_bubble(n) for n in range(1, 7)]
    payload = {"type": "flex", "altText": "友泰京玻璃工程｜李柏融 Benson 電子名片",
               "contents": {"type": "carousel", "contents": bubbles}}
    out = pathlib.Path(__file__).with_name("flex-cards.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"寫出 {out}　卡片數 = {len(bubbles)}　{out.stat().st_size} bytes")
    inject_into_page(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    inject_candidates()


if __name__ == "__main__":
    main()
