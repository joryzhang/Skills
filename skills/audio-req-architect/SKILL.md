---
name: audio-req-architect
description: Transcribe local audio files (m4a/mp3/wav) with FunASR, then summarize and split requirements from the transcript. Use when the user provides an audio file and wants requirement extraction, architecture suggestions, or follow-up questions based on spoken content.
---

# Audio Req Architect

## Overview
Transcribe audio to text with FunASR, then structure the content into requirement items and draft implementation steps/questions.

## Workflow
1. **Transcribe audio** using the bundled script.
2. **Review transcript** and clean obvious errors if needed.
3. **Split requirements** and group into functional/non-functional items.
4. **Draft implementation plan** and ask clarifying questions.

## Transcription (FunASR)
Use the script in `scripts/transcribe_and_analyze.py`.

```bash
/home/azureuser/.openclaw/workspace-Frame/.venv/bin/python \
  /home/azureuser/.openclaw/workspace-Frame/skills/audio-req-architect/scripts/transcribe_and_analyze.py \
  --input /path/to/audio.m4a \
  --out /path/to/output.json
```

### Notes
- The script converts audio to 16kHz mono WAV via ffmpeg before ASR.
- Default models are Chinese; override `--model`, `--vad_model`, `--punc_model` if needed.
- The JSON output includes `text` and a naive `requirement_splits` list for quick review.

## Output Expectations
- Provide the transcript.
- Provide split requirements (functional + constraints).
- Provide a short implementation plan.
- Ask clarifying questions.
