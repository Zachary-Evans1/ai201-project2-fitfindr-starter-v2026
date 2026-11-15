# Running FitFindr

Everything about how the starter works and how to use it.

---

## Start here: run FitFindr

FitFindr searches a set of thrift-store listings from a description, a size and
a maximum price. For the best match it suggests outfits from a wardrobe and
writes a short fit-card caption. The language model is Google's Gemini, so you
need a free API key.

**You need**

- Python 3.11, 3.12 or 3.13. **Not 3.14.**
- Git
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com).
  Sign in, create a project, and create a key inside it.
- An internet connection

### 1. Get the code

```bash
git clone https://github.com/Zachary-Evans1/ai201-project2-fitfindr-starter-v2026
cd ai201-project2-fitfindr-starter-v2026
```

### 2. Create a virtual environment and install the packages

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell refuses to run the activate script, run this once and try again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `(.venv)` prefix in your prompt means it's active. Activate it again in
every new terminal.

### 3. Add your API key

**Windows:** `copy .env.example .env`
**macOS / Linux:** `cp .env.example .env`

Open `.env` in a text editor and replace `your_key_here` with your key. Keep
the `GEMINI_API_KEY=` part. Don't add quotes or spaces. Check that the file is
named `.env` and not `.env.txt`. The file is gitignored, so it won't be
committed.

### 4. Check that it works

```bash
python test.py
```

You should see `10 passed, 0 failed`. If the model check fails, the key is
wrong or missing. Fix it in `.env` and run `test.py` again.

### 5. Run it

```bash
python app.py ask 'vintage graphic tee under $30'
python app.py ask 'designer ballgown size XXS under $5'
```

Use **single quotes** around the query. In PowerShell, double quotes turn
`$30` into an empty variable, and the price limit is silently dropped.

- The first query prints a **Found:** line with a listing, then **Outfit:** and
  **Fit card:**.
- The second query prints **stopped:** and says no listings matched. It tells
  you what to change. It has no fit card, and that's correct.

`python agent.py` runs both queries in one command.

### 6. Run the web server (optional)

```bash
python serve.py
```

It prints `FitFindr is listening on http://localhost:5000`. Leave it running,
and in a second terminal:

**Windows (PowerShell)**

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
Invoke-RestMethod -Uri "http://localhost:5000/ask" -Method Post -ContentType "application/json" -Body '{"query": "vintage graphic tee under $30"}'
```

**macOS / Linux**

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/ask -H 'Content-Type: application/json' -d '{"query": "vintage graphic tee under $30"}'
```

`/health` returns `{"status":"ok"}`. `/ask` returns the full session as JSON.
Stop the server with Ctrl+C.

### 7. The hosted version

The same server is deployed at
`https://ai201-project2-fitfindr-starter-v2026-hjlm.onrender.com`. Use the same
`/health` and `/ask` requests with that address in place of `localhost:5000`.
The free host goes to sleep when idle. The first request after a quiet period
can take about a minute.

### Each run is logged

Every run appends records to `logs/run.jsonl`. See **The run log** below for what
each record means.

### If something goes wrong

| What you see | What to do |
|---|---|
| `No GEMINI_API_KEY found` | `.env` is missing or misnamed. Check step 3 |
| `The model rejected your API key` | The key is wrong or incomplete. Create a new one at aistudio.google.com |
| `Couldn't reach the model` | Check your internet connection and try again |
| `[rate limit] ... Waiting 34s` | Normal. The app is pacing its requests. Wait |
| The price limit is ignored | You used double quotes in PowerShell. Use single quotes |

More problems and their causes are listed under **When something goes wrong**
below.

---

## Before your first class

Setup happens **before class**. The [environment setup page](../pages/ide_setup)
has the per-operating-system commands and the exact versions.

**Same API key you set up in unit 1.** Nothing new to sign up for. There is one
new package — the MCP SDK, for unit 4 — and it installs with everything else.

From inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then paste your key into .env
python test.py
```

**You're ready when `python test.py` passes.**

If it doesn't and you've made one honest attempt at the error, post the
**whole** output in the help channel.

> Activate the virtual environment every time you open a new terminal. You
> should see `(.venv)` at the start of your prompt.

---

## Your first five minutes

Start with the data. Your tools will only be as good as your understanding of
what they're reading, and ten minutes here saves an hour of confused debugging.

```bash
python app.py fields                    # what a listing and a wardrobe item hold
python app.py listings --full -n 6      # read six listings all the way through
python app.py examples                  # queries worth trying
python app.py ask 'vintage graphic tee under $30'
```

> **Quote your queries with single quotes**, on every operating system. In
> PowerShell, `"vintage graphic tee under $30"` in double quotes silently
> becomes `vintage graphic tee under ` — PowerShell reads `$30` as a variable
> and substitutes nothing. You get results with no price ceiling and no error
> saying so. Single quotes are literal in PowerShell, bash and zsh alike.

That last one runs the loop. All three tools are stubs, so it will tell you the
loop isn't built yet. **That's the correct starting position** — it runs, and it
does nothing.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment. Run it whenever something feels off |
| `python app.py fields` | The fields a listing and a wardrobe item have — **Milestone 1** |
| `python app.py listings` | Browse the data. `--full` for whole records, `-n` for how many |
| `python app.py examples` | Queries worth trying, including one that matches nothing |
| `python app.py ask '...'` | Run the agent on one query — **single quotes** |
| `python app.py ask` | Keep asking until you press Enter on an empty line |
| `python agent.py` | Runs both example paths — one that matches, one that can't |
| `python mcp_server.py` | Starts your MCP server — **unit 4** |
| `python mcp_client.py` | Asks the server what it offers — **unit 4** |
| `python run_eval.py --label before` | Runs every scenario five times and writes the run log — **unit 4** |
| `python serve.py` | Serves the agent over HTTP instead of exiting — **unit 9** |

Useful flags on `ask`:

| Flag | What it does |
|---|---|
| `--trace` | Print the loop step by step, once you've added the trace calls |
| `--empty-wardrobe` | Run as a user with nothing saved — one of unit 4's failure modes |

---

## Which command goes with which milestone

### Unit 3 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Read the data, run the starter | `app.py fields`, `app.py listings --full`, `app.py ask` |
| 2 | Spec your three tools | README, **Tool Inventory** |
| 3 | Write your acceptance criteria | `criteria.md` |
| 4 | Build the three tools | `tools.py`, tested one at a time from a terminal |
| 5 | Wire the loop and the state | `agent.py::run_agent` |
| 6 | Write it up | README |

### Unit 4 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Move one tool onto MCP | `mcp_server.py`, then `mcp_client.call_tool` in `run_agent` |
| 2 | Break it on purpose, then trace it | `trace.py`, `app.py ask --trace` |
| 3 | Run your test | `scenarios.py`, then `run_eval.py --label before` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | `run_eval.py --label after` |
| 6 | Say what's still broken | README |

---

## Running it somewhere else — **unit 9**

Everything above exits when the command finishes. A host has nothing to keep
running, so before you can deploy this you need something that stays up.
`serve.py` is that: the same `run_agent()`, behind two HTTP routes.

On your machine:

```bash
python serve.py
curl -X POST http://localhost:5000/ask \
  -H 'Content-Type: application/json' \
  -d '{"query": "vintage graphic tee under $30"}'
```

On a host, the start command is:

```bash
gunicorn serve:app
```

| Thing | What it means |
|---|---|
| `PORT` | The host tells your app which port to listen on by setting this. Both `serve.py` and `gunicorn` read it, and `serve.py` falls back to `5000` on your machine. Don't hard-code a port |
| `POST /ask` | `{"query": "...", "wardrobe": {...}}` — wardrobe optional. Returns the session dict, `error` and all |
| `GET /health` | Says `ok` if the app is awake |
| It answers one request at a time | On purpose. A second request waits for the first to finish, and prints `[serve] another request is still running` while it waits. An MCP tool call starts a whole second Python process, and the free tier's 512 MB has no room for two of those at once — and `generate.py`'s rate-limit counting assumes one caller. The reasoning is written out in `serve.py` |
| `gunicorn serve:app`, exactly | Not `-k gevent`, not `-k eventlet`, not wrapped for uvicorn. `mcp_client.call_tool` uses `asyncio.run()`, which won't start inside a running event loop, so an async worker breaks **every** MCP call — and only once you've deployed it |
| The first request is slow | The free tier puts your app to sleep after about fifteen minutes of nothing. The next request wakes it up and waits for it — around a minute. Not a bug, and worth knowing before you demo it |

`serve.py` writes a `request` record for every HTTP call, and every agent run
writes its own records. See **The run log** below.

### Deploying to Render (Path A)

Render builds from the code on GitHub, not from your machine. **Push your
commits first**, or the deploy will run old code.

| Setting | Value |
|---|---|
| Runtime | Python |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn serve:app` |
| Instance type | Free |
| Environment variable `GEMINI_API_KEY` | Your key. Set it in the Render dashboard only. Never put it in a file in the repo |
| Environment variable `PYTHON_VERSION` | `3.13.13`. The requirements don't support 3.14, and Render may default to a newer version |

Check that it's up:

```bash
curl https://YOUR-URL.onrender.com/health
```

Free instances go to sleep after about fifteen minutes, and their disk is wiped
when they do. That includes `logs/`. Copy the log lines you need into
`results/` and commit them the same session.

**On Windows, `gunicorn` won't run** — it imports `fcntl`, which only exists on
Linux and macOS. Use `python serve.py` on your machine. Render runs Linux, so
the start command above works there.

---

## The run log

Every run writes one JSON object per line to `logs/run.jsonl`. The `logs/`
folder is gitignored. When you want to keep lines, copy them into `results/`
and commit that copy.

| Event | Written by | Main fields |
|---|---|---|
| `run_start` | `agent.py` | `query` |
| `model_call` | `generate.py` | `ok`, `cache_hit`, `attempt`, `ms`, `prompt_tokens`, `output_tokens`, `error` |
| `model_retry` | `generate.py` | `attempt`, `backoff_s`, `ms` |
| `mcp_call` | `mcp_client.py` | `tool`, `ok`, `ms`, `returned_count`, `error` |
| `run_end` | `agent.py` | `outcome` (`completed` or `stopped_no_results`), `ms`, `has_fit_card` |
| `request` | `serve.py` | `method`, `path`, `status`, `ms`, `lock_wait_ms`, `error` |

Every line also has `ts` (a timestamp) and `run_id`. Lines from the same run
share a `run_id`, so you can pull one run out of the file.

Read the log back in PowerShell:

```powershell
Get-Content logs\run.jsonl
```

**For real timings, turn the cache off.** Answers are cached by default, so a
cached model call shows `ms: 0` and no tokens. Turn the cache off for the
current shell only:

```powershell
$env:AI201_CACHE = "0"     # macOS / Linux: export AI201_CACHE=0
```

Turn it back on with `Remove-Item Env:AI201_CACHE` (macOS / Linux: `unset AI201_CACHE`).

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting worth changing — **TEMPERATURE and the cache are at the top** |
| `tools.py` | Your three tools. **Stubs — you build these** |
| `agent.py` | The planning loop and the session. **Stub — you build this** |
| `generate.py` | The only thing that calls out to a service. Handles pacing and quota |
| `trace.py` | The trace helper, and the loop's stop condition |
| `app.py` | The command line |
| `serve.py` | The same agent over HTTP, for deploying — **unit 9** |
| `mcp_server.py` | Your MCP server — **unit 4, you register the tool** |
| `mcp_client.py` | Calling an MCP tool from your agent. Given to you |
| `scenarios.py` | What your test runs. **You fill this in** |
| `run_eval.py` | Runs the scenarios repeatedly and writes the run log |
| `criteria.md` | Your five acceptance criteria. **You fill this in** |
| `data/` | 40 listings and the wardrobe schema |
| `utils/data_loader.py` | Loading the data. Use this rather than reading the files yourself |
| `results/` | Run logs. **Commit these** — they're your evidence |
| `runlog.py` | Writes the run log. Every other file that logs calls into it |
| `logs/` | The live run log, `logs/run.jsonl`. Gitignored. Copy what you keep into `results/` |

---

## The two settings people go looking for

Both are at the top of `config.py`, and the brief points at them by name.

If your fit cards come out **word-for-word identical** every time, it is one of:

- **`CACHE_ENABLED`** — while you build, identical prompts reuse the answer
  already received. That's deliberate; it makes debugging free. `run_eval.py`
  turns it off automatically.
- **`TEMPERATURE`** — at `0.0` the model gives you the same words every time.
  It ships at `0.9`.

---

## About rate limits

**This is the heaviest pair in the course for call volume.** Two of your three
tools call the model, so one agent run is several requests, and a few runs back
to back while debugging can cross the per-minute limit.

`generate.py` handles it:

- **It paces itself** and says when it's waiting. **A pause is the starter
  doing its job, not a bug.**
- **It reuses answers** to prompts already sent, while you build.
- **It stops** if a session makes an unreasonable number of calls, rather than
  draining your day's allowance. For an agent, that usually means a loop isn't
  ending — look for that before raising the number.
- **It counts your calls** and prints the total when you exit.

`config.MAX_ITERATIONS` is the loop's own stop condition. Your loop this unit
is short enough that you may never hit it. Keep it — a missing stop condition
is the most common architectural failure in production agents.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `The planning loop isn't built yet` | Correct, at the start. That's the TODO in `agent.py` |
| `No GEMINI_API_KEY found` | No `.env`, or the key wasn't pasted in. On Windows check it didn't save as `.env.txt` |
| A message saying the model couldn't be reached | Usually a bad key. This is also **exactly what unit 4 Milestone 2 asks you to trigger on purpose** |
| `[rate limit] ... Waiting 34s` | Working as intended. Leave it |
| `[serve] another request is still running` | Also working as intended. `serve.py` answers one request at a time; yours is queued behind one that's mid-run |
| `QuotaGuard: This session has made 300 requests` | A loop isn't ending. Find it before raising the budget |
| `The loop ran 11 times, past MAX_ITERATIONS` | Same thing, caught earlier |
| `The server doesn't offer a tool called '...'` | Nothing registered in `mcp_server.py` yet, or the name doesn't match |
| MCP returns a string where you expected a list | You're not going through `mcp_client.call_tool`, which unwraps it |
| Fit cards identical every run | `CACHE_ENABLED` or `TEMPERATURE`. See above |
| `--trace` prints nothing | You haven't added `trace.step()` calls yet — unit 4, Milestone 2 |
| `IncompleteFieldDefinitionWarning: Field 'lifespan'` | Harmless noise from the MCP library's dependencies. Not your code, not an error. Ignore it |
| A price ceiling you typed is being ignored | You used double quotes in PowerShell. `$30` vanished. Use single quotes |
| `ModuleNotFoundError: No module named 'fcntl'` when you run `gunicorn` | You're on Windows. `gunicorn` only runs on Linux and macOS. Use `python serve.py` locally |
| The hosted `/ask` returns `ModelUnavailable: ... rejected your API key` | The `GEMINI_API_KEY` in the host's environment is wrong or incomplete. Re-paste it in the dashboard and let the service redeploy. `/health` still works while this happens |
| `UnicodeEncodeError: 'charmap' codec can't encode` | Shouldn't happen — `config.py` sets the console to UTF-8. If you see it, you're running a file that doesn't import `config` |

Still stuck after one honest attempt? Post in the help channel with the full
error, what you ran, and what you expected.

---

## A note on committing

At least four new commits in unit 3, at least four more in unit 4. Your commit
history is what shows your criteria existed before your results did.

**Do not delete and recreate this repository.** You submit the same URL both
units.

`results/` is deliberately **not** in `.gitignore`.
