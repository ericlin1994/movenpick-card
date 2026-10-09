#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一頁式名片網頁 內容重建器（多客戶版）
------------------------------------------------
換客戶只改 client.json，不要改本檔。

資料驅動的兩塊：
  1. CONTENT 區塊（<!-- CONTENT_START --> ... <!-- CONTENT_END -->）＝ 名片內容
  2. 品牌／SEO／配色／footer／JS LINKS ＝ 用結構化 regex 就地改寫
     （不再比對「上一個客戶的字串」，所以任何客戶都能直接換）

用法：python rebuild_page.py
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).parent
CLIENT = json.loads((HERE / "client.json").read_text(encoding="utf-8"))

B      = CLIENT["brand"]
C      = CLIENT["contact"]
LK     = CLIENT["links"]
WEB    = CLIENT["web"]
TH     = CLIENT["theme"]

BRAND    = B["name"]
BRAND_EN = B["en"]
LEGAL    = B["legal"]
OWNER    = (B["owner_name"], B["owner_en"])
ROLE     = B["role"]
SLOGAN1, SLOGAN2 = B["slogan1"], B["slogan2"]
TAGS     = B["tags"]

ADDR      = C["addr"]
ADDR_NOTE = C["addr_note"]
HOURS     = C["hours"]
TEL_TXT   = C["phone"]
TEL_LINK  = LK["tel"]
LINE      = LK["line"]
IG        = LK["ig"]
FB        = LK["fb"]
MAPQ      = C["map_query"]

AUDIENCE = [tuple(x) for x in WEB["audience"]]
PAINS    = WEB["pains"]
SVCS     = [tuple(x) for x in WEB["services"]]
STATS    = [tuple(x) for x in WEB["stats"]]
STEPS    = [tuple(x) for x in WEB["steps"]]
CRAFT    = [tuple(x) for x in WEB["craft"]]
CTA      = WEB["cta"]

CONTENT = f"""<!-- CONTENT_START -->
  <!-- ═══════════ 1　主卡 ═══════════ -->
  <header class="hero">
    <div class="logo">{BRAND_EN}<small>{BRAND}</small></div>

    <!-- TODO: 形象照存成 photo.jpg 放同一資料夾；沒有檔案時顯示佔位圈 -->
    <img class="portrait" src="photo.jpg" alt="{OWNER[0]} {OWNER[1]}"
         onerror="this.outerHTML='<div class=&quot;portrait-ph&quot;>形象照</div>'">

    <h1 class="name">{OWNER[0]} <span>{OWNER[1]}</span></h1>
    <p class="role">{ROLE}</p>

    <div class="slogan">
      <i>“</i>
      <span class="big">{SLOGAN1}</span>
      {SLOGAN2}
      <i>”</i>
    </div>

    <div class="tags">
      {''.join(f'<span class="tag">{t}</span>' for t in TAGS)}
    </div>

    <nav class="actions">
      <a class="btn line" data-link="line"><span class="ic">💬</span>LINE 諮詢</a>
      <a class="btn" data-link="ig"><span class="ic">📷</span>IG 作品</a>
      <a class="btn" data-link="map"><span class="ic">📍</span>導航門市</a>
    </nav>
  </header>

  <!-- ═══════════ 2 ═══════════ -->
  <div class="sec-title">{WEB["about_title_html"]}</div>
  <div class="rail" id="rail">

    <article class="card">
      <h3>我們專為<em>誰服務</em></h3>
      <div class="grid6">
        {''.join(f'<div><span>{i}</span>{t}</div>' for i, t in AUDIENCE)}
      </div>
      <div class="box">
        <div class="bt">{WEB["pain_title"]}</div>
        <ul class="warn">
          {''.join(f'<li>{p}</li>' for p in PAINS)}
        </ul>
      </div>
      <div class="talk">{WEB["talk"]}</div>
    </article>

    <!-- ═══════════ 3 ═══════════ -->
    <article class="card">
      <h3>{WEB["services_title"]}</h3>
      <p class="sub">{WEB["services_sub"]}</p>
      {''.join(f'''<div class="svc">
        <div class="ico">{ic}</div>
        <div>
          <h4>{h}</h4>
          <div class="tagsm">{tg}</div>
          <p>{p}</p>
        </div>
      </div>''' for ic, h, tg, p in SVCS)}
    </article>

    <!-- ═══════════ 4 ═══════════ -->
    <article class="card">
      <h3>為什麼選擇 <em>{WEB["why_short_name_em"]}</em>？</h3>
      <div class="stats">
        {''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in STATS)}
      </div>
      <p class="sub" style="margin-bottom:8px">{WEB["steps_sub"]}</p>
      <ol class="steps">
        {''.join(f'<li><b>{n}</b>　{d}</li>' for n, d in STEPS)}
      </ol>
    </article>

    <!-- ═══════════ 5 ═══════════ -->
    <article class="card">
      <h3>{WEB["craft_title_html"]}</h3>
      <div class="craft">
        {''.join(f'''<figure>
          <img src="{src}" alt="{h}" onerror="this.outerHTML='<div class=&quot;ph&quot;>照片</div>'">
          <figcaption><h4>{h}</h4><p>{p}</p></figcaption>
        </figure>''' for src, h, p in CRAFT)}
      </div>
    </article>

    <!-- ═══════════ 6 ═══════════ -->
    <article class="card">
      <h3>{WEB["case_title_html"]}</h3>
      <p class="sub">{WEB["case_sub"]}</p>
      <div class="craft">
        {''.join(f'''<figure>
          <img src="case{i}.jpg" alt="案例{i}" onerror="this.outerHTML='<div class=&quot;ph&quot;>案例照</div>'">
        </figure>''' for i in range(1, WEB["case_count"] + 1))}
      </div>
    </article>

    <!-- ═══════════ 7 ═══════════ -->
    <article class="card">
      <h3>{WEB["contact_title_html"]}</h3>
      <div class="box" style="text-align:center;background:{WEB["cta_box_bg"]};border-style:solid">
        <p style="margin:0 0 6px;font-weight:800;color:var(--navy);font-size:15px">{CTA[0]}</p>
        <p style="margin:0;font-weight:800;color:var(--brown);font-size:15px">{CTA[1]}</p>
        <p style="margin:8px 0 0;font-size:13.5px;color:#4A5468">{CTA[2]}</p>
      </div>

      <div class="info" style="margin:14px 0 0;box-shadow:none;padding:0;border:0">
        <div class="row"><div class="k">電話</div><div><a href="{TEL_LINK}">{TEL_TXT}</a></div></div>
        <div class="row"><div class="k">地址</div><div>{ADDR}<br><span class="note">{ADDR_NOTE}</span></div></div>
        <div class="row"><div class="k">營業時間</div><div class="note">{HOURS}</div></div>
      </div>

      <nav class="actions" style="grid-template-columns:1fr 1fr;margin-top:16px">
        <a class="btn line" data-link="line"><span class="ic">💬</span>LINE 諮詢</a>
        <a class="btn" data-link="ig"><span class="ic">📷</span>Instagram</a>
        <a class="btn" href="{TEL_LINK}"><span class="ic">📞</span>撥打電話</a>
        <a class="btn" data-link="map"><span class="ic">📍</span>導航門市</a>
        <a class="btn" data-link="fb"><span class="ic">👍</span>Facebook</a>
      </nav>
    </article>

  </div>
  <div class="count" id="count"><b>2</b> / 7　左右滑動看更多</div>

  <!-- ═══════════ 店家資訊 ═══════════ -->
  <div class="sec-title">{WEB["visit_title_html"]}</div>
  <div class="info">
    <div class="row"><div class="k">地址</div><div>{ADDR}<br><span class="note">{ADDR_NOTE}</span></div></div>
    <div class="row"><div class="k">電話</div><div><a href="{TEL_LINK}">{TEL_TXT}</a></div></div>
    <div class="row"><div class="k">時間</div><div class="note">{HOURS}</div></div>
    <div class="row"><div class="k">LINE</div><div><a data-link="line" href="#">{C["line_id"]}（官方帳號）</a><br><span class="note">個人帳號：{C["line_personal"]}</span></div></div>
    <div class="row"><div class="k">社群</div><div><a data-link="ig" href="#">Instagram</a>　·　<a data-link="fb" href="#">Facebook</a></div></div>
  </div>
<!-- CONTENT_END -->"""


def sub1(html, pattern, repl, label):
    """結構化單次取代；找不到就回報（避免靜默失效）"""
    new, n = re.subn(pattern, repl, html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"✗ 找不到要取代的區塊：{label}（pattern={pattern!r}）")
    return new


def main():
    page = pathlib.Path(__file__).with_name("index.html")
    html = page.read_text(encoding="utf-8")

    # ── 1. 名片內容區 ──
    if "<!-- CONTENT_START -->" not in html or "<!-- CONTENT_END -->" not in html:
        raise SystemExit("✗ index.html 缺少 <!-- CONTENT_START/END --> 界線，無法重建內容區")
    i = html.index("<!-- CONTENT_START -->")
    j = html.index("<!-- CONTENT_END -->") + len("<!-- CONTENT_END -->")
    html = html[:i] + CONTENT + html[j:]

    # ── 2. 品牌／SEO ──
    title = WEB["seo_title"]
    html = sub1(html, r"(<title>).*?(</title>)", lambda m: m.group(1) + title + m.group(2), "<title>")
    html = sub1(html, r'(<meta name="description" content=")[^"]*(">)',
                lambda m: m.group(1) + WEB["seo_description"] + m.group(2), "meta description")
    html = sub1(html, r'(<meta property="og:title" content=")[^"]*(">)',
                lambda m: m.group(1) + title + m.group(2), "og:title")
    html = sub1(html, r'(<meta property="og:description" content=")[^"]*(">)',
                lambda m: m.group(1) + WEB["seo_description"] + m.group(2), "og:description")
    html = sub1(html, r'(<meta name="theme-color" content=")[^"]*(">)',
                lambda m: m.group(1) + TH["NAVY"] + m.group(2), "theme-color")
    # favicon：emoji 藏在 href 的 data URI 內（同一個 tag 裡就有 '>'），所以整段一起比對
    html = sub1(html, r"(<link rel=\"icon\".*?font-size='90'>).*?(</text>)",
                lambda m: m.group(1) + B["favicon_emoji"] + m.group(2), "favicon emoji")
    html = sub1(html, r'(<div class="ss-logo">).*?(</div>)',
                lambda m: m.group(1) + f'{BRAND_EN}<small>{BRAND}</small>' + m.group(2), "分享頁 logo")

    # ── 3. 配色（由 client.json theme 決定） ──
    nv, ac = TH["WEB_NAVY"], TH["WEB_ACCENT"]
    html = sub1(html, r"--navy:#[0-9A-Fa-f]{6}; --navy-2:#[0-9A-Fa-f]{6}; --navy-3:#[0-9A-Fa-f]{6};",
                f"--navy:{nv[0]}; --navy-2:{nv[1]}; --navy-3:{nv[2]};", "navy 三階")
    html = sub1(html, r"--brown:#[0-9A-Fa-f]{6}; --gold:#[0-9A-Fa-f]{6}; --gold-2:#[0-9A-Fa-f]{6};",
                f"--brown:{ac[0]}; --gold:{ac[1]}; --gold-2:{ac[2]};", "強調色三階")

    # ── 4. footer ──
    html = sub1(html, r"  <footer>.*?</footer>",
                "  <footer>\n"
                f"    {BRAND} {BRAND_EN}　{B['services_line']}<br>\n"
                f"    {ADDR}　{TEL_TXT}<br>\n"
                f"    © <span id=\"y\"></span> {LEGAL}. All rights reserved.\n"
                "  </footer>", "footer")

    # ── 5. JS 連結與分享文案 ──
    html = sub1(html, r"const LINKS = \{.*?\n\};",
                "const LINKS = {\n"
                f"  line: '{LINE}',\n"
                f"  map : 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('{MAPQ}'),\n"
                f"  ig  : '{IG}',\n"
                f"  fb  : '{FB}'\n"
                "};", "const LINKS")
    share_title = f"{OWNER[0]} {OWNER[1]}｜{BRAND} 執行長"
    html = sub1(html, r"const SHARE_TITLE = '.*?';",
                f"const SHARE_TITLE = '{share_title}';", "SHARE_TITLE")
    html = sub1(html, r"const SHARE_TEXT  = '.*?';",
                f"const SHARE_TEXT  = '{WEB['seo_description']}';", "SHARE_TEXT")

    page.write_text(html, encoding="utf-8")
    print("✓ 一頁式名片內容已依 client.json 重建　", len(html.encode()), "bytes")


if __name__ == "__main__":
    main()
