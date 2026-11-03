#!/usr/bin/env python3
"""Genuine desktop capture with chapter markers. Requires Codespaces desktop X display."""
import argparse,json,os,re,signal,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"outputs"
STATE=OUT/"recording.json";MARKS=OUT/"markers.json";RAW=OUT/"real_sites_capture.mkv"

def state():
    if not STATE.exists():raise SystemExit("No recording. Start first: python scripts/record.py start")
    return json.loads(STATE.read_text())
def alive(pid):
    try:os.kill(pid,0);return True
    except ProcessLookupError:return False

def start():
    OUT.mkdir(parents=True,exist_ok=True)
    if STATE.exists():
        previous=state()
        if not previous.get("stopped_at") and alive(previous["pid"]):raise SystemExit("Recording already running.")
    if RAW.exists():raise SystemExit("Move aside the existing raw capture before re-recording: "+str(RAW))
    display=os.environ.get("DISPLAY",":1")
    display=display if "." in display else display+".0"
    info=subprocess.run(["xdpyinfo","-display",display],capture_output=True,text=True)
    match=re.search(r"dimensions:\s*(\d+)x(\d+)\s+pixels",info.stdout)
    if not match:raise SystemExit("Cannot find active graphical desktop. Check Codespaces noVNC and DISPLAY.")
    w,h=map(int,match.groups())
    log=(OUT/"ffmpeg.log").open("wb")
    cmd=["ffmpeg","-hide_banner","-loglevel","warning","-y","-f","x11grab","-draw_mouse","1","-framerate","30","-video_size",f"{w}x{h}","-i",display,"-an","-c:v","libx264","-preset","ultrafast","-crf","19","-pix_fmt","yuv420p",str(RAW)]
    p=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    time.sleep(1)
    if p.poll() is not None:raise SystemExit("FFmpeg failed. Inspect outputs/ffmpeg.log.")
    STATE.write_text(json.dumps({"pid":p.pid,"started_at":time.time(),"resolution":[w,h],"display":display},indent=2))
    MARKS.write_text("[]\n")
    print("Recording",w,h,"at",display,"PID",p.pid)

def mark(name):
    s=state()
    if s.get("stopped_at") or not alive(s["pid"]):raise SystemExit("Capture no longer running.")
    if not re.fullmatch("[a-z][a-z0-9_-]*",name):raise SystemExit("Invalid marker.")
    marks=json.loads(MARKS.read_text())
    if marks and marks[-1]["id"]==name:raise SystemExit("Consecutive duplicate marker.")
    marks.append({"id":name,"at":round(time.time()-s["started_at"],3)})
    MARKS.write_text(json.dumps(marks,indent=2));print(name,marks[-1]["at"])

def stop():
    s=state()
    if s.get("stopped_at"):print("Already stopped.");return
    marks=json.loads(MARKS.read_text())
    if not marks or marks[-1]["id"]!="end":
        marks.append({"id":"end","at":round(time.time()-s["started_at"],3)})
        MARKS.write_text(json.dumps(marks,indent=2))
    if alive(s["pid"]):os.kill(s["pid"],signal.SIGINT)
    s["stopped_at"]=time.time();STATE.write_text(json.dumps(s,indent=2))
    print("Stopped. Raw footage:",RAW)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("action",choices=["start","mark","stop","status"]);ap.add_argument("name",nargs="?")
    a=ap.parse_args()
    if a.action=="start":start()
    elif a.action=="mark":
        if not a.name:ap.error("mark requires a scene name")
        mark(a.name)
    elif a.action=="stop":stop()
    else:print(json.dumps(state(),indent=2))
if __name__=="__main__":main()
