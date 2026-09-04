# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a step-by-step tutorial project: a Flask expense tracker ("Spendly") being built incrementally by a student following a guided course. Many routes and modules are intentionally left as placeholders (plain strings like `"Logout — coming in Step 3"`) for the student to implement in later steps — do not "complete" these unless explicitly asked to work on that step, since the whole point is for the student to write that code themselves as part of the tutorial.

## Environment

- Windows machine. The venv lives at `venv/` with a **Windows layout** (`venv/Scripts/`, not `venv/bin/`).
- Each Bash tool call starts a fresh shell, so an activated venv does not persist across separate tool calls. Call the venv's interpreter directly instead of relying on activation:
  - `venv/Scripts/python.exe app.py`
  - `venv/Scripts/pip.exe install -r requirements.txt`
- There is no `python3` executable in this venv (only `python.exe` / `pythonw.exe`) — always use `python`, never `python3`.

## Commands

- Install dependencies: `venv/Scripts/pip.exe install -r requirements.txt`
- Run the dev server: `venv/Scripts/python.exe app.py` — serves on `http://127.0.0.1:5001` (not the Flask default 5000). Runs with `debug=True`, so it never exits on its own and auto-reloads on file changes; treat a "timeout" from a long-running tool call as expected, not a failure.
- Tests: `pytest` and `pytest-flask` are in `requirements.txt`, but no test files exist yet in the repo.

## Architecture

```
expense-tracker/
├── app.py                  # Flask app + all routes
├── requirements.txt
├── database/
│   ├── __init__.py         # empty, marks package
│   └── db.py                # empty stubs: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html            # shared layout (navbar, footer, blocks)
│   ├── landing.html
│   ├── login.html
│   └── register.html
└── static/
    ├── css/style.css
    └── js/main.js
```

- `app.py` — single-file Flask app; all routes are defined directly on the module-level `app` object (no blueprints).
- `database/db.py` — currently empty stubs; intended to eventually hold `get_db()` (SQLite connection, row_factory + foreign keys on), `init_db()` (`CREATE TABLE IF NOT EXISTS` schema), and `seed_db()` (sample data). No database code exists yet — routes don't touch persistence.
- `templates/` — Jinja2 templates. `base.html` is the shared layout (navbar, footer, CSS/JS includes) and defines `{% block title %}`, `{% block head %}`, `{% block content %}`, `{% block scripts %}` for pages to extend.
- `static/css/style.css` and `static/js/main.js` — global styles/scripts, linked from `base.html` via `url_for('static', ...)`.
- Route naming doubles as the Jinja `url_for()` target (e.g. `url_for('landing')`, `url_for('login')`) — when renaming a route function, update the corresponding `url_for()` calls in templates too.
