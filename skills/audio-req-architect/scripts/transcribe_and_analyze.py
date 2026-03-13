#!/usr/bin/env python3
"""Transcribe an audio file with FunASR (m4a/mp3/wav) and emit text + simple requirement splits.

Usage:
  transcribe_and_analyze.py --input <audio.m4a> --out <output.json>

Notes:
- Converts input to 16kHz mono wav via ffmpeg before ASR.
- Default models target Chinese speech; override with flags if needed.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{proc.stderr}")
    return proc.stdout


def ensure_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found. Please install ffmpeg.")


def convert_to_wav(input_path: Path, wav_path: Path):
    ensure_ffmpeg()
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(wav_path),
    ]
    run(cmd)


def simple_split_requirements(text: str):
    """Very light heuristic split; real analysis should be done by the assistant."""
    # split by common delimiters and keep non-empty lines
    raw = [seg.strip() for seg in text.replace("。", "\n").replace("；", "\n").replace(";", "\n").splitlines()]
    items = [seg for seg in raw if seg]
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to audio file (m4a/mp3/wav)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--model", default="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
    parser.add_argument("--vad_model", default="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch")
    parser.add_argument("--punc_model", default="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    tmp_wav = input_path.with_suffix(".tmp.16k.wav")
    convert_to_wav(input_path, tmp_wav)

    from funasr import AutoModel

    model = AutoModel(
        model=args.model,
        vad_model=args.vad_model,
        punc_model=args.punc_model,
        device=args.device,
    )

    res = model.generate(input=str(tmp_wav), batch_size_s=300)
    text = res[0].get("text", "").strip()

    output = {
        "input": str(input_path),
        "wav": str(tmp_wav),
        "text": text,
        "requirement_splits": simple_split_requirements(text),
    }

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    # cleanup
    try:
        tmp_wav.unlink(missing_ok=True)
    except Exception:
        pass

    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
