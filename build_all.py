#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一鍵重建（換客戶流程）
------------------------------------------------
  1. 改 client.json
  2. python build_all.py            ← 產生圖片、Flex 卡片、內嵌 payload、重建一頁式網頁
  3. python validate_flex.py flex-cards.json   ← 最後把關（build_flex 已自動跑過一次）
  4. git add -A && git commit -m "換客戶：<名稱>" && git push
"""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
STEPS = ["gen_cards.py", "build_flex.py", "rebuild_page.py"]

if __name__ == "__main__":
    for s in STEPS:
        print(f"──── {s} ────")
        r = subprocess.run([sys.executable, str(HERE / s)],
                           capture_output=True, text=True, encoding="utf-8")
        out = (r.stdout or "").strip()
        err = (r.stderr or "").strip()
        if out:
            print(out)
        if r.returncode != 0:
            print(err or "(no stderr)")
            raise SystemExit(f"✗ {s} 失敗，中止（後續步驟未執行）")
    print("\n✅ 全部完成。檢查 git diff 後再 push。")
