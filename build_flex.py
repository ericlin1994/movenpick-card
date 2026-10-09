#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE 電子名片 Flex Message 產生器 v4（多客戶版）
------------------------------------------------
所有客戶資料都集中在 client.json —— 換客戶只改 client.json，不要改本檔。
風格：雜誌海報感（3:4 直式 Hero 烤字）+ 精品配色
用法：python build_flex.py
"""
import json, pathlib, urllib.parse

HERE = pathlib.Path(__file__).parent
CLIENT = json.loads((HERE / "client.json").read_text(encoding="utf-8"))

B      = CLIENT["brand"]
C      = CLIENT["contact"]
LK     = CLIENT["links"]
FLEX   = CLIENT["flex"]
IMGCFG = CLIENT["images"]
TH     = CLIENT["theme"]

IMG      = LK["img_base"]
LIFF_URL = LK["liff"]
ADDR     = C["addr"]

# liff 未設定時（模板狀態）給一個格式合法但無效的佔位網址，
# 讓卡片結構仍能通過 validate_flex；買家填上自己的 LIFF 後就自動生效。
_UNSET = "https://liff.line.me/0000000000-XXXXXXXX"
if (not LIFF_URL) or "0000000000" in LIFF_URL:
    LIFF_URL = _UNSET
# ── 分享模式 ──
# own    = 客戶自己申請的 LIFF（點卡片圖片 → 開啟自己的名片頁 → 再按分享）
# shared = 共用一組 LIFF（點卡片圖片 → 中繼頁把 src 指到的 flex-cards.json 抓回來分享）
#          買家不必自己去 LINE 控制台申請，這是自助版的預設。
SHARE = LK.get("share") or {}
SHARE_MODE = SHARE.get("mode", "own")
if SHARE_MODE == "shared" and SHARE.get("relay_liff"):
    SRC = SHARE.get("src") or (LK["page_url"].rstrip("/") + "/flex-cards.json")
    SHARE_URL = f"{SHARE['relay_liff']}?share=1&src={SRC}&v={LK['share_ver']}"
    CARD_URL = SHARE_URL          # 點卡片圖片 = 一鍵轉發
else:
    SHARE_URL = LIFF_URL + "?share=1&v=" + LK["share_ver"]
    CARD_URL = LIFF_URL           # 點卡片圖片 = 開啟自己的名片頁

LINKS = {
    "line":  LK["line"],
    "line2": LK["line2"],
    "ig":    LK["ig"],
    "fb":    LK["fb"],
    "tel":   LK["tel"],
    "map":   "https://www.google.com/maps/search/?api=1&query="
             + urllib.parse.quote(C["map_query"]),
    "share": SHARE_URL,
}

# ═══════════ Design Tokens ═══════════
NAVY   = TH["NAVY"]
NAVY_D = TH["NAVY_D"]
COPPER = TH["COPPER"]
BEIGE  = TH["BEIGE"]
WHITE  = TH["WHITE"]
MUTED  = TH["MUTED"]
DIVIDE = TH["DIVIDE"]


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


def chunk(seq, n):
    return [list(seq[i:i + n]) for i in range(0, len(seq), n)]


def pill(label, uri, bg, fg=WHITE):
    """圓角膠囊按鈕：用 box + action 做（LINE 預設 button 無法自訂圓角與底色）。
    標籤要短、字級 xxs、允許換行——三顆膠囊各佔 1/3 寬，字太長會被裁掉。"""
    return box([t(label, size="xxs", weight="bold", color=fg, align="center", wrap=True)],
               spacing="none", padding="10px", bg=bg, radius="100px", flex=1,
               action={"type": "uri", "label": label[:20], "uri": uri})


def control_row():
    """共用底部操作區：米白圓角底 + 膠囊列（由 client.json 的 flex.pills 決定）"""
    return box([hbox(*[pill(p["label"], LINKS[p["link"]], TH[p["bg"]]) for p in FLEX["pills"]],
                     spacing="sm")],
               spacing="none", padding="10px", bg=BEIGE, radius="20px")


def tag_pill(label):
    return box([t(label, size="xxs", weight="bold", color=WHITE, align="center", wrap=False)],
               spacing="none", padding="8px", radius="100px", flex=1,
               border=("1px", COPPER))


# ═══════════ 逐卡 body ═══════════
def body1():
    """雜誌封面款：主文案烤進 Hero 圖；body 保留一行保險文字 + 操作列"""
    return vbox([t(FLEX["cover_line"], size="xxs", color=MUTED, margin="none"),
                 control_row()], spacing="md", padding="14px", bg=NAVY)


def body2():
    aud = FLEX["audiences"]
    pains = FLEX["pains"]
    return vbox([
        t(FLEX["titles"][1], size="xl", weight="bold", color=COPPER, margin="none"),
        vbox(*[hbox(*[tag_pill(x) for x in row], spacing="xs") for row in chunk(aud, 3)],
             spacing="xs", margin="md"),
        box([t(FLEX["pain_title"], size="xs", weight="bold", color=NAVY, margin="none"),
             sep("sm", DIVIDE)] +
            [hbox(t("📌", size="xs", color=COPPER, flex=1, wrap=False),
                  t(p, size="xs", color=NAVY, flex=6, margin="none"), spacing="sm",
                  margin="sm")
             for p in pains],
            spacing="sm", padding="18px", bg=BEIGE, radius="20px", margin="md"),
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body3():
    def cell(ic, name, desc):
        return box([t(ic, size="md", color=COPPER, margin="none", wrap=False),
                    t(name, size="sm", weight="bold", color=WHITE, margin="sm", wrap=False),
                    t(desc, size="xs", color=MUTED, margin="xs")],
                   spacing="none", padding="16px", bg=NAVY_D, radius="16px", flex=1)
    return vbox([
        t(FLEX["services_title"], size="xl", weight="bold", color=COPPER, margin="none"),
        t(FLEX["services_sub"], size="sm", color=WHITE, margin="xs"),
    ] + [hbox(*[cell(s["icon"], s["name"], s["desc"]) for s in row], spacing="md", margin="md")
         for row in chunk(FLEX["services"], 2)] + [
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body4():
    stats = [(s["big"], s["small"]) for s in FLEX["stats"]]
    return vbox([
        t(f"{FLEX['why_prefix']}{B['short_name']}？", size="xl", weight="bold", color=COPPER, margin="none"),
    ] + [hbox(t(big, size="4xl", weight="bold", color=COPPER, flex=2, wrap=False),
              t(small, size="sm", weight="bold", color=WHITE, flex=3, margin="none"),
              spacing="md", align_items="center", margin="xl" if i == 0 else "md")
         for i, (big, small) in enumerate(stats)] + [
        control_row(),
    ], spacing="md", padding="18px", bg=NAVY)


def body5():
    """工藝：主文案烤進 3:4 Hero 圖；body 保留一行保險文字 + 操作列"""
    return vbox([t(FLEX["craft_line"], size="xxs", color=MUTED, margin="none"),
                 control_row()], spacing="md", padding="14px", bg=NAVY)


def body6():
    def row(ic, txt, size="sm", weight="bold", color=WHITE):
        return hbox(t(ic, size="sm", color=COPPER, flex=1, wrap=False),
                    t(txt, size=size, weight=weight, color=color, flex=6, margin="none"),
                    spacing="sm", margin="sm")
    rows = [row(r["icon"], r["text"],
                size="sm" if r.get("emphasis", True) else "xs",
                weight="bold" if r.get("emphasis", True) else "regular")
            for r in FLEX["contact_rows"]]
    return vbox([
        t(FLEX["contact_title"], size="xl", weight="bold", color=NAVY, margin="none"),
        t(FLEX["contact_sub"], size="xs", weight="bold", color=COPPER, margin="xs"),
        box(rows, spacing="sm", padding="18px", bg=NAVY, radius="20px", margin="md"),
        control_row(),
    ], spacing="md", padding="18px", bg=BEIGE)


BODIES = [body1, body2, body3, body4, body5, body6]
HEROES = {int(k): f"{IMG}/{v}" for k, v in IMGCFG["heroes"].items()}
BG_COLOR = {i + 1: TH[name] for i, name in enumerate(FLEX["bg_pages"])}
TITLES = FLEX["titles"]
SUMMARIES = FLEX["summaries"]


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
                     "action": {"type": "uri", "label": "開啟名片", "uri": CARD_URL}}
    return b


# ═══════════ 備援版（結構最簡） ═══════════
def build_candidate(with_hero: bool):
    bubbles = []
    for i in range(len(BODIES)):
        n = i + 1
        body = vbox([t(TITLES[i], size="sm", weight="bold", color=WHITE, margin="none"),
                     t("\n".join("· " + s for s in SUMMARIES[i]), size="xs", color=MUTED, margin="xs")],
                    spacing="none")
        b = {"type": "bubble", "styles": {"body": {"backgroundColor": NAVY}}, "body": body,
             "footer": vbox([box([t(FLEX["cta_line"], size="xs", weight="bold", color=WHITE,
                                    align="center", wrap=False)], padding="12px", bg=COPPER,
                                 radius="100px", action={"type": "uri", "label": FLEX["cta_line"],
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
    bubbles = [build_bubble(n) for n in range(1, len(BODIES) + 1)]
    payload = {"type": "flex", "altText": FLEX["alt_text"],
               "contents": {"type": "carousel", "contents": bubbles}}
    out = pathlib.Path(__file__).with_name("flex-cards.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"寫出 {out}　卡片數 = {len(bubbles)}　{out.stat().st_size} bytes")
    inject_into_page(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    inject_candidates()


if __name__ == "__main__":
    main()
