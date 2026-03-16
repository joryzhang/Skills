---
name: asr-funasr
description: Transcribe local audio files (m4a/mp3/wav) to text using FunASR. Use when the user provides audio files and wants ASR/transcription output, or when another skill needs a consistent transcript JSON schema.
---

# ASR (FunASR)

## Quick Start
Run the script to transcribe and emit JSON:

```bash
/home/azureuser/.openclaw/workspace-Frame/.venv/bin/python \
  /home/azureuser/.openclaw/workspace-Frame/skills/asr-funasr/scripts/transcribe_funasr.py \
  --input /path/to/audio.m4a \
  --out /path/to/output.json
```

## Notes
- The script converts input to 16kHz mono WAV via ffmpeg.
- If the input directory is not writable, pass `--tmp-dir`.
- Default models target Chinese; override with `--model`, `--vad_model`, `--punc_model` as needed.

## Output Schema
See `references/schema.md` for the JSON schema.
