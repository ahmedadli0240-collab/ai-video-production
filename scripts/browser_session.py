#!/usr/bin/env python3
"""Open genuine QuickBooks and ChatGPT in cloud Chromium. Human performs authentication and file-upload checkpoints."""
import argparse
from pathlib import Path
import re
import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs"
QBO="https://qbo.intuit.com/redir/testdrive"
CHATGPT="https://chatgpt.com/"

def click_one(page,name):
    for locate in (page.get_by_role("link",name=re.compile("^"+re.escape(name)+"$",re.I)),page.get_by_role("button",name=re.compile("^"+re.escape(name)+"$",re.I))):
        try:
            if locate.count()==1 and locate.first.is_visible():
                locate.first.click(timeout=4000)
                return True
        except Exception: pass
    return False

def clipboard(path):
    print("\nPaste this actual prompt into the real ChatGPT:\n",path.read_text())
    try:
        subprocess.run(["xclip","-selection","clipboard"],input=path.read_bytes(),check=True,timeout=6)
        print("Prompt copied to cloud clipboard.")
    except Exception: print("Clipboard unavailable. Open the prompt file and copy its text manually.")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--autonav",action="store_true")
    args=parser.parse_args()
    (OUT/"downloads").mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        ctx=p.chromium.launch_persistent_context(user_data_dir=str(OUT/"profile"),headless=False,viewport={"width":1600,"height":900},accept_downloads=True,downloads_path=str(OUT/"downloads"),args=["--no-first-run","--disable-notifications"],slow_mo=120)
        q=ctx.pages[0] if ctx.pages else ctx.new_page()
        def downloaded(d):
            destination=OUT/"downloads"/Path(d.suggested_filename).name
            try: d.save_as(str(destination));print("Saved actual browser download:",destination)
            except Exception as exc:print("Download failed:",exc)
        ctx.on("download",downloaded)
        try:q.goto(QBO,wait_until="domcontentloaded",timeout=60000)
        except PWTimeout:print("QuickBooks loading slowly; continue manually.")
        chat=ctx.new_page()
        try:chat.goto(CHATGPT,wait_until="domcontentloaded",timeout=60000)
        except PWTimeout:print("ChatGPT loading slowly; continue manually.")
        print("\nSIGN IN to ChatGPT before recording. Never record login credentials or share a password.")
        input("Press Enter once signed in and QuickBooks demo is accessible... ")
        q.bring_to_front()
        input("Start screen capture in the other terminal, mark intro, then press Enter... ")
        if args.autonav:
            for name in ("Reports","Standard reports","Profit and Loss"):
                if click_one(q,name):print("Clicked",name)
                else:print("Could not uniquely locate",name,"— use the real browser manually.")
                q.wait_for_timeout(1000)
        print("Choose a report period with transactions, confirm basis, then export to Excel.")
        input("Press Enter AFTER the REAL QuickBooks Excel export is downloaded... ")
        print("Downloads:",*[str(f) for f in (OUT/"downloads").glob("*")],sep="\n ")
        chat.bring_to_front()
        clipboard(ROOT/"lesson"/"analysis_prompt.txt")
        print("Upload the real QuickBooks Excel file using the actual ChatGPT website. Submit the prompt. Manually verify totals.")
        input("Press Enter once ChatGPT's actual answer is visible and checked... ")
        clipboard(ROOT/"lesson"/"followup_prompt.txt")
        print("Paste and submit follow-up; show final result.")
        input("Press Enter once the result is ready... ")
        print("Stop screen capture from the other terminal. Browser remains open until you confirm.")
        input("Press Enter to close the browser session... ")
        ctx.close()

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:print("Browser stopped by operator.")
