# ASR Output Schema

```json
{
  "input": "/abs/path/to/audio.m4a",
  "text": "full transcript",
  "models": {
    "asr": "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    "vad": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    "punc": "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"
  }
}
```

Notes:
- `text` is the full transcript with punctuation.
- If you need timestamps or diarization later, extend the script with segment output.
