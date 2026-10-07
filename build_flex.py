#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜LINE 電子名片 Flex Message 產生器（Gemini 設計規格實作版）
------------------------------------------------
設計規格：設計規格_給Gemini.md／Gemini 回覆的 Design Tokens + 逐卡結構
用法：python build_flex.py
"""
import json, pathlib, urllib.parse

IMG = "https://ericlin1994.github.io/movenpick-card/img"
CARDS_N = 6
IMAGES = [f"{IMG}/card{i}.jpg" for i in range(1, CARDS_N + 1)]

LIFF_URL = "https://liff.line.me/2011897701-TrLfDuwi"
ADDR = "新北市中和區連城路518巷8號"
LINKS = {
    "line":  "https://line.me/ti/p/@fez86488989",     # 官方帳號
    "line2": "https://line.me/ti/p/~benson911",        # 個人帳號（備用）
    "ig":    "https://www.instagram.com/tc_fez_glass_team/",
    "fb":    "https://www.facebook.com/profile.php?id=100079776776531",
    "tel":   "tel:+886938111822",
    "map":   "https://www.google.com/maps/search/?api=1&query="
             + urllib.parse.quote("友泰京玻璃工程 " + ADDR),
    "share": LIFF_URL + "?share=1&v=2026-10-07-0600",
}

# ═══════════ Design Tokens（Gemini 規格） ═══════════
PRIMARY = "#0E2A3A"   # 主色 深墨藍
SECOND     = "#2E7D8F"   # 輔色 湖水青
ACCENT  = "#B8860B"   # 點綴 暗金
BG      = "#FFFFFF"   # 主白底
BG_ALT  = "#F4F6F8"   # 淺灰底
TEXT    = "#1A1A1A"   # 主內文
MUTED   = "#737D8C"   # 次要
SEP     = "#E2E6EA"   # 分隔線
CYAN_L  = "#9BD7E4"   # 淺青（深底上的副文字）
WHITE   = "#FFFFFF"

# padding / cornerRadius 一律用 px（關鍵字值不在官方規格內，用錯會被 LINE 整則丟掉）


def t(s, size="xs", weight="regular", color=TEXT, wrap=True, margin=None,
      align=None, flex=None, max_lines=None):
    o = {"type": "text", "text": s, "size": size, "weight": weight,
         "color": color, "wrap": wrap}
    if margin: o["margin"] = margin
    if align: o["align"] = align
    if flex is not None: o["flex"] = flex
    if max_lines: o["maxLines"] = max_lines
    return o


def vbox(contents, spacing="sm", margin=None, padding=None, bg=None, radius=None, flex=None,
         align_items=None):
    o = {"type": "box", "layout": "vertical", "contents": contents, "spacing": spacing}
    if margin: o["margin"] = margin
    if padding: o["paddingAll"] = padding
    if bg: o["backgroundColor"] = bg
    if radius: o["cornerRadius"] = radius
    if flex is not None: o["flex"] = flex
    if align_items: o["alignItems"] = align_items
    return o


def hbox(contents, spacing="sm", margin=None, flex=None, align_items=None):
    o = {"type": "box", "layout": "horizontal", "contents": contents, "spacing": spacing}
    if margin: o["margin"] = margin
    if flex is not None: o["flex"] = flex
    if align_items: o["alignItems"] = align_items
    return o


def sep(margin="sm", color=SEP):
    return {"type": "separator", "margin": margin, "color": color}


def tag(label):
    """膠囊標籤：圓角色塊 + 小字"""
    return vbox([t(label, size="xxs", weight="bold", color=PRIMARY, align="center")],
                spacing="none", padding="8px", bg=BG_ALT, radius="6px")


def icon_line(emoji, body, size="xs", color=TEXT, weight="regular", flex=6, wrap=True, margin=None):
    """左 emoji、右文字的一列"""
    return hbox([t(emoji, size="sm", flex=1, align="center"),
                 t(body, size=size, color=color, weight=weight, flex=flex, wrap=wrap)],
                spacing="md", margin=margin)


def btn(label, uri, style="primary", color=None):
    """只留 style / color / action。
    PITFALL：加 height / margin / scaling 會讓 LINE 靜默丟掉整則訊息。"""
    a = {"type": "uri", "label": label, "uri": uri}
    o = {"type": "button", "style": style, "action": a}
    if color: o["color"] = color
    return o


# ═══════════ 逐卡內容（Gemini 設計，文案逐字） ═══════════
def body1():
    return vbox([
        t("李柏融  Benson Lee", size="xl", weight="bold", color=PRIMARY, margin="none"),
        t("友泰京玻璃工程　執行長", size="sm", color=MUTED, margin="xs"),
        sep("md"),
        t("讓藝術融入玻璃，讓隔熱成為空間美學\n以藝術玻璃工藝，打造節能舒適新視界",
          size="xs", weight="bold", color=SECOND, margin="md"),
        vbox([hbox([tag("藝術玻璃"), tag("空間玻璃")], spacing="xs"),
              hbox([tag("工程整合"), tag("外牆高空作業")], spacing="xs")],
             spacing="xs", margin="md"),
    ], spacing="md", padding="18px", bg=BG)


def body2():
    pains = ["大圖輸出缺工藝，難達藝術質感",
             "玻璃鐵件分包，尺寸收邊難整合",
             "設計圖美，卻找不到廠家實作",
             "特殊彎曲或異材質，找不到方案",
             "需兼顧採光隔熱，不知如何選材",
             "報價工法差異大，品質難以判斷"]
    return vbox([
        t("我們專為誰服務", size="lg", weight="bold", color=PRIMARY, margin="none"),
        t("設計師｜建築師｜建商｜營造｜商空｜業主", size="xs", weight="bold", color=ACCENT, margin="xs"),
        sep("sm"),
    ] + [icon_line("⚠️", p, size="xs", color=TEXT, margin=m) for p, m in
         zip(pains, ["md"] + ["sm"] * 5)],
        spacing="sm", padding="18px", bg=BG)


def body3():
    svcs = [("🎨", "藝術玻璃", "結合工藝色彩，打造獨特空間作品"),
            ("🪟", "空間玻璃", "隔間淋浴門窗，兼顧美感與實用"),
            ("🏗️", "工程整合", "玻璃鋁框鐵件，丈量安裝完整到位"),
            ("🧗", "高空作業", "外牆檢測防水，依現場規劃施工")]
    return vbox([
        t("我們能為你做什麼", size="lg", weight="bold", color=PRIMARY, margin="none"),
        t("從設計規劃到現場施作，實現空間想像", size="xs", weight="bold", color=SECOND, margin="xs"),
        vbox([hbox([t(ic, size="sm", flex=1, align="center"),
                    vbox([t(name, size="sm", weight="bold", color=PRIMARY, margin="none"),
                          t(desc, size="xs", color=MUTED, margin="xs")], spacing="none", flex=5)],
                   spacing="sm")
              for ic, name, desc in svcs], spacing="md", margin="md"),
    ], spacing="md", padding="18px", bg=BG_ALT)


def body4():
    stats = [("30+", "年產業經驗\n專業整合"), ("3", "代工藝傳承\n品質保證"), ("4", "大服務項目\n一條龍施作")]
    return vbox([
        t("為什麼選擇 友泰京？", size="lg", weight="bold", color=WHITE, margin="none"),
        t("流程：確認→場勘→定案→製作→交付", size="xs", weight="bold", color=ACCENT, margin="xs"),
        sep("md", SECOND),
    ] + [hbox([t(big, size="xxl", weight="bold", color=WHITE, flex=2, wrap=False),
               t(small, size="sm", weight="bold", color=CYAN_L, flex=3)],
              spacing="md", align_items="center", margin="md")
         for big, small in stats],
        spacing="md", padding="18px", bg=PRIMARY)


def body5():
    items = [("🔹 藝術工藝｜光影層次", "鑲嵌、紋理與複合工藝，呈現立體美感"),
             ("🔹 機能選材｜美感兼顧", "安全玻璃、Low-E 或中空複合結構"),
             ("🔹 精準加工｜施工細節", "彎曲異材質搭配，矽膠收邊俐落穩固")]
    out = [t("品質落在實處", size="lg", weight="bold", color=PRIMARY, margin="none"),
           t("工藝藏在細節，滿足高標準設計", size="xs", color=MUTED, margin="xs"),
           sep("sm")]
    for head, desc in items:
        out.append(sep("sm"))
        out.append(t(head, size="sm", weight="bold", color=SECOND, margin="sm"))
        out.append(t(desc, size="xs", color=TEXT, margin="xs"))
    return vbox(out, spacing="sm", padding="18px", bg=BG)


def body6():
    return vbox([
        t("讓我們聊聊你的空間", size="lg", weight="bold", color=PRIMARY, margin="none"),
        t("拍下現場照片＋尺寸，LINE 傳給我免費評估", size="xs", weight="bold", color=ACCENT, margin="xs"),
        sep("md"),
        icon_line("📞", "0938-111-822", size="sm", weight="bold"),
        icon_line("💬", "LINE：@fez86488989", size="sm", weight="bold"),
        icon_line("⏰", "週一～五 08:00-17:00", size="xs"),
        icon_line("📍", "新北市中和區連城路518巷8號（中和高中旁巷）", size="xs"),
    ], spacing="sm", padding="18px", bg=BG_ALT)


BODIES = [body1, body2, body3, body4, body5, body6]
SUMMARIES = [
    ["李柏融 Benson Lee｜執行長", "讓藝術融入玻璃，讓隔熱成為空間美學", "藝術玻璃・空間玻璃・工程整合・外牆高空作業"],
    ["我們專為誰服務", "設計師｜建築師｜建商｜營造｜商空｜業主",
     "大圖輸出缺工藝，難達藝術質感", "玻璃鐵件分包，尺寸收邊難整合", "設計圖美，卻找不到廠家實作",
     "特殊彎曲或異材質，找不到方案", "需兼顧採光隔熱，不知如何選材", "報價工法差異大，品質難以判斷"],
    ["我們能為你做什麼", "藝術玻璃 結合工藝色彩，打造獨特空間作品", "空間玻璃 隔間淋浴門窗，兼顧美感與實用",
     "工程整合 玻璃鋁框鐵件，丈量安裝完整到位", "高空作業 外牆檢測防水，依現場規劃施工"],
    ["為什麼選擇 友泰京？", "30+ 年產業經驗", "3 代工藝傳承", "4 大服務項目", "流程：確認→場勘→定案→製作→交付"],
    ["品質落在實處", "藝術工藝 鑲嵌紋理複合工藝，呈現立體美感", "機能選材 安全玻璃、Low-E 或中空複合結構",
     "精準加工 彎曲異材質搭配，矽膠收邊俐落穩固"],
    ["讓我們聊聊你的空間", "電話 0938-111-822", "LINE @fez86488989", "週一～五 08:00-17:00",
     "新北市中和區連城路518巷8號（中和高中旁巷）"],
]
TITLES = ["李柏融  Benson Lee", "我們專為誰服務", "我們能為你做什麼",
          "為什麼選擇 友泰京？", "品質落在實處", "讓我們聊聊你的空間"]


def build_bubble(i):
    """PITFALL：bubble 少了 "type": "bubble" 就是無效 Flex。"""
    return {
        "type": "bubble", "size": "mega",
        "hero": {"type": "image", "url": IMAGES[i], "size": "full",
                 "aspectRatio": "20:13", "aspectMode": "cover",
                 "action": {"type": "uri", "label": "開啟名片", "uri": LIFF_URL}},
        "body": BODIES[i](),
        "footer": {"type": "box", "layout": "vertical", "spacing": "sm",
                   "paddingAll": "12px", "contents": [
                       hbox([btn("LINE 諮詢", LINKS["line"], "primary", PRIMARY),
                             btn("IG 作品", LINKS["ig"], "secondary"),
                             btn("導航門市", LINKS["map"], "secondary")], spacing="sm"),
                       btn("分享給好友", LINKS["share"], "link", MUTED) ]},
    }


# ═══════════ 備援版（結構最簡，若正式版有問題時可切換） ═══════════
def build_candidate(with_hero: bool):
    bubbles = []
    for i in range(CARDS_N):
        body = vbox([t(TITLES[i], size="sm", weight="bold", color=PRIMARY, margin="none"),
                     t("\n".join("· " + s for s in SUMMARIES[i]), size="xs", color=TEXT, margin="xs")],
                    spacing="none")
        b = {"type": "bubble", "body": body,
             "footer": vbox([btn("LINE 諮詢", LINKS["line"], "primary"),
                             btn("IG 作品", LINKS["ig"], "primary"),
                             btn("導航門市", LINKS["map"], "primary")], spacing="sm")}
        if with_hero:
            b["hero"] = {"type": "image", "url": IMAGES[i], "size": "full",
                         "aspectRatio": "20:13", "aspectMode": "cover"}
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
    bubbles = [build_bubble(i) for i in range(CARDS_N)]
    payload = {"type": "flex", "altText": "友泰京玻璃工程｜李柏融 Benson 電子名片",
               "contents": {"type": "carousel", "contents": bubbles}}
    out = pathlib.Path(__file__).with_name("flex-cards.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"寫出 {out}　卡片數 = {len(bubbles)}　{out.stat().st_size} bytes")
    inject_into_page(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    inject_candidates()


if __name__ == "__main__":
    main()
