#!/usr/bin/env python3
"""One-command guided recording of the REAL QuickBooks and ChatGPT websites.

All authentication is completed privately before capture starts. This is intentionally
human-in-the-loop: accounts, downloads and financial claims require verification.
"""
import os
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PwTimeoutError

sys.path.insert(0,str(Path(__file__).resolve().parent))
from record import start as start_capture, mark as mark_capture, stop as stop_capture

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs"
QBO="https://qbo.intuit.com/redir/testdrive"
CHATGPT="https://chatgpt.com/"

def cue(message):
    print("\n"+"="*72+"\n"+message+"\n"+"="*72,flush=True)
    input("PRESS ENTER to continue... ")

def navigate(page,labels):
    for name in labels:
        attempts=[page.get_by_role("link",name=re.compile(r"^"+re.escape(name)+r"$",re.I)),
                  page.get_by_role("button",name=re.compile(r"^"+re.escape(name)+r"$",re.I))]
        clicked=False
        for locator in attempts:
            try:
                if locator.count()==1 and locator.first.is_visible():
                    locator.first.click(timeout=4000); clicked=True;break
            except Exception:pass
        print(("Opened" if clicked else "Please open manually")+": "+name)
        page.wait_for_timeout(900)

def submit_prompt(chat,filepath):
    """Visible interaction only. If the current ChatGPT UI differs, fall back to manual."""
    prompt=filepath.read_text(encoding="utf-8")
    for selector in ("[contenteditable='true'][data-placeholder]","[contenteditable='true'][role='textbox']","#prompt-textarea","[contenteditable='true']"):
        try:
            loc=chat.locator(selector)
            if loc.count()!=1 or not loc.first.is_visible():continue
            loc.first.fill(prompt,timeout=3500)
            loc.first.press("Enter",timeout=3500)
            print("Submitted actual prompt via browser UI.")
            return True
        except Exception:pass
    print("Could not uniquely locate the current ChatGPT composer.")
    print("Copy and submit the prompt manually from",filepath)
    return False

def upload_file(chat,report):
    """Upload ONLY through visible, authenticated ChatGPT browser UI."""
    try:
        items=chat.locator("input[type=file]")
        if items.count()==1:
            items.first.set_input_files(str(report),timeout=7000)
            print("Attached original report:",report.name)
            return True
    except Exception as exc:
        print("Automatic file upload was not available:",exc)
    print("Attach this Excel file manually in ChatGPT:",report)
    return False

def new_export_since(start_at):
    allowed=(".xlsx",".xls",".csv")
    files=[f for f in (OUT/"downloads").glob("*") if f.is_file() and f.suffix.lower() in allowed]
    files=[f for f in files if f.stat().st_mtime>start_at-3]
    return max(files,key=lambda f:f.stat().st_mtime) if files else None

def main():
    (OUT/"downloads").mkdir(exist_ok=True,parents=True)
    (OUT/"profile").mkdir(exist_ok=True,parents=True)
    if (OUT/"real_sites_capture.mkv").exists():
        raise SystemExit("A previous recording exists. Download or rename outputs/real_sites_capture.mkv before re-recording.")
    with sync_playwright() as p:
        context=p.chromium.launch_persistent_context(
            user_data_dir=str(OUT/"profile"),headless=False,
            viewport={"width":1600,"height":900},
            accept_downloads=True,downloads_path=str(OUT/"downloads"),
            args=["--no-first-run","--disable-notifications"],slow_mo=80)
        q=context.pages[0] if context.pages else context.new_page()
        chat=context.new_page()
        try:
            q.goto(QBO,wait_until="domcontentloaded",timeout=60000)
        except PwTimeoutError:print("QuickBooks may still be loading.")
        try:
            chat.goto(CHATGPT,wait_until="domcontentloaded",timeout=60000)
        except PwTimeoutError:print("ChatGPT may still be loading.")
        cue("BEFORE RECORDING: Sign into ChatGPT in the cloud desktop. Confirm the demo QuickBooks company is accessible. No passwords will be recorded.")
        q.bring_to_front()
        cue("READY TO FILM: Close menus and popups, maximize the cloud Chromium window, and confirm the QuickBooks screen is visible. Recording begins AFTER you press Enter.")
        recording=False
        try:
            start_capture();recording=True
            mark_capture("intro");q.wait_for_timeout(4000)
            mark_capture("quickbooks")
            navigate(q,["Reports","Standard reports","Profit and Loss"])
            cue("In the real QuickBooks browser: open the Profit and Loss report, choose a period with transactions and verify the accounting basis. Keep the report visible.")
            mark_capture("export")
            started=time.time()
            cue("Export the ORIGINAL Profit and Loss report to Excel in QuickBooks. Do not make up a replacement report. Press Enter only after the download completes.")
            report=new_export_since(started)
            if not report:
                candidates=sorted((OUT/"downloads").glob("*"),key=lambda f:f.stat().st_mtime,reverse=True)
                report=next((f for f in candidates if f.suffix.lower() in (".xlsx",".xls",".csv")),None)
            if not report:
                raise RuntimeError("No genuine downloaded Excel/CSV report found. Recording stopped; review the QuickBooks export.")
            mark_capture("chatgpt")
            chat.bring_to_front()
            if not upload_file(chat,report):
                cue("Attach the genuine exported report to ChatGPT before continuing.")
            cue("Confirm ChatGPT has the actual Excel report attached. Next, the analysis prompt will be entered.")
            sent=submit_prompt(chat,ROOT/"lesson"/"analysis_prompt.txt")
            if not sent:cue("Paste and submit the analysis prompt from lesson/analysis_prompt.txt.")
            cue("Allow ChatGPT to finish its REAL analysis. Check its reported totals against QuickBooks and scroll through the actual result on screen.")
            mark_capture("analysis")
            cue("Continue showing the real analysis on-screen, including verified figures and any charts. Then continue to the follow-up.")
            mark_capture("followup")
            sent=submit_prompt(chat,ROOT/"lesson"/"followup_prompt.txt")
            if not sent:cue("Paste and submit the follow-up prompt from lesson/followup_prompt.txt.")
            cue("Wait for the REAL 30-day action-plan response. Show its recommendations and check they do not invent savings or facts.")
            mark_capture("outro");chat.wait_for_timeout(5000)
            stop_capture();recording=False
            print("\nSUCCESS: genuine website footage captured.")
            print("Next: add ELEVENLABS_API_KEY as a Codespaces secret, then run:")
            print("  python scripts/narrate.py")
            print("  python scripts/assemble.py")
            print("Output: outputs/QuickBooks_ChatGPT_REAL_Platform_Lesson.mp4")
        finally:
            if recording:
                print("Recording interrupted; stopping safely.")
                stop_capture()
            context.close()

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:print("Interrupted by operator.")
