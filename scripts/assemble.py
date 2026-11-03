#!/usr/bin/env python3
"""Render an authentic screen recording and separately recorded TTS segments to 1080p MP4."""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"outputs"
SCENES=json.loads((ROOT/"lesson"/"narration.json").read_text())
def call(a):subprocess.run(a,check=True)
def seconds(path):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],capture_output=True,text=True,check=True)
    return float(p.stdout.strip())
def clock(t):
    ms=max(0,round(t*1000));h,rem=divmod(ms,3600000);m,rem=divmod(rem,60000);s,rem=divmod(rem,1000)
    return f"{h:02d}:{m:02d}:{s:02d},{rem:03d}"
def main():
    video=OUT/"real_sites_capture.mkv";markerfile=OUT/"markers.json"
    if not video.exists() or not markerfile.exists():raise SystemExit("Record the REAL websites and scene markers first.")
    marks=json.loads(markerfile.read_text());want=[x["id"] for x in SCENES]+["end"]
    if [m["id"] for m in marks]!=want:raise SystemExit(f"Required markers: {want}; recorded: {[m['id'] for m in marks]}")
    if marks[-1]["at"]>seconds(video)+3:raise SystemExit("Markers extend beyond capture duration.")
    clips=OUT/"clips";clips.mkdir(exist_ok=True,parents=True)
    parts=[];subtitles=[];timeline=0
    for i,scene in enumerate(SCENES,1):
        a=marks[i-1]["at"];b=marks[i]["at"];original=b-a
        if original<2:raise SystemExit("Scene too short: "+scene["id"])
        voice=OUT/"audio"/f"{i:02d}_{scene['id']}.mp3"
        if not voice.exists():raise SystemExit("Missing male voice clip: "+str(voice))
        narration=seconds(voice);target=narration+1.1
        factor=target/original if original>=target*0.8 else 1
        pad=max(.12,target-original*factor+.2)
        if original>target*2.3:print("Review accelerated scene:",scene["id"])
        clip=clips/f"{i:02d}_{scene['id']}.mp4"
        filtergraph=f"[0:v]setpts=(PTS-STARTPTS)*{factor:.8f},fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,tpad=stop_mode=clone:stop_duration={pad:.4f},trim=duration={target:.4f},setsar=1[v];[1:a]aresample=48000,apad=pad_dur=2,atrim=duration={target:.4f}[a]"
        call(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{a:.3f}","-t",f"{original:.3f}","-i",str(video),"-i",str(voice),"-filter_complex",filtergraph,"-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","160k","-t",f"{target:.4f}",str(clip)])
        parts.append(clip)
        chunks=[x.strip() for x in re.split(r"(?<=[.!?])\s+",scene["text"]) if x.strip()]
        total=sum(max(1,len(x.split())) for x in chunks)
        cursor=timeline
        for chunk in chunks:
            dur=narration*max(1,len(chunk.split()))/total
            if dur>=1:subtitles.append((cursor,cursor+dur,chunk))
            cursor+=dur
        timeline+=target
    concat=clips/"concat.txt"
    concat.write_text("".join("file '"+p.name+"'\n" for p in parts))
    output=OUT/"QuickBooks_ChatGPT_REAL_Platform_Lesson.mp4"
    call(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(output)])
    srt=OUT/"QuickBooks_ChatGPT_REAL_Platform_Lesson.srt"
    srt.write_text("".join(f"{i}\n{clock(a)} --> {clock(b)}\n{t}\n\n" for i,(a,b,t) in enumerate(subtitles,1)),encoding="utf-8")
    print("Done:",output,"\nCaption review required:",srt)
if __name__=="__main__":main()
