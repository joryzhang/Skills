---
name: audio-req-analyzer
description: Analyze ASR transcript JSON (from asr-funasr) to split requirements and produce a structured list for follow-up architecture or implementation planning. Use when the user wants requirement extraction from audio transcripts.
---

# Audio Requirement Analyzer

## Quick Start

```bash
/home/azureuser/.openclaw/workspace-Frame/.venv/bin/python \
  /home/azureuser/.openclaw/workspace-Frame/skills/audio-req-analyzer/scripts/req_extract.py \
  --input /path/to/asr.json \
  --out /path/to/reqs.json
```

## Workflow
1. Run `asr-funasr` to generate transcript JSON.
2. Run `req_extract.py` to generate a naive requirement list.
3. Review and refine into functional/non-functional requirements, constraints, and open questions.

## Output Schema
See `references/schema.md`.
