#!/usr/bin/env python3
"""ElevenLabs narration. Set ELEVENLABS_API_KEY in a secret (never in repository files)."""
import argparse,json,os
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
SCENES=json.loads((ROOT/"lesson"/"narration.json").read_text())
OUT=ROOT/"outputs"/"audio"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--voice-id",default=os.environ.get("ELEVENLABS_VOICE_ID","pNInz6obpgDQGcFmaJgB"))
    args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    key=os.environ.get("ELEVENLABS_API_KEY")
    if not key and not args.dry_run:raise SystemExit("Add ELEVENLABS_API_KEY as a private Codespaces secret.")
    for i,scene in enumerate(SCENES,1):
        dest=OUT/f"{i:02d}_{scene['id']}.mp3"
        if args.dry_run:print("Dry run:",dest.name,len(scene["text"]),"characters");continue
        if dest.exists():print("Existing:",dest.name);continue
        resp=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{args.voice_id}",headers={"xi-api-key":key,"Content-Type":"application/json"},params={"output_format":"mp3_44100_128"},json={"text":scene["text"],"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.55,"similarity_boost":0.78}},timeout=120)
        resp.raise_for_status()
        if len(resp.content)<1000:raise RuntimeError("Unexpected empty audio for "+scene["id"])
        dest.write_bytes(resp.content);print("Generated",dest.name)
if __name__=="__main__":main()
