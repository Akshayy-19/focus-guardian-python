# Focus Guardian — Study Timer

Focus Guardian is a beginner-friendly desktop study timer built with Python and Tkinter. It provides a 25-minute focus session, subject selection, pause/resume/reset controls, and a completed-session counter.

## Features
- 25-minute countdown timer
- Select a study subject: Python, Mathematics, Programming, or Other
- Start, pause, resume, and reset controls
- Minimize and maximize/restore window controls
- Completed-session counter
- Completion notification
- Dark-themed Tkinter interface

## Requirements
- Python 3 with Tkinter
- Windows, macOS, or Linux desktop environment

Tkinter is included with many standard Python installations. On some Linux distributions, it may need to be installed separately.

## Run the project
1. Install Python 3 if it is not already installed.
2. Open a terminal in this folder.
3. Run:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

## Project structure
- `main.py` — application source code
- `README.md` — project description and run instructions
- `.gitignore` — ignores Python cache and editor files

## Current limitations
- Session length is fixed at 25 minutes.
- Completed session count resets when the application closes.
- The app does not store historical study sessions or reports.
