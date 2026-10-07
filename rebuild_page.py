#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
友泰京玻璃工程｜一頁式名片網頁 內容重建器
------------------------------------------------
把 index.html 裡的「名片內容區」整段換成 TEZ 的文案（其餘程式邏輯不動）。
改文案只要改這個檔的 CONTENT，然後 python rebuild_page.py

區域界線：<!-- CONTENT_START -->  ...  <!-- CONTENT_END -->
"""
import pathlib, re

ADDR = "新北市中和區連城路518巷8號"
TEL_TXT = "0938-111-822"
TEL_LINK = "tel:+886938111822"
LINE = "https://line.me/ti/p/@fez86488989"
IG = "https://www.instagram.com/tc_fez_glass_team/"
FB = "https://www.facebook.com/profile.php?id=100079776776531"
MAPQ = "友泰京玻璃工程 " + ADDR

BRAND = "友泰京玻璃工程"
BRAND_EN = "TC FEZ GLASS"
OWNER = ("李柏融", "Benson Lee")
ROLE = "友泰京玻璃工程　執行長"
SLOGAN1, SLOGAN2 = "讓藝術融入玻璃", "讓隔熱成為空間美學"
TAGS = ["藝術玻璃", "空間玻璃", "工程整合", "外牆高空作業"]

AUDIENCE = [("🏢", "設計師"), ("📐", "建築師"), ("🏗️", "建商"),
            ("🧱", "營造"), ("🏬", "商業空間"), ("🏠", "住宅業主")]
PAINS = ["想做有質感的藝術玻璃，卻只拿到大圖輸出的方案，缺少工藝層次",
         "玻璃與鐵件扶手由不同廠商施作，尺寸、固定與收邊難以整合",
         "設計圖很漂亮，卻找不到能實際製作與施工的玻璃廠商",
         "特殊造型、彎曲或異材質搭配，詢問多家仍找不到合適方案",
         "希望玻璃兼顧美感、採光與隔熱，卻不知道該如何選材",
         "玻璃種類與報價差異大，難以判斷品質及工法是否符合需求"]
SVCS = [("🎨", "藝術玻璃", "工藝 · 色彩 · 光影", "結合工藝、色彩與光影，為住宅、商業空間及建築打造獨特的玻璃作品。"),
        ("🪟", "空間玻璃", "隔間 · 門窗 · 欄杆", "依空間需求規劃玻璃隔間、門窗、淋浴拉門與欄杆，兼顧美感與實用機能。"),
        ("🔧", "工程整合", "丈量 · 加工 · 安裝", "整合玻璃、鋁框與鐵件，從丈量、加工到安裝，讓尺寸、固定與收邊完整到位。"),
        ("🧗", "外牆高空作業", "檢測 · 修繕 · 防水", "提供外牆檢測、修繕、防水及矽膠更新，依現場條件規劃高空作業方式。")]
STATS = [("30+ 年", "玻璃產業服務經驗"), ("第三代", "玻璃工藝傳承"), ("4 大服務", "完整專業整合")]
STEPS = [("需求確認", "了解設計想法、使用需求與預算，釐清施作範圍"),
         ("場勘丈量", "確認現場尺寸、結構及施工條件，評估整合細節"),
         ("方案定案", "確認玻璃選材、工法、樣品與報價，建立施作依據"),
         ("製作安裝", "依確認方案加工製作，整合玻璃、鋁框與鐵件施工"),
         ("驗收交付", "確認成品、收邊與使用功能，提供保養及維護建議")]
CRAFT = [("craft1.jpg", "藝術工藝｜光影層次", "鑲嵌、紋理與複合工藝，呈現玻璃的立體層次與光影美感"),
         ("craft2.jpg", "機能選材｜美感兼顧實用", "安全玻璃、Low-E 或中空複合結構，兼顧美感與機能需求"),
         ("craft3.jpg", "精準加工｜實現特殊設計", "特殊尺寸、彎曲造型及異材質搭配，符合設計需求"),
         ("craft4.jpg", "施工細節｜整合完整到位", "固定、接合及矽膠收邊，讓成品穩固、俐落且便於維護")]

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
  <div class="sec-title">ABOUT｜<em>認識友泰京</em></div>
  <div class="rail" id="rail">

    <article class="card">
      <h3>我們專為<em>誰服務</em></h3>
      <div class="grid6">
        {''.join(f'<div><span>{i}</span>{t}</div>' for i, t in AUDIENCE)}
      </div>
      <div class="box">
        <div class="bt">你是不是也遇過這些狀況？</div>
        <ul class="warn">
          {''.join(f'<li>{p}</li>' for p in PAINS)}
        </ul>
      </div>
      <div class="talk">中了其中一項，歡迎直接找我聊聊！</div>
    </article>

    <!-- ═══════════ 3 ═══════════ -->
    <article class="card">
      <h3>我們能為你做什麼</h3>
      <p class="sub">從設計規劃到現場施作，實現空間想像</p>
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
      <h3>為什麼選擇 <em>友泰京</em>？</h3>
      <div class="stats">
        {''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in STATS)}
      </div>
      <p class="sub" style="margin-bottom:8px">從需求到交付，五步完成</p>
      <ol class="steps">
        {''.join(f'<li><b>{n}</b>　{d}</li>' for n, d in STEPS)}
      </ol>
    </article>

    <!-- ═══════════ 5 ═══════════ -->
    <article class="card">
      <h3>工藝藏在<em>細節</em>，品質落在實處</h3>
      <div class="craft">
        {''.join(f'''<figure>
          <img src="{src}" alt="{h}" onerror="this.outerHTML='<div class=&quot;ph&quot;>照片</div>'">
          <figcaption><h4>{h}</h4><p>{p}</p></figcaption>
        </figure>''' for src, h, p in CRAFT)}
      </div>
    </article>

    <!-- ═══════════ 6 ═══════════ -->
    <article class="card">
      <h3>作品<em>案例</em></h3>
      <p class="sub">實際施作案例照（Benson 提供後放入 case1~3.jpg）</p>
      <div class="craft">
        {''.join(f'''<figure>
          <img src="case{i}.jpg" alt="案例{i}" onerror="this.outerHTML='<div class=&quot;ph&quot;>案例照</div>'">
        </figure>''' for i in (1, 2, 3))}
      </div>
    </article>

    <!-- ═══════════ 7 ═══════════ -->
    <article class="card">
      <h3>讓我們聊聊<em>你的空間</em></h3>
      <div class="box" style="text-align:center;background:#E7F2F5;border-style:solid">
        <p style="margin:0 0 6px;font-weight:800;color:var(--navy);font-size:15px">拍下現場照片 ＋ 尺寸</p>
        <p style="margin:0;font-weight:800;color:var(--brown);font-size:15px">LINE 傳給我</p>
        <p style="margin:8px 0 0;font-size:13.5px;color:#4A5468">免費初步評估最適合的玻璃方案</p>
      </div>

      <div class="info" style="margin:14px 0 0;box-shadow:none;padding:0;border:0">
        <div class="row"><div class="k">電話</div><div><a href="{TEL_LINK}">{TEL_TXT}</a></div></div>
        <div class="row"><div class="k">地址</div><div>{ADDR}<br><span class="note">中和高中旁巷</span></div></div>
        <div class="row"><div class="k">營業時間</div><div class="note">週一～五 08:00-17:00</div></div>
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
  <div class="sec-title">VISIT｜<em>聯絡資訊</em></div>
  <div class="info">
    <div class="row"><div class="k">地址</div><div>{ADDR}<br><span class="note">中和高中旁巷</span></div></div>
    <div class="row"><div class="k">電話</div><div><a href="{TEL_LINK}">{TEL_TXT}</a></div></div>
    <div class="row"><div class="k">時間</div><div class="note">週一～五 08:00-17:00</div></div>
    <div class="row"><div class="k">LINE</div><div><a data-link="line" href="#">@fez86488989（官方帳號）</a><br><span class="note">個人帳號：benson911</span></div></div>
    <div class="row"><div class="k">社群</div><div><a data-link="ig" href="#">Instagram</a>　·　<a data-link="fb" href="#">Facebook</a></div></div>
  </div>
<!-- CONTENT_END -->"""


def main():
    page = pathlib.Path(__file__).with_name("index.html")
    html = page.read_text(encoding="utf-8")

    if "<!-- CONTENT_START -->" in html:
        i = html.index("<!-- CONTENT_START -->")
        j = html.index("<!-- CONTENT_END -->") + len("<!-- CONTENT_END -->")
    else:  # 第一次：用舊區塊界線包起來
        i = html.index("  <!-- ═══════════ 1 / 7")
        j = html.index('<p class="tip" id="tipText">') - 2
    html = html[:i] + CONTENT + html[j:]

    # 品牌／SEO／配色／footer／JS 連結
    html = html.replace("<title>吳明憲 Steve｜莫凡彼沙發工藝 負責人</title>",
                        f"<title>{OWNER[0]} {OWNER[1]}｜{BRAND} 執行長</title>")
    html = html.replace('content="吳明憲 Steve｜莫凡彼沙發工藝 負責人"',
                        f'content="{OWNER[0]} {OWNER[1]}｜{BRAND} 執行長"')
    html = html.replace('content="生活沒有標準尺寸，沙發也不該只有標準答案。沙發訂製・展售・批發・專業諮詢｜03-397-2191"',
                        f'content="{SLOGAN1}，{SLOGAN2}。藝術玻璃・空間玻璃・工程整合・外牆高空作業｜{TEL_TXT}"')
    html = re.sub(r"--navy:#16233D; --navy-2:#22355C; --navy-3:#2E4675;",
                  "--navy:#0E2A3A; --navy-2:#123A4A; --navy-3:#1B5063;", html, count=1)
    html = re.sub(r"--brown:#A96B3C; --gold:#C9A227; --gold-2:#E3C878;",
                  "--brown:#2E7D8F; --gold:#4FA8BD; --gold-2:#9BD7E4;", html, count=1)
    html = html.replace('<div class="ss-logo">MOVENPICK<small>莫凡彼沙發工藝</small></div>',
                        f'<div class="ss-logo">{BRAND_EN}<small>{BRAND}</small></div>')
    html = html.replace('background:#A96B3C">📨 直接傳到這個聊天室', 'background:#2E7D8F">📨 直接傳到這個聊天室')
    html = re.sub(r"const LINKS = \{.*?\n\};",
                  "const LINKS = {\n"
                  f"  line: '{LINE}',\n"
                  f"  map : 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('{MAPQ}'),\n"
                  f"  ig  : '{IG}',\n"
                  f"  fb  : '{FB}'\n"
                  "};", html, count=1, flags=re.S)
    html = re.sub(r"const SHARE_TITLE = '.*?';",
                  f"const SHARE_TITLE = '{OWNER[0]} {OWNER[1]}｜{BRAND} 執行長';", html, count=1)
    html = re.sub(r"const SHARE_TEXT  = '.*?';",
                  f"const SHARE_TEXT  = '{SLOGAN1}，{SLOGAN2}。藝術玻璃・空間玻璃・工程整合・外牆高空作業｜{TEL_TXT}';",
                  html, count=1)
    html = re.sub(r"  footer\{.*?\n", "  footer{text-align:center;font-size:11.5px;color:#9AA1AE;margin:24px 20px 0;line-height:1.9}\n",
                  html, count=1)
    html = re.sub(r"  <footer>.*?</footer>",
                  f"  <footer>\n    {BRAND} {BRAND_EN}　藝術玻璃・空間玻璃・工程整合・外牆高空作業<br>\n"
                  f"    {ADDR}　{TEL_TXT}<br>\n"
                  f"    © <span id=\"y\"></span> TC FEZ Glass. All rights reserved.\n  </footer>",
                  html, count=1, flags=re.S)
    page.write_text(html, encoding="utf-8")
    print("✓ 一頁式名片內容已換成友泰京　", len(html.encode()), "bytes")


if __name__ == "__main__":
    main()
