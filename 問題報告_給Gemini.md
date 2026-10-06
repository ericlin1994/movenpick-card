# LINE 電子名片（LIFF + Flex Message）問題報告

> 目的：把目前所有事實、證據、程式碼與已排除的假設整理出來，請第三方（Gemini）協助找出「為什麼 shareTargetPicker 回報成功卻沒有卡片」。

---

## 0. 摘要（TL;DR）

* 目標：做一張**在 LINE 聊天室裡原生顯示、可左右滑動 7 張、底部有按鈕、收到的人可以再轉發**的電子名片。
* 做法：LIFF 網頁 + `liff.shareTargetPicker()` 送 Flex Message carousel（**不需要 LINE 官方帳號**）。
* 現況：
  * **極簡卡片**（1 顆按鈕、無圖片、約 390 bytes）→ **可以送達**。
  * **正式版卡片**（7 張、有圖片、多顆按鈕、3～17 KB）→ `shareTargetPicker` **回報 `{status:"success"}`，但對方聊天室完全沒有東西**（連空白氣泡都沒有、雙方都沒有「傳送失敗」標記）。
  * 另一條通道 `liff.sendMessages()` 明確報錯：**`The permission is not in LIFF app scope.`**

---

## 1. 環境與設定

| 項目 | 值 |
|---|---|
| 平台 | iPhone / iOS 26.5.2 / LINE App **26.15.1** |
| LIFF SDK | 2.31.1 |
| LIFF ID | `2011897701-TrLfDuwi` |
| LIFF Endpoint URL | `https://ericlin1994.github.io/movenpick-card/` |
| Channel 狀態 | 已 **Publish**（發佈後無法退回 Developing） |
| `shareTargetPicker` | Console 已 **Enable** |
| `liff.isInClient()` | true |
| `liff.isLoggedIn()` | true |
| `liff.isApiAvailable('shareTargetPicker')` | true |
| **LIFF Scopes** | **未開啟 `chat_message.write`（sendMessages 明確報錯）** |
| 送出者 | 自己的 LINE 帳號（非官方帳號、非 bot） |

前端診斷面板輸出（使用者手機實際畫面）：

```
· payload 來源：內嵌在頁面（最新）
· payload：7 張卡｜按鈕屬性 乾淨
· LINE App 版本：26.15.1｜LIFF SDK：2.31.1｜OS：(iPhone; CPU iPhone OS 26_5_2 like Mac O
· 頁面版本：2026-10-07-0210-加sendMessages路線
✗ liff.init OK｜inClient=true｜loggedIn=true｜shareTargetPicker=true｜payload=7 張卡
· 👆 分享按鈕被按下（上午12:07:11）
· 本次送出類型：完整 7 張 Flex 卡片
· shareTargetPicker 回傳成功，卡片已送出
```

---

## 2. 送出程式（目前實際執行的程式碼）

```js
// 分享（走 picker）
async function shareCard(){
  if(liffReady){
    if(!liff.isLoggedIn()){ liff.login({ redirectUri: location.href }); return; }
    if(!liff.isApiAvailable('shareTargetPicker')){ /* 顯示錯誤 */ }
    else{
      msg = [flexPayload];                       // 正式版：一則 carousel
      const res = await liff.shareTargetPicker(msg, { isMultiple: true });
      if(res){ /* 面板印「回傳成功」 */ }          // res = { status: "success" }
      else   { /* 使用者取消 → res 是 null */ }
    }
  }
}

// 另一條通道（不使用 picker）
async function sendToChat(){
  const ctx = liff.getContext();                 // ctx.type === 'utou'（一對一）
  await liff.sendMessages([flexPayload]);        // ← 這裡報 scope 錯誤
}
```

---

## 3. 症狀：回報成功但沒有送達

`liff.shareTargetPicker()` 的官方回傳語意（LIFF API reference）：

* 成功送出 → `Promise` resolved 且帶 `{ status: "success" }`
* 使用者取消 → resolved 但**不帶物件**（`null`）
* 送出行為前出錯 → rejected，帶 `LiffError`

我們的觀察：**拿到 `{ status: "success" }`，但訊息不存在**。因此問題不在「使用者取消」，也不在 SDK 丟錯。

---

## 4. 關鍵證據：哪些 payload 成功、哪些失敗

全部都是**同一支手機、同一支程式、同一個接收對象**，且 `shareTargetPicker` 全部回報成功。

| 測試 | payload 內容 | 大小 | 結果 |
|---|---|---|---|
| 純文字 | `[{type:"text"}]` | ~100 B | ✅ 送達 |
| 極簡卡 | 1 bubble：body 2 個 text + footer 1 顆 button（無圖片、無 `color`） | ~390 B | ✅ 送達 |
| 2 張極簡輪播 | 同上 ×2 bubbles | ~600 B | ✅ 送達（可左右滑） |
| 正式版（C 系列結構） | 7 bubbles：hero image + body 6～11 個元件（含 separator、margin、color、size 變體）+ footer（橫向 box 內 3 顆彩色 button + 1 顆 secondary） | **17.6 KB** | ❌ 沒送達 |
| 正式版（瘦身） | 7 bubbles：hero + body 3 個元件（內文用 `\n` 換行）+ footer（同 hbox 3 顆 + share） | 12.2 KB | ❌ 沒送達 |
| F1 | 7 bubbles：**無圖片** + body 3 個 text + footer **3 顆基本樣式 button（垂直排列、無 hbox）** | 8.0 KB | ❌ 沒送達 |
| F2 | F1 + hero image | 9.1 KB | ❌ 沒送達 |
| 2 張（正式版結構、無圖片） | 2 bubbles：body 3 元件 + footer hbox 3 顆 + share | ~2 KB | ❌ 沒送達 |

**目前無法用「單一零件」解釋成功／失敗**：1 顆按鈕成功、3 顆失敗；無圖片也可能失敗；但 2 張極簡輪播成功、2 張正式結構失敗。

---

## 5. 已用二分法「排除」的假設（每一個都做過對照組）

1. **按鈕屬性**：`height` / `margin` / `scaling` 加在 button 上 → 會讓整則訊息消失。移除後（只留 `style` + `color`）確實可送達過。→ **已修正**
2. **文字內容**：全角空格 `U+3000`、「·」等字元 → 含這些字元的極簡卡可以送達。→ **排除**
3. **快取**：LINE 內建瀏覽器會快取 LIFF 頁面與外部 JSON → 已改成把 payload **內嵌進 HTML**、加 `PAGE_VER` 版本戳記，使用者每次都確認拿到最新版。→ **排除**
4. **bubble 缺 `type`**：測試分支曾漏寫 `type:"bubble"`（無效 Flex）→ 已修，並寫了結構驗證器把關。→ **排除**
5. **`size: "mega"`、`spacing/margin` 值、`separator`、`aspectRatio: "20:13"`** → 逐項對照官方文件，全是合法值。→ **排除**
6. **機制與帳號**：`inClient`、`loggedIn`、`shareTargetPicker` 可用性、channel 已發佈 → 都正常，且極簡卡可送達。→ **排除**
7. **限流**：同一批零件在 23:00 可送達、23:20 之後全失敗 → 曾懷疑是 LINE 端降級，但**未證實**；且極簡卡在後期仍可送達，讓此假設說服力下降。

---

## 6. 最新發現（尚未驗證的關鍵）

`liff.sendMessages()` 的錯誤：

```
sendMessages 失敗：The permission is not in LIFF app scope.
聊天室類型：utou
```

官方文件：LIFF app 的 **Scopes** 需要 `chat_message.write` 才能用 `liff.sendMessages()`。目前**沒有開**。

**待驗證的假設**：
> `liff.shareTargetPicker()` 是否也在缺少 `chat_message.write`（或其他 scope）時，出現「回報 success 但訊息實際上沒有被送進 LINE 平台」的行為？若是，這就能同時解釋「極簡卡可送達、正式版沉默消失」之外的大部分現象（但**極簡卡為何能送達仍無法解釋**，需要進一步釐清）。

---

## 7. 希望協助回答的問題

1. `liff.shareTargetPicker()` 在缺少 `chat_message.write` scope 時，會不會出現「resolved 但沒有實際送達」的行為？還是它只需要「已登入」？
2. 有沒有**未公開的訊息大小／元件數量上限**（例如單則 Flex message 或 `messages` 陣列的位元組上限）會造成「回報成功但訊息被丟棄」？
3. 我這份 payload 有沒有任何**違反 Flex Message 規格**但不會被一般驗證器抓到的地方？（附錄 A、B 為實際 JSON）
4. 若 `shareTargetPicker` 這條路短期無法解決，**用「一對一聊天室 + `liff.sendMessages()`」或「官方帳號的多頁訊息」**，哪一條能達到「原生卡片、可左右滑、收件人可再轉發」的需求？

---

## 附錄 A：可正常送達的極簡卡（完整 JSON，約 390 B）

```json
{
  "type": "flex",
  "altText": "極簡小卡",
  "contents": {
    "type": "bubble",
    "body": { "type": "box", "layout": "vertical", "contents": [
      { "type": "text", "text": "極簡小卡（最早成功過的那張）", "weight": "bold" },
      { "type": "text", "text": "看到這張＝這個結構可用", "size": "sm", "wrap": true }
    ]},
    "footer": { "type": "box", "layout": "vertical", "contents": [
      { "type": "button", "style": "primary",
        "action": { "type": "uri", "label": "官方網站", "uri": "https://example.com" } }
    ]}
  }
}
```

## 附錄 B：正式版（失敗）第 1 張卡的結構（7 張同構，差異只有 hero 圖片與文字）

```json
{
  "type": "bubble",
  "size": "mega",
  "hero": { "type": "image", "url": "https://ericlin1994.github.io/movenpick-card/img/card1.jpg",
            "size": "full", "aspectRatio": "20:13", "aspectMode": "cover",
            "action": { "type": "uri", "label": "開啟名片",
                        "uri": "https://liff.line.me/2011897701-TrLfDuwi" } },
  "body": { "type": "box", "layout": "vertical", "spacing": "none", "paddingAll": "16px",
            "contents": [
    { "type": "text", "text": "吳明憲  Steve", "size": "lg", "color": "#16233D", "weight": "bold", "wrap": true, "margin": "none", "align": "start" },
    { "type": "text", "text": "莫凡彼沙發工藝　負責人", "size": "xs", "color": "#6B7280", "weight": "regular", "wrap": true, "margin": "sm", "align": "start" },
    { "type": "separator", "margin": "md", "color": "#E6E0D4" },
    { "type": "text", "text": "生活沒有標準尺寸", "size": "xl", "color": "#16233D", "weight": "bold", "wrap": true, "margin": "md", "align": "start" },
    { "type": "text", "text": "沙發也不該只有標準答案", "size": "md", "color": "#A96B3C", "weight": "bold", "wrap": true, "margin": "xs", "align": "start" },
    { "type": "text", "text": "沙發訂製　·　展售批發　·　專業諮詢", "size": "xs", "color": "#6B7280", "weight": "regular", "wrap": true, "margin": "md", "align": "start" }
  ]},
  "footer": { "type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "12px",
              "contents": [
    { "type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
      { "type": "button", "style": "primary", "color": "#16233D", "action": { "type": "uri", "label": "官方網站", "uri": "https://example.com" } },
      { "type": "button", "style": "primary", "color": "#A96B3C", "action": { "type": "uri", "label": "LINE 諮詢", "uri": "https://line.me/ti/p/~example" } },
      { "type": "button", "style": "primary", "color": "#16233D", "action": { "type": "uri", "label": "導航門市", "uri": "https://www.google.com/maps/search/?api=1&query=..." } }
    ]},
    { "type": "button", "style": "secondary",
      "action": { "type": "uri", "label": "分享給好友", "uri": "https://liff.line.me/2011897701-TrLfDuwi?share=1" } }
  ]}
}
```

> 註：image URL 開頭為 `https://`，尺寸 1040×676 JPEG、約 60 KB，可從瀏覽器正常取得（HTTP 200 / `image/jpeg`）。

## 附錄 C：已排除項目的技術細節

* **carousel 張數**：7 張（上限 12）✅
* **bubble 寬度一致**：皆為 `mega` ✅
* **`messages` 陣列上限**：官方 5 則，實測送 1 則 ✅
* **每個 bubble 的 JSON 大小**：官方上限 30 KB，實際約 2.5 KB ✅
* **整體訊息大小**：官方 Flex 上限 50 KB，實際 17.6 KB ✅
* **image 規格**：https、JPEG、60 KB（上限 10 MB）✅
* **action 型別**：全部是 `uri`（shareTargetPicker 只允許 URI action）✅
* **按鈕屬性**：只留 `type` / `style` / `color` / `action` ✅
* **`type` 欄位**：以自寫驗證器掃過整份 payload，無缺漏 ✅


---

# 【重要更新 2026-10-07 12:30】找到真正的原因了

## 新證據：`liff.sendMessages()` 會回報真正的錯誤

原本 `shareTargetPicker` 只回 `{status:"success"}` 就靜默丟棄，查不出原因。改用 `liff.sendMessages()`（同樣的 Flex 規格、不同通道）後：

1. 第一次錯誤：`The permission is not in LIFF app scope.`
   → LIFF app 的 **Scopes 沒勾 `chat_message.write`**。到 Console → LINE Login channel → LIFF → Scopes 勾選後 Update。
2. 補上 scope 後的真實錯誤：**`(code: INVALID_MESSAGE) invalid message`**
   → **訊息本身不合法**，所以不是限流、不是帳號問題。

## 元凶：`action.uri` 含空格／全形字元

正式版 payload 裡有三顆按鈕的 URI 是佔位符：

```json
"uri": "https://【官網網址】"
"uri": "https://line.me/ti/p/~【個人LINE ID】"   ← 含半形空格 + 全形括號
```

`https://line.me/ti/p/~【個人LINE ID】` **URI 內有空格**，在 URI 語法上就是不合法。LINE 的渲染器會容忍（所以極簡卡在 picker 路徑下能顯示），但**驗證器會直接判定整則訊息 invalid**。已全部換成合法網址。

同時也解釋了先前的一大堆矛盾：picker 路徑「回報成功但沒有卡片」，是因為訊息被驗證器擋掉後**靜默丟棄**，而 picker 不把錯誤回報給前端。

## 修改內容

`build_flex.py` 的 `LINKS` 全部改成合法 URI：

```python
LINKS = {
    "site":  "https://ericlin1994.github.io/movenpick-card/",
    "line":  "https://liff.line.me/2011897701-TrLfDuwi",
    "map":   "https://www.google.com/maps/search/?api=1&query=%E8%8E%AB%E5%87%A1%E5%BD%BC%E7%85%89%E7%99%BC%E5%B7%A5%E8%97%9D",
    "share": "https://liff.line.me/2011897701-TrLfDuwi?share=1",
}
```

`validate_flex.py` 新增 **URI 稽核**：掃描所有 `action.uri`，命中 `[\s\u3000\uFF00-\uFFEF]` 就擋下不部署。

```
✓ 結構驗證通過：7 張卡、17707 bytes、無缺漏 type、按鈕屬性乾淨
✓ URI 檢查通過
```

## 給 reviewer 的問題（更新版）

1. 除了 URI，還有哪個欄位會讓 LINE 判 `INVALID_MESSAGE` 但一般驗證器抓不出來？
2. `shareTargetPicker` 是否有任何方式可以取得「為什麼被丟棄」的原因？（目前只知道它 silent）
3. 在 picker 路徑下，URI 不合法是否**一定**會導致整則訊息被丟棄（而非只讓那顆按鈕失效）？


---

# 【結案 2026-10-07 03:40】已完全解決

## 根因確認
`action.uri` 含半形空格／全形字元（`https://line.me/ti/p/~【個人LINE ID】`）→ LINE 判定整則訊息 `INVALID_MESSAGE` → `shareTargetPicker` **靜默丟棄**（只回 `{status:"success"}`）。
改用合法 URI 後，**7 張 carousel 完整送達**。

## 另外兩個關鍵設定（缺一不可）
1. LIFF app 的 **Scopes 要勾 `chat_message.write`**，否則 `liff.sendMessages()` 報 `The permission is not in LIFF app scope.`
2. `liff.sendMessages()` **會回報真正的錯誤**（`INVALID_MESSAGE` 等），而 `shareTargetPicker()` 不會 → **除錯一律先用 sendMessages 驗證 payload 合法性**。

## 最終架構
- 卡片按鈕「分享給好友」→ `https://liff.line.me/{liffId}?share=1` → LIFF 頁面載入後**自動呼叫 `liff.shareTargetPicker()`**，收件者一鍵即可再轉發（實測有效，官方條件只有「已登入＋Console 已 Enable」，無手勢要求）。
- LIFF 頁面加 `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">`，否則 LINE 內建瀏覽器的快取會讓使用者以為「修好了還是舊行為」。

## 給 reviewer 的最終問題
1. 除了 URI，還有哪些欄位錯誤會造成 `INVALID_MESSAGE` 但一般結構驗證器抓不出來？（建議做一份檢查清單）
2. `shareTargetPicker` 有沒有任何方法取得「被丟棄的原因」？（目前確認它只會 silent success）
