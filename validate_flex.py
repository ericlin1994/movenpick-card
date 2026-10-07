#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Flex Message 結構 + 值域 驗證器
用法：python validate_flex.py flex-cards.json

為什麼需要它：LINE 對不合法的 Flex 會「靜默丟棄」整則訊息——
shareTargetPicker 只回 success、sendMessages 才給 INVALID_MESSAGE，
所以上線前一定要先在本地把所有不合法的值擋下來。
"""
import json, re, sys, pathlib

SIZES = {"xxs", "xs", "sm", "md", "lg", "xl", "xxl", "3xl", "4xl", "5xl", "full"}
WEIGHTS = {"regular", "bold"}
LAYOUTS = {"vertical", "horizontal", "baseline"}
BTN_STYLES = {"primary", "secondary", "link"}
ALIGNS = {"start", "center", "end"}
SPACINGS = {"none", "xs", "sm", "md", "lg", "xl", "xxl"}
ACTIONS = {"uri", "message", "postback", "datetimepicker", "camera", "cameraRoll",
           "location", "clipboard", "richmenuswitch"}
COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
LENGTH_RE = re.compile(r"^(\d+(\.\d+)?(px|%))$")
URI_ILLEGAL = re.compile(r"[\s\u3000\uFF00-\uFFEF\u4e00-\u9fff]")


def main():
    p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "flex-cards.json")
    payload = json.loads(p.read_text(encoding="utf-8"))
    errs = []

    # ── 頂層 ──
    if payload.get("type") != "flex":
        errs.append("最外層 type 必須是 flex")
    if not payload.get("altText"):
        errs.append("缺少 altText")
    contents = payload.get("contents", {})
    if contents.get("type") not in ("bubble", "carousel"):
        errs.append("contents.type 必須是 bubble 或 carousel")
    bubbles = contents.get("contents", []) if contents.get("type") == "carousel" else [contents]
    if not bubbles:
        errs.append("沒有任何卡片")
    if len(bubbles) > 12:
        errs.append(f"carousel 超過 12 張（{len(bubbles)}）")

    allowed = {"type", "text", "size", "weight", "color", "wrap", "margin", "align",
               "flex", "maxLines", "action", "contents", "layout", "spacing", "paddingAll",
               "paddingStart", "paddingEnd", "paddingTop", "paddingBottom", "backgroundColor",
               "cornerRadius", "borderWidth", "borderColor", "style", "label", "uri",
               "aspectRatio", "aspectMode", "url", "hero", "body", "footer", "altText",
               "maxWidth", "maxHeight", "scaling", "height", "justifyContent", "alignItems",
               "position", "offsetTop", "offsetBottom", "offsetStart", "offsetEnd",
               "animation", "width", "gravity", "adjustMode"}

    def walk(node, path, in_hbox=False):
        if isinstance(node, list):
            for i, x in enumerate(node):
                walk(x, f"{path}[{i}]", in_hbox)
            return
        if not isinstance(node, dict):
            return
        typ = node.get("type")
        if "type" not in node and "contents" in node:
            errs.append(f"{path} 缺少 type")
        for k in node:
            if k not in allowed:
                errs.append(f"{path} 出現未知屬性 {k}（可能是拼錯，LINE 會整則丟掉）")

        if typ == "text":
            if not isinstance(node.get("text"), str):
                errs.append(f"{path} text 必須是字串")
            if "size" in node and node["size"] not in SIZES:
                errs.append(f"{path} size={node['size']} 不合法")
            if "weight" in node and node["weight"] not in WEIGHTS:
                errs.append(f"{path} weight={node['weight']} 不合法")
            if "align" in node and node["align"] not in ALIGNS:
                errs.append(f"{path} align={node['align']} 不合法")
        elif typ == "box":
            if node.get("layout") not in LAYOUTS:
                errs.append(f"{path} layout={node.get('layout')} 不合法")
            for k in ("paddingAll", "paddingStart", "paddingEnd", "paddingTop", "paddingBottom"):
                if k in node and not LENGTH_RE.match(str(node[k])):
                    errs.append(f"{path} {k}={node[k]} 必須是 px 或 %（關鍵字值不合法）")
            if "cornerRadius" in node and not LENGTH_RE.match(str(node["cornerRadius"])):
                errs.append(f"{path} cornerRadius={node['cornerRadius']} 必須是 px 或 %")
            if "spacing" in node and node["spacing"] not in SPACINGS:
                errs.append(f"{path} spacing={node['spacing']} 不合法")
        elif typ == "button":
            if node.get("style") and node["style"] not in BTN_STYLES:
                errs.append(f"{path} button.style={node['style']} 不合法")
            for bad in ("height", "margin", "scaling", "flex"):
                if bad in node:
                    errs.append(f"{path} button 不可有 {bad}（實測會讓整則訊息被靜默丟棄）")
            if node.get("style") == "link" and "color" not in node:
                pass  # link 沒給 color 也可以（用預設）
        elif typ == "image":
            if not str(node.get("url", "")).startswith("https://"):
                errs.append(f"{path} 圖片 url 必須是 https")
        elif typ == "separator":
            pass

        if "color" in node and not COLOR_RE.match(str(node["color"])):
            errs.append(f"{path} color={node['color']} 不是 #RRGGBB")
        if "backgroundColor" in node and not COLOR_RE.match(str(node["backgroundColor"])):
            errs.append(f"{path} backgroundColor={node['backgroundColor']} 不是 #RRGGBB")
        if "borderColor" in node and not COLOR_RE.match(str(node["borderColor"])):
            errs.append(f"{path} borderColor={node['borderColor']} 不是 #RRGGBB")
        if "margin" in node and not (node["margin"] in SPACINGS or LENGTH_RE.match(str(node["margin"]))):
            errs.append(f"{path} margin={node['margin']} 不合法")
        if "flex" in node and not isinstance(node["flex"], int):
            errs.append(f"{path} flex 必須是整數")

        # action
        act = node.get("action")
        if isinstance(act, dict):
            if act.get("type") not in ACTIONS:
                errs.append(f"{path} action.type={act.get('type')} 不合法")
            uri = act.get("uri")
            if uri is not None:
                if not str(uri).startswith(("https://", "http://", "tel:", "line:", "mailto:")):
                    errs.append(f"{path} action.uri 開頭不合法：{uri}")
                if URI_ILLEGAL.search(str(uri)):
                    errs.append(f"{path} action.uri 含空格／全形字元，LINE 會判 INVALID_MESSAGE：{uri}")
            if act.get("type") == "uri" and not act.get("label"):
                errs.append(f"{path} uri action 缺少 label")
            if isinstance(act.get("label"), str) and len(act["label"]) > 20:
                errs.append(f"{path} action.label 過長（≤20 字）")

        for k, v in node.items():
            if k in ("action",):
                continue
            if isinstance(v, (dict, list)):
                walk(v, f"{path}.{k}", node.get("layout") == "horizontal" and typ == "box")

    for i, b in enumerate(bubbles):
        if b.get("type") != "bubble":
            errs.append(f"第 {i+1} 張卡缺少 type: bubble")
        if "size" in b and b["size"] != "mega":
            errs.append(f"第 {i+1} 張卡 size 不是 mega（carousel 內寬度必須一致）")
        walk(b, f"bubble[{i}]")

    size = len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode())
    if errs:
        for e in errs[:40]:
            print("✗", e)
        print(f"\n共 {len(errs)} 個問題（{len(bubbles)} 張卡、{size} bytes）")
        sys.exit(1)
    print(f"✓ 結構驗證通過：{len(bubbles)} 張卡、{size} bytes、無缺漏 type、按鈕屬性乾淨、值域合法")
    print("✓ URI 檢查通過")
    if size > 50 * 1024:
        print(f"⚠️ 整包 {size} bytes 接近 LINE 50KB 上限")


if __name__ == "__main__":
    main()
