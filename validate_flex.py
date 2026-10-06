#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flex payload 結構驗證器
----------------------
把「回報成功但對方看不到」的常見結構錯誤擋在部署前。
用法：python validate_flex.py [payload.json]
"""
import json
import re, sys, pathlib

VALID_TYPES = {
    "flex", "bubble", "carousel", "box", "text", "image", "button", "separator",
    "icon", "span", "video", "filler",
}
REQUIRED = {
    "flex":     ["contents"],
    "bubble":   [],                     # body/footer 都可以沒有，但 type 一定要有
    "carousel": ["contents"],
    "box":      ["layout", "contents"],
    "text":     ["text"],
    "image":    ["url"],
    "button":   ["action"],
    "separator": [],
}
BAD_BUTTON_KEYS = ("height", "margin", "scaling")


def walk(node, path="root", problems=None):
    if problems is None:
        problems = []
    if isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f"{path}[{i}]", problems)
        return problems

    if isinstance(node, dict):
        t = node.get("type")
        if t is None:
            problems.append(f"{path}: 缺少 type（LINE 會回報成功但不顯示）")
        elif t not in VALID_TYPES:
            problems.append(f"{path}: 未知的 type={t!r}")
        else:
            for key in REQUIRED.get(t, []):
                if key not in node:
                    problems.append(f"{path} (type={t}): 缺少必要欄位 {key!r}")
        if t == "button":
            hit = [k for k in BAD_BUTTON_KEYS if k in node]
            if hit:
                problems.append(f"{path}: button 帶了會讓訊息被丟掉的屬性 {hit}")
        for k, v in node.items():
            if k == "action":          # action 不是元件，別往下檢查 type
                continue
            if isinstance(v, (dict, list)):
                walk(v, f"{path}.{k}", problems)
        return problems

    return problems


def main():
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "flex-cards.json")
    payload = json.loads(src.read_text(encoding="utf-8"))
    problems = walk(payload)

    # 額外檢查：carousel 內的每個 bubble 寬度要一致、張數上限
    contents = payload.get("contents", {})
    if contents.get("type") == "carousel":
        bubbles = contents["contents"]
        sizes = {b.get("size", "mega") for b in bubbles}
        if len(sizes) > 1:
            problems.append(f"carousel: bubble 寬度不一致 {sizes}")
        if len(bubbles) > 12:
            problems.append(f"carousel: {len(bubbles)} 張超過上限 12")

    if problems:
        print("✗ 發現", len(problems), "個問題：")
        for p in problems:
            print("   •", p)
        sys.exit(1)
    n = len(contents.get("contents", [])) if contents.get("type") == "carousel" else 1
    size = len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode())
    print(f"✓ 結構驗證通過：{n} 張卡、{size} bytes、無缺漏 type、按鈕屬性乾淨")


    # URI 檢查：URI 內不得有空格或全形字元（會被 LINE 判 invalid message）
    bad = []
    def _uri(n):
        if isinstance(n, dict):
            for k, x in n.items():
                if k == "uri" and isinstance(x, str):
                    if re.search(r"[\s\u3000\uFF00-\uFFEF\u4e00-\u9fff]", x):
                        bad.append(x)
                elif isinstance(x, (dict, list)):
                    _uri(x)
        elif isinstance(n, list):
            for x in n: _uri(x)
    _uri(payload)
    if bad:
        print("✗ URI 不合法（含空格／全形字元）:", bad[:3])
        sys.exit(1)
    print("✓ URI 檢查通過")

if __name__ == "__main__":
    main()
