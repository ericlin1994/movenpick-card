#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜LINE 電子名片 Flex Message 產生器
------------------------------------------------
產出 flex-cards.json  →  給 liff.shareTargetPicker() 用的輪播卡

用法：python build_flex.py
改內容：只改下面 IMG / LIFF_URL / LINKS / CARDS 四塊
"""
import json, pathlib, urllib.parse

# ══════════════════════════════════════════════════════
# 1) 圖片網址（部署後把圖丟進同一個 repo，改這裡就好）
#    尺寸 1040x676（20:13），LINE 會自動裁切
# ══════════════════════════════════════════════════════
IMG = "https://ericlin1994.github.io/movenpick-card/img"
CARDS_N = 6
IMAGES = [f"{IMG}/card{i}.jpg" for i in range(1, CARDS_N + 1)]

# 2) 連結
LIFF_URL = "https://liff.line.me/2011897701-TrLfDuwi"  # LIFF app ID
ADDR = "新北市中和區連城路518巷8號"
LINKS = {
    # 全部必須是合法 URI（不能有空格或全形括號，否則 LINE 會判 invalid message）
    "line":  "https://line.me/ti/p/@fez86488989",                       # 官方帳號
    "line2": "https://line.me/ti/p/~benson911",                          # 個人帳號（備用）
    "ig":    "https://www.instagram.com/tc_fez_glass_team/",
    "fb":    "https://www.facebook.com/profile.php?id=100079776776531",
    "tel":   "tel:+886938111822",
    "map":   "https://www.google.com/maps/search/?api=1&query="
             + urllib.parse.quote("友泰京玻璃工程 " + ADDR),
    # 分享鈕帶版本參數：每次改版都會換網址，順便破掉 LINE 內建瀏覽器的頁面快取
    "share": LIFF_URL + "?share=1&v=2026-10-07-0500",
}

# 3) 卡片文案（Benson 2026-10-07 提供）
CARDS = [
    dict(
        title="李柏融  Benson Lee",
        sub="友泰京玻璃工程　執行長",
        body=[
            ("quote", "讓藝術融入玻璃，讓隔熱成為空間美學"),
            ("quote2", "以藝術玻璃工藝，打造節能舒適新視界"),
            ("tag", "藝術玻璃　·　空間玻璃　·　工程整合　·　外牆高空作業"),
        ],
    ),
    dict(
        title="我們專為誰服務",
        sub="設計師｜建築師｜建商｜營造｜商業空間｜住宅業主",
        body=[
            ("head", "你是不是也遇過這些狀況？"),
            ("li", "想做有質感的藝術玻璃，卻只拿到大圖輸出的方案，缺少工藝層次"),
            ("li", "玻璃與鐵件扶手由不同廠商施作，尺寸、固定與收邊難以整合"),
            ("li", "設計圖很漂亮，卻找不到能實際製作與施工的玻璃廠商"),
            ("li", "特殊造型、彎曲或異材質搭配，詢問多家仍找不到合適方案"),
            ("li", "希望玻璃兼顧美感、採光與隔熱，卻不知道該如何選材"),
            ("li", "玻璃種類與報價差異大，難以判斷品質及工法是否符合需求"),
            ("foot", "中了其中一項，歡迎直接找我聊聊！"),
        ],
    ),
    dict(
        title="我們能為你做什麼",
        sub="從設計規劃到現場施作，實現空間想像",
        body=[
            ("head", "藝術玻璃"),
            ("li", "結合工藝、色彩與光影，為住宅、商業空間及建築打造獨特的玻璃作品"),
            ("head", "空間玻璃"),
            ("li", "依空間需求規劃玻璃隔間、門窗、淋浴拉門與欄杆，兼顧美感與實用機能"),
            ("head", "工程整合"),
            ("li", "整合玻璃、鋁框與鐵件，從丈量、加工到安裝，讓尺寸、固定與收邊完整到位"),
            ("head", "外牆高空作業"),
            ("li", "提供外牆檢測、修繕、防水及矽膠更新，依現場條件規劃高空作業方式"),
        ],
    ),
    dict(
        title="為什麼選擇 友泰京？",
        sub="30+ 年產業經驗｜第三代工藝傳承｜4 大服務整合",
        body=[
            ("head", "30+ 年｜玻璃產業服務經驗"),
            ("li", "累積藝術玻璃與各式玻璃工程的實務經驗"),
            ("head", "第三代｜玻璃工藝傳承"),
            ("li", "延續工藝底蘊，結合現代設計與空間需求"),
            ("head", "4 大服務｜完整專業整合"),
            ("li", "藝術玻璃、空間玻璃、工程整合與外牆高空作業"),
            ("head", "從需求到交付，五步完成"),
            ("multi", "01 需求確認　了解設計想法、使用需求與預算\n"
                      "02 場勘丈量　確認現場尺寸、結構及施工條件\n"
                      "03 方案定案　確認玻璃選材、工法、樣品與報價\n"
                      "04 製作安裝　依確認方案加工，整合玻璃、鋁框與鐵件\n"
                      "05 驗收交付　確認成品、收邊與使用功能，提供保養建議"),
        ],
    ),
    dict(
        title="工藝藏在細節，品質落在實處",
        sub="藝術工藝｜機能選材｜精準加工｜施工細節",
        body=[
            ("head", "藝術工藝｜光影層次"),
            ("li", "依設計需求運用鑲嵌、紋理與複合工藝，呈現玻璃的立體層次與光影美感"),
            ("head", "機能選材｜美感兼顧實用"),
            ("li", "依使用情境搭配安全玻璃、Low-E 或中空複合結構，兼顧美感與機能需求"),
            ("head", "精準加工｜實現特殊設計"),
            ("li", "透過細緻丈量與客製加工，讓特殊尺寸、彎曲造型及異材質搭配符合設計需求"),
            ("head", "施工細節｜整合完整到位"),
            ("li", "重視玻璃、鋁框與鐵件的固定、接合及矽膠收邊，讓成品穩固、俐落且便於維護"),
        ],
    ),
    dict(
        title="讓我們聊聊你的空間",
        sub="拍下現場照片 ＋ 尺寸，LINE 傳給我，免費初步評估",
        body=[
            ("head", "友泰京玻璃工程"),
            ("li", "電話　0938-111-822"),
            ("li", "地址　" + ADDR),
            ("li", "　　　（中和高中旁巷）"),
            ("li", "營業時間　週一～五 08:00-17:00"),
            ("li", "LINE　" + LINKS["line"].replace("https://", "")),
            ("foot", "藝術玻璃・空間玻璃・工程整合・外牆高空作業"),
        ],
    ),
]

NAVY, ACCENT, SEP = "#0E2A3A", "#2E7D8F", "#DCEAEE"


def txt(t, size="sm", color="#3C4658", weight="regular", wrap=True, margin="sm", align="start"):
    return {"type": "text", "text": t, "size": size, "color": color,
            "weight": weight, "wrap": wrap, "margin": margin, "align": align}


def build_body(card):
    """只吐 2～3 個文字元件（內文全部塞進一個用 \\n 換行的 text）。
    PITFALL: 每個 bubble 塞十幾個 text 元件時曾出現問題；壓縮＋換行符號內容一字不少。"""
    out = [txt(card["title"], size="lg", color=NAVY, weight="bold", margin="none")]
    if card.get("sub"):
        out.append(txt(card["sub"], size="xs", color="#6B7280", margin="sm"))
    out.append({"type": "separator", "margin": "md", "color": SEP})
    for kind, t in card["body"]:
        if kind == "quote":
            out.append(txt(t, size="lg", color=NAVY, weight="bold", margin="md"))
        elif kind == "quote2":
            out.append(txt(t, size="sm", color=ACCENT, weight="bold", margin="xs"))
        elif kind == "tag":
            out.append(txt(t, size="xs", color="#6B7280", margin="md"))
        elif kind == "head":
            out.append(txt(t, size="sm", color=NAVY, weight="bold", margin="md"))
        elif kind == "li":
            out.append(txt("· " + t, size="xs", color="#4A5468", margin="xs"))
        elif kind == "multi":
            out.append(txt(t, size="xs", color="#4A5468", margin="xs"))
        elif kind == "foot":
            out.append(txt(t, size="xs", color=ACCENT, weight="bold", margin="md"))
    return out


def btn(label, uri, bg, fg="#FFFFFF"):
    """只留 style + color。
    PITFALL: 加上 height / margin / scaling 會讓 shareTargetPicker 回報成功、
    但整則訊息在對方聊天室完全不顯示（實測於 2026-10，已用二分法定位）。"""
    return {"type": "button", "style": "primary", "color": bg,
            "action": {"type": "uri", "label": label, "uri": uri}}


def build_bubble(i, card):
    """PITFALL：bubble 少了 "type": "bubble" 就是無效 Flex——LINE 會回報成功但完全不顯示。"""
    return {
        "type": "bubble", "size": "mega",
        "hero": {"type": "image", "url": IMAGES[i], "size": "full",
                 "aspectRatio": "20:13", "aspectMode": "cover",
                 "action": {"type": "uri", "label": "開啟名片", "uri": LIFF_URL}},
        "body": {"type": "box", "layout": "vertical", "spacing": "none",
                 "paddingAll": "16px", "contents": build_body(card)},
        "footer": {"type": "box", "layout": "vertical", "spacing": "sm",
                   "paddingAll": "12px", "contents": [
                       {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                           btn("LINE 諮詢", LINKS["line"], ACCENT),
                           btn("IG 作品", LINKS["ig"], NAVY),
                           btn("導航門市", LINKS["map"], NAVY) ]},
                       {"type": "button", "style": "secondary",
                        "action": {"type": "uri", "label": "分享給好友", "uri": LINKS["share"]}} ]},
    }


def inject_into_page(payload_json: str):
    """把 payload 內嵌進 index.html，並把 BUILD 版號 +1。
    內嵌的理由：LINE 內建瀏覽器會快取外部 json，導致一直送出舊版卡片。"""
    import re
    page = pathlib.Path(__file__).with_name("index.html")
    html = page.read_text(encoding="utf-8")
    s_mark, e_mark = "/* ═══════ FLEX_PAYLOAD_START", "/* ═══════ FLEX_PAYLOAD_END"
    i, j = html.index(s_mark), html.index(e_mark)
    line_end = html.index("\n", i) + 1
    html = (html[:line_end]
            + "const INLINE_FLEX = " + payload_json + ";\n"
            + html[j:])
    html = re.sub(r"(const BUILD = 'b)(\d+)(')",
                  lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", html, count=1)
    page.write_text(html, encoding="utf-8")
    print("已內嵌進 index.html，頁面大小", len(html.encode()), "bytes")


def _lines(card):
    out = []
    for kind, t in card["body"]:
        if kind == "head":
            out.append("【" + t + "】")
        elif kind == "li":
            out.append("· " + t)
        else:
            out.append(t)
    return "\n".join(out)


def build_candidate(with_hero: bool):
    """備援版：兩行文字 body ＋ footer 三顆基本樣式按鈕（垂直排列）。"""
    bubbles = []
    for i, card in enumerate(CARDS):
        body = [{"type": "text", "text": card["title"], "weight": "bold", "color": NAVY},
                {"type": "text", "text": _lines(card), "size": "xs", "color": "#4A5468", "wrap": True}]
        if card.get("sub"):
            body.insert(1, {"type": "text", "text": card["sub"], "size": "xs", "color": "#6B7280", "wrap": True})
        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "contents": body},
            "footer": {"type": "box", "layout": "vertical", "contents": [
                {"type": "button", "style": "primary", "action": {"type": "uri", "label": "LINE 諮詢", "uri": LINKS["line"]}},
                {"type": "button", "style": "primary", "action": {"type": "uri", "label": "IG 作品", "uri": LINKS["ig"]}},
                {"type": "button", "style": "primary", "action": {"type": "uri", "label": "導航門市", "uri": LINKS["map"]}},
            ]},
        }
        if with_hero:
            bubble["hero"] = {"type": "image", "url": IMAGES[i], "size": "full",
                              "aspectRatio": "20:13", "aspectMode": "cover"}
        bubbles.append(bubble)
    return {"type": "flex", "altText": ("F2 有圖版" if with_hero else "F1 無圖版"),
            "contents": {"type": "carousel", "contents": bubbles}}


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
    bubble_cards = [build_bubble(i, c) for i, c in enumerate(CARDS)]
    payload = {"type": "flex", "altText": "友泰京玻璃工程｜李柏融 Benson 電子名片",
               "contents": {"type": "carousel", "contents": bubble_cards}}
    out = pathlib.Path(__file__).with_name("flex-cards.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"寫出 {out}　卡片數 = {len(bubble_cards)}　{out.stat().st_size} bytes")
    inject_into_page(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    inject_candidates()


if __name__ == "__main__":
    main()
