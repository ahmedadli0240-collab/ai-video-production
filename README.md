# AI Finance Video Studio — Real QuickBooks + ChatGPT

Produce a course video using the **actual websites**, not recreated interfaces. Designed for GitHub Codespaces with a private noVNC desktop, a real Chromium browser, FFmpeg screen capture, optional ElevenLabs American-English male narration, and automatic MP4 editing.

**Status:** Source code and lesson workflow are ready. The real QuickBooks and ChatGPT recording has not been captured. You must start the Codespace and sign into ChatGPT interactively; the GitHub connector cannot launch Codespaces or operate the desktop.

## First-time setup

1. **Set this repository to PRIVATE** (Settings → General → Danger Zone → Change repository visibility). Never commit credentials, session cookies, financial exports, or recordings.
2. In GitHub, select **Code → Codespaces → Create codespace on main**. Allow the development container setup to finish.
3. Open the **Ports** tab → port **6080** → set visibility to **Private** → open in browser. The desktop password is specified in `.devcontainer/devcontainer.json`; access is additionally controlled by private Codespaces port permissions.
4. From a Codespaces terminal run: `python scripts/browser_session.py --autonav`. A real Chromium desktop opens Intuit's free QuickBooks Online demo and chatgpt.com. Sign into ChatGPT **before** you record.
5. From a second terminal start the real screen capture: `python scripts/record.py start`. Mark scenes in sequence: `intro`, `quickbooks`, `export`, `chatgpt`, `analysis`, `followup`, `outro` using `python scripts/record.py mark SCENE`. Finally run `python scripts/record.py stop`.
6. Use QuickBooks' actual Profit and Loss report and export it to Excel. Upload the exported Excel file to ChatGPT manually and use `lesson/analysis_prompt.txt`. Read ChatGPT's real response and ask the real follow-up from `lesson/followup_prompt.txt`. Cross-check amounts against QuickBooks.
7. Configure an **ELEVENLABS_API_KEY Codespaces secret**, **not in repository files**. Run `python scripts/narrate.py` to generate male narration (Adam voice; optional ELEVENLABS_VOICE_ID override). Then `python scripts/assemble.py` to render the final 1080p MP4 and an approximate subtitle SRT.
8. Finished file: `outputs/QuickBooks_ChatGPT_REAL_Platform_Lesson.mp4`. Download it from the cloud environment; output files are gitignored.

## Recording safety

- This project does not fake QuickBooks or ChatGPT interfaces or claim financial results that were not verified.
- Keep port 6080 private; do not record login screens; never expose ElevenLabs or other API keys.
- ChatGPT login, some QuickBooks navigation and prompts are manual checkpoints. The automation intentionally does not bypass CAPTCHA or scrape ChatGPT responses.
- The demo company can reset. If exporting a genuine report is blocked, stop rather than substitute fabricated data.

## What's in this repository

- `.devcontainer/`: Codespaces desktop and Playwright runtime
- `scripts/browser_session.py`: opens actual websites in Chromium, assists with demo report navigation
- `scripts/record.py`: records actual desktop and marks video chapters
- `scripts/narrate.py`: ElevenLabs male AI voice from written lesson
- `scripts/assemble.py`: trims and aligns real video with voice, outputs MP4 and SRT
- `lesson/`: prompts, story outline, narration script and review checklist

Official sources: [Intuit test drive](https://quickbooks.intuit.com/learn-support/en-us/help-article/small-business-processes/test-drive-quickbooks-online/L9C12ODlA_US_en_US), [Playwright for Codespaces](https://playwright.dev/python/docs/docker), [desktop-lite](https://github.com/devcontainers/features/tree/main/src/desktop-lite).
