# AI Finance Video Studio — Real QuickBooks + ChatGPT

Produce a course video using the **actual websites**, not recreated interfaces. Designed for GitHub Codespaces with a private noVNC desktop, a real Chromium browser, FFmpeg screen capture, optional ElevenLabs American-English male narration, and automatic MP4 editing.

**Status:** Source code and lesson workflow are ready. The real QuickBooks and ChatGPT recording has not been captured. You must start the Codespace and sign into ChatGPT interactively; the GitHub connector cannot launch Codespaces or operate the desktop.

## First-time setup

1. The repository can remain public if you wish. **Always keep the Codespaces port 6080 PRIVATE**, and never commit credentials, session cookies, financial exports, or recordings.
2. In GitHub, select **Code → Codespaces → Create codespace on main**. Allow the development container setup to finish.
3. Open the **Ports** tab → port **6080** → set visibility to **Private** → open in browser. The desktop password is specified in `.devcontainer/devcontainer.json`; access is additionally controlled by private Codespaces port permissions.
4. Open Codespaces terminal and run **`git pull --ff-only && python scripts/start_lesson.py`**. The guided script opens the REAL QuickBooks demo and chatgpt.com, assists with navigation, starts/stops recording, marks chapters, saves a genuine QuickBooks export, and attempts to attach it to ChatGPT and submit prompts. Sign into ChatGPT privately **before recording**. You still need to supervise QuickBooks report selection/export, any browser controls the automation cannot find, and the financial check. The script will ask you to press Enter at checkpoints.
5. Alternatively, after pulling code, use **Terminal → Run Task → Start AI Video Lesson — real QuickBooks and ChatGPT**. This does the same thing.
6. Check the genuine ChatGPT analysis and source QuickBooks totals for correctness. The script intentionally stops if the report export is missing rather than fabricating data.
7. Configure an **ELEVENLABS_API_KEY Codespaces secret**, **not in repository files**. Run `python scripts/narrate.py` to generate male narration (Adam voice; optional ELEVENLABS_VOICE_ID override). Then `python scripts/assemble.py` to render the final 1080p MP4 and an approximate subtitle SRT. An additional 'Generate male narration and render MP4' VS Code task is available.
8. Finished file: `outputs/QuickBooks_ChatGPT_REAL_Platform_Lesson.mp4`. Download it from the cloud environment; output files are gitignored.

## Recording safety

- This project does not fake QuickBooks or ChatGPT interfaces or claim financial results that were not verified.
- Keep port 6080 private; do not record login screens; never expose ElevenLabs or other API keys.
- ChatGPT login, some QuickBooks navigation, and financial verification are manual checkpoints. The automation intentionally does not bypass CAPTCHA or scrape ChatGPT responses.
- The demo company can reset. If exporting a genuine report is blocked, stop rather than substitute fabricated data.

## What's in this repository

- `.devcontainer/`: Codespaces desktop and Playwright runtime
- `scripts/start_lesson.py`: recommended single-command recording workflow (browser, downloads, prompts, chapter markers)
- `scripts/browser_session.py`: legacy manual-assisted browser session
- `scripts/record.py`: records actual desktop and marks video chapters
- `scripts/narrate.py`: ElevenLabs male AI voice from written lesson
- `scripts/assemble.py`: trims and aligns real video with voice, outputs MP4 and SRT
- `lesson/`: prompts, story outline, narration script and review checklist

Official sources: [Intuit test drive](https://quickbooks.intuit.com/learn-support/en-us/help-article/small-business-processes/test-drive-quickbooks-online/L9C12ODlA_US_en_US), [Playwright for Codespaces](https://playwright.dev/python/docs/docker), [desktop-lite](https://github.com/devcontainers/features/tree/main/src/desktop-lite).
