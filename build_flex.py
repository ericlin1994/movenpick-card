#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
莫凡彼沙發工藝｜LINE 電子名片 Flex Message 產生器
------------------------------------------------
產出 flex-cards.json  →  給 liff.shareTargetPicker() 用的 7 張輪播卡

用法：python build_flex.py
改內容：只改下面 IMG / LIFF_URL / LINKS / CARDS 四塊
"""
import json, pathlib

# ══════════════════════════════════════════════════════
# 1) 圖片網址（部署後把圖丟進同一個 repo，改這裡就好）
#    尺寸建議 1040x1040 或 1200x780，LINE 會自動裁切
# ══════════════════════════════════════════════════════
IMG = "https://ericlin1994.github.io/movenpick-card/img"
IMAGES = [
    f"{IMG}/card1.jpg",   # 主卡：吳明憲 Steve 形象照
    f"{IMG}/card2.jpg",   # 我們專為這些人打造沙發
    f"{IMG}/card3.jpg",   # 我們能為你做什麼
    f"{IMG}/card4.jpg",   # 為什麼選擇莫凡彼
    f"{IMG}/card5.jpg",   # 好坐感，來自細節的堅持
    f"{IMG}/card6.jpg",   # Google 真實案例與好評
    f"{IMG}/card7.jpg",   # 想換沙發卻不知道怎麼選
]

# 2) 連結（改成 Steve 的真實連結）
LIFF_URL = "https://liff.line.me/2011897701-TrLfDuwi"  # LIFF app ID
LINKS = {
    "site": "https://【官網網址】",
    "line": "https://line.me/ti/p/~【個人LINE ID】",   # 個人帳號用 ~；官方帳號是 @
    "map":  "https://www.google.com/maps/search/?api=1&query="
            "%E8%8E%AB%E5%87%A1%E5%BD%BC%E7%85%89%E7%99%BC%E5%B7%A5%E8%97%9D",
}

# 3) 7 張卡的文案（照原圖逐字）
CARDS = [
    dict(
        title="吳明憲  Steve",
        sub="莫凡彼沙發工藝　負責人",
        body=[
            ("quote", "生活沒有標準尺寸"),
            ("quote2", "沙發也不該只有標準答案"),
            ("tag", "沙發訂製　·　展售批發　·　專業諮詢"),
        ],
    ),
    dict(
        title="我們專為這些人打造沙發",
        sub="新成屋｜換屋族｜豪宅｜設計師｜商業空間｜家具通路",
        body=[
            ("head", "你是不是也有這些困擾？"),
            ("li", "沙發坐起來不舒服，久坐腰酸背痛"),
            ("li", "尺寸不合，空間總是差一點點"),
            ("li", "想換皮革／布料／顏色卻不知道怎麼選"),
            ("li", "找不到符合風格又耐用的沙發"),
            ("li", "設計師提案需要特殊尺寸款式"),
            ("li", "坐感可客製：柔軟／適中／扎實自由選擇"),
            ("foot", "中了其中一項，歡迎直接找我聊聊！"),
        ],
    ),
    dict(
        title="我們能為你做什麼",
        sub="從需求到落地，一次搞定",
        body=[
            ("head", "沙發訂製"),
            ("li", "尺寸 · 材質 · 坐感 — 依空間、身形與使用習慣客製"),
            ("head", "展售批發"),
            ("li", "現場體驗 · 合作供應 — 家具通路與設計產業合作，供貨穩定"),
            ("head", "專業諮詢"),
            ("li", "配置 · 選材 · 需求評估 — 給你清楚實用的建議"),
        ],
    ),
    dict(
        title="為什麼選擇 莫凡彼？",
        sub="40+年三代經驗｜200+合作通路｜100,000+組｜800坪自有廠",
        body=[
            ("head", "從設計到製造，一條龍完成"),
            ("li", "01 需求　了解空間／需求、使用習慣"),
            ("li", "02 選材　皮革、布料、填充、五金"),
            ("li", "03 設計　設計討論"),
            ("li", "04 製造　台灣工廠、精工製造"),
            ("li", "05 交付　專人安裝、售後服務"),
        ],
    ),
    dict(
        title="好坐感，來自我們對細節的堅持",
        sub="嚴選牛皮｜實木骨架｜高密度泡棉｜台灣製椅腳",
        body=[
            ("head", "嚴選牛皮"),
            ("li", "細緻柔韌、透氣耐用，越坐越舒適"),
            ("head", "實木骨架"),
            ("li", "結構穩固耐用，使用壽命更長"),
            ("head", "高密度泡棉"),
            ("li", "多層結構、支撐性佳，久坐不易塌陷"),
            ("head", "台灣製椅腳"),
            ("li", "穩固耐重、不易晃動，細節成就品質"),
        ],
    ),
    dict(
        title="Google 真實案例與好評",
        sub="精選 Google 評論",
        body=[
            ("head", "吳ＯＯ　★★★★★"),
            ("li", "和親友都一同選擇莫凡彼的沙發！老闆專業且耐心溝通，做工質感都非常好！"),
            ("head", "吳ＯＯ　★★★★★"),
            ("li", "價格合理、成品舒適又美觀！老闆解說詳細又親切，能滿足客戶需求。"),
            ("head", "Amber　★★★★★"),
            ("li", "質感很好的沙發！從參觀到下訂都講解得很詳細；小狗喜歡，主人也喜歡。"),
        ],
    ),
    dict(
        title="想換沙發卻不知道怎麼選？",
        sub="我幫你免費初步評估最適合你的沙發",
        body=[
            ("head", "拍下你的空間照片 ＋ 尺寸，LINE 傳給我"),
            ("li", "電話　03-397-2191"),
            ("li", "地址　桃園市龜山區大湖路249號"),
            ("li", "　　　林口長庚　近警察大學"),
            ("foot", "沙發訂製・展售・批發・諮詢"),
        ],
    ),
]

NAVY, BROWN = "#16233D", "#A96B3C"


def txt(t, size="sm", color="#3C4658", weight="regular", wrap=True, margin="sm", align="start"):
    return {"type": "text", "text": t, "size": size, "color": color,
            "weight": weight, "wrap": wrap, "margin": margin, "align": align}


def build_body(card):
    """只吐 2～3 個文字元件（內文全部塞進一個用 \n 換行的 text）。
    PITFALL: 每個 bubble 塞十幾個 text 元件時，shareTargetPicker 會回報成功但整則被丟掉；
    壓成 2～3 個元件＋換行符號就正常，內容一字不少。"""
    out = [txt(card["title"], size="lg", color=NAVY, weight="bold", margin="none")]
    if card.get("sub"):
        out.append(txt(card["sub"], size="xs", color="#6B7280", margin="sm"))
    out.append({"type": "separator", "margin": "md", "color": "#E6E0D4"})
    for kind, t in card["body"]:
        if kind == "quote":
            out.append(txt(t, size="xl", color=NAVY, weight="bold", margin="md"))
        elif kind == "quote2":
            out.append(txt(t, size="md", color=BROWN, weight="bold", margin="xs"))
        elif kind == "tag":
            out.append(txt(t, size="xs", color="#6B7280", margin="md"))
        elif kind == "head":
            out.append(txt(t, size="sm", color=NAVY, weight="bold", margin="md"))
        elif kind == "li":
            out.append(txt("· " + t, size="xs", color="#4A5468", margin="xs"))
        elif kind == "foot":
            out.append(txt(t, size="xs", color=BROWN, weight="bold", margin="md"))
    return out


def btn(label, uri, bg, fg="#FFFFFF"):
    """只留 style + color。
    PITFALL: 加上 height / margin / scaling 會讓 shareTargetPicker 回報成功、
    但整則訊息在對方聊天室完全不顯示（實測於 2026-10，已用二分法定位）。"""
    return {"type": "button", "style": "primary", "color": bg,
            "action": {"type": "uri", "label": label, "uri": uri}}


def build_bubble(i, card):
    """PITFALL：bubble 少了 "type": "bubble" 就是無效 Flex——LINE 會回報成功但完全不顯示。
    每次組卡片都要確認這個欄位在。"""
    share = {"type": "button", "style": "secondary",
             "action": {"type": "uri", "label": "分享給好友", "uri": LIFF_URL + "?share=1"}}
    body = [txt(card["title"], size="lg", color=NAVY, weight="bold", margin="none")]
    if card.get("sub"):
        body.append(txt(card["sub"], size="xs", color="#6B7280", margin="sm"))
    lines = []
    for kind, t in card["body"]:
        if kind == "head":
            lines.append("【" + t + "】")
        elif kind == "li":
            lines.append("· " + t)
        else:
            lines.append(t)
    if lines:
        body.append(txt("\n".join(lines), size="xs", color="#4A5468", margin="md"))
    body.append(share)          # 分享鈕放 body（footer 只留三顆，降低風險）
    return {
        "type": "bubble",
        "hero": {"type": "image", "url": IMAGES[i], "size": "full",
                 "aspectRatio": "20:13", "aspectMode": "cover"},
        "body": {"type": "box", "layout": "vertical", "contents": body},
        "footer": {"type": "box", "layout": "vertical", "paddingAll": "12px", "contents": [
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                btn("官方網站", LINKS["site"], NAVY),
                btn("LINE 諮詢", LINKS["line"], BROWN),
                btn("導航門市", LINKS["map"], NAVY) ]} ]},
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
    # BUILD 版號 +1（給外部檔案模式留一份保險）
    html = re.sub(r"(const BUILD = 'b)(\d+)(')",
                  lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", html, count=1)
    page.write_text(html, encoding="utf-8")
    print("已內嵌進 index.html，頁面大小", len(html.encode()), "bytes")


def main():
    bubble_cards = [build_bubble(i, c) for i, c in enumerate(CARDS)]
    payload = {"type": "flex", "altText": "莫凡彼沙發工藝｜吳明憲 Steve 電子名片",
               "contents": {"type": "carousel", "contents": bubble_cards}}
    out = pathlib.Path(__file__).with_name("flex-cards.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"寫出 {out}　卡片數 = {len(bubble_cards)}　{out.stat().st_size} bytes")
    inject_into_page(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
