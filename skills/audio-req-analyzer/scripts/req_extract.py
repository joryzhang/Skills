#!/usr/bin/env python3
"""Extract requirement items from an ASR transcript JSON.

Usage:
  req_extract.py --input /path/to/asr.json --out /path/to/reqs.json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def simple_split(text: str):
    text = text.replace("。", "\n").replace("；", "\n").replace(";", "\n")
    text = re.sub(r"\n{2,}", "\n", text)
    parts = [p.strip() for p in text.splitlines()]
    return [p for p in parts if p]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="ASR JSON path")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    data = json.loads(in_path.read_text(encoding="utf-8"))
    text = data.get("text", "").strip()

    output = {
        "input": str(in_path),
        "text": text,
        "requirement_splits": simple_split(text),
    }

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
