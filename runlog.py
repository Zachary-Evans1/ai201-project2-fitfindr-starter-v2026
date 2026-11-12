"""
A structured run log: one JSON object per line, one line per event.

Every run appends to logs/run.jsonl. Each line has a timestamp, an event name,
a run_id that ties together the lines from one agent run, and the numbers that
matter: how long things took, whether they worked, and what came back.

    {"ts": "...", "run_id": "a1b2c3d4", "event": "model_call", "ok": true, "ms": 812}

Events:
    request      one HTTP call to /ask (serve.py): status, total ms, lock wait ms
    run_start    the agent started on a query
    run_end      the agent finished: outcome, total ms, how many results
    model_call   one call to the model: ms, ok, cache hit, tokens
    model_retry  the model pushed back (rate limit): how long we waited
    mcp_call     one call to an MCP tool: tool name, ms, ok

Logging must never break a run. A failed write prints one warning to stderr
and the run carries on.
"""

import json
import sys
import time
import uuid
from datetime import datetime, timezone

import config

LOG_PATH = config.ROOT / "logs" / "run.jsonl"

_run_id: str | None = None
_run_t0: float | None = None
_warned = False


def start_run() -> str:
    """Begin a new run. Every event after this carries the same run_id."""
    global _run_id, _run_t0
    _run_id = uuid.uuid4().hex[:8]
    _run_t0 = time.monotonic()
    return _run_id


def clear_run() -> None:
    """Forget the current run, so a request that never reaches the agent isn't tagged with an old run."""
    global _run_id, _run_t0
    _run_id = None
    _run_t0 = None


def run_id() -> str | None:
    return _run_id


def run_ms() -> int | None:
    """Milliseconds since start_run(), or None if no run is active."""
    return ms_since(_run_t0) if _run_t0 is not None else None


def ms_since(t0: float) -> int:
    return round((time.monotonic() - t0) * 1000)


def event(kind: str, **fields) -> None:
    """Write one event line. Fields whose value is None are left out."""
    global _warned
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": _run_id,
        "event": kind,
    }
    record.update({k: v for k, v in fields.items() if v is not None})
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except OSError as exc:
        if not _warned:
            _warned = True
            print(f"  [runlog] could not write {LOG_PATH}: {exc}", file=sys.stderr, flush=True)
