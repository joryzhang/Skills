#!/usr/bin/env python3
"""Transcribe audio with FunASR and emit JSON.

Supports m4a/mp3/wav via ffmpeg conversion to 16kHz mono wav.

Usage:
  transcribe_funasr.py --input <audio.m4a> --out <output.json>

Optional:
  --model <asr model>
  --vad_model <vad model>
  --punc_model <punc model>
  --device <cpu|cuda>
  --tmp-dir <dir>   # if input dir is not writable
"""

import argparse
import json
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to audio file (m4a/mp3/wav)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--model", default="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
    parser.add_argument("--vad_model", default="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch")
    parser.add_argument("--punc_model", default="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--tmp-dir", default="")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    tmp_dir = Path(args.tmp_dir).expanduser().resolve() if args.tmp_dir else input_path.parent
    tmp_dir.mkdir(parents=True, exist_ok=True)

    tmp_wav = tmp_dir / (input_path.stem + ".tmp.16k.wav")
    convert_to_wav(input_path, tmp_wav)

    from funasr import AutoModel

    model = AutoModel(
        model=args.model,
        vad_model=args.vad_model,
        punc_model=args.punc_model,
        device=args.device,
        disable_update=True,
    )

    res = model.generate(input=str(tmp_wav), batch_size_s=300)
    text = res[0].get("text", "").strip()

    output = {
        "input": str(input_path),
        "text": text,
        "models": {
            "asr": args.model,
            "vad": args.vad_model,
            "punc": args.punc_model,
        },
    }

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

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
