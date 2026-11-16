#!/usr/bin/env python3
"""
The runs that produce the numbers for criteria 6, 8, 9 and 10. ← UNIT 9, MILESTONE 5

    python criteria_test.py --trial 1
    python criteria_test.py --trial 2
    python criteria_test.py --trial 3

Milestone 5 asks for three separate trials, so run this three times, each time
with a new trial number. Each trial writes its own file to results/.

Each trial does two things, in one process, with the cache off:

  1. Ten successful runs of the matching query.
     Feeds criteria 6 (speed), 8 (tokens) and 10 (logging).
  2. Ten failing runs. The model name is set to one that doesn't exist, so the
     first model call fails the way a bad key or a bad model would.
     Feeds criteria 9 (failure gives a message) and 10 (logging).

Criterion 7 (cold start) is NOT run here. It needs the hosted service to sleep
for about fifteen minutes and a stopwatch on your phone. The script prints the
steps at the end of each trial, and you record that time by hand.

What this script does NOT do: decide the verdict. It prints the counts and the
pass rule it used for each criterion. Check those rules against the sentences
in criteria.md before you copy any number into the table.
"""

import argparse
import datetime as dt
import json
import sys
import traceback

import config

MATCHING_QUERY = "vintage graphic tee under $30"
MATCHING_RUNS = 10
FAILING_RUNS = 10
FAKE_MODEL = "criteria-9-model-that-does-not-exist"

# Limits and targets, copied from criteria.md. Edit here if the criteria change.
# Each target is (passes needed, out of how many).
SPEED_LIMIT_MS = 6000       # criterion 6: run_end.ms
SPEED_TARGET = (8, 10)
TOKEN_LIMIT = 1200          # criterion 8: total tokens per run
TOKEN_TARGET = (8, 10)
FAILURE_TARGET = (10, 10)   # criterion 9
LOGGING_TARGET = (10, 10)   # criterion 10
COLD_START_MS = 66000       # criterion 7: manual, measured by stopwatch
COLD_START_RUNS = 1         # criterion 7: 1 of 1 run, per trial


# ─── Running ────────────────────────────────────────────────────────────────


def run_one(query):
    """One full agent run. Returns the run_id and whatever came back or was raised."""
    from agent import run_agent
    from utils.data_loader import get_example_wardrobe
    import runlog

    result = {"run_id": None, "session": None, "error": None, "traceback": None}
    try:
        result["session"] = run_agent(query, get_example_wardrobe())
    except Exception as exc:  # noqa: BLE001 — what the exception is, is the result
        result["error"] = exc
        result["traceback"] = traceback.format_exc()
    result["run_id"] = runlog.run_id()
    return result


def read_log(run_ids):
    """Every log line that belongs to one of the given runs, in file order."""
    path = config.ROOT / "logs" / "run.jsonl"
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(raw)
        if record.get("run_id") in run_ids:
            lines.append(record)
    return lines


def group_by_run(records):
    grouped = {}
    for record in records:
        grouped.setdefault(record["run_id"], []).append(record)
    return grouped


# ─── Scoring: one function per criterion ────────────────────────────────────


def score_speed(grouped):
    """Criterion 6. Completed, non-rate-limited runs, timed by run_end.ms."""
    pool, passed, detail = 0, 0, []
    for run_id, events in grouped.items():
        end = next((e for e in events if e["event"] == "run_end"), None)
        if not end or end.get("outcome") != "completed":
            continue
        # Rate-limited means the model pushed back (model_retry) or the pacer
        # made the run wait for its per-minute window (model_wait). The pacer
        # was not logged before this change, so trials run before it show
        # those runs as ordinary slow runs.
        if any(e["event"] in ("model_retry", "model_wait") for e in events):
            detail.append(f"{run_id}: excluded, rate-limited or paced")
            continue
        pool += 1
        ok = end["ms"] <= SPEED_LIMIT_MS
        passed += ok
        detail.append(f"{run_id}: {end['ms']} ms {'PASS' if ok else 'FAIL'}")
    return {"pass": passed, "of": pool, "detail": detail,
            "rule": f"completed, not rate-limited or paced, run_end.ms <= {SPEED_LIMIT_MS}"}


def score_tokens(grouped):
    """Criterion 8. Completed runs that produced a fit card, summed over model calls."""
    pool, passed, detail = 0, 0, []
    for run_id, events in grouped.items():
        end = next((e for e in events if e["event"] == "run_end"), None)
        if not end or end.get("outcome") != "completed" or not end.get("has_fit_card"):
            continue
        tokens = sum(
            (e.get("prompt_tokens") or 0) + (e.get("output_tokens") or 0)
            for e in events
            if e["event"] == "model_call" and e.get("ok")
        )
        pool += 1
        ok = tokens <= TOKEN_LIMIT
        passed += ok
        detail.append(f"{run_id}: {tokens} tokens {'PASS' if ok else 'FAIL'}")
    return {"pass": passed, "of": pool, "detail": detail,
            "rule": f"completed with fit card, total tokens <= {TOKEN_LIMIT}"}


def score_failure_message(failing_results):
    """Criterion 9. A failing run raises ModelUnavailable with a readable message."""
    from generate import ModelUnavailable

    passed, detail = 0, []
    for result in failing_results:
        exc = result["error"]
        ok = isinstance(exc, ModelUnavailable) and bool(str(exc).strip())
        passed += ok
        kind = type(exc).__name__ if exc else "no exception"
        detail.append(f"{result['run_id']}: {kind} {'PASS' if ok else 'FAIL'}")
    return {"pass": passed, "of": len(failing_results), "detail": detail,
            "rule": "raises ModelUnavailable with a non-empty message (not any other exception)"}


def score_logging(matching_results, failing_results, grouped):
    """Criterion 10. Counted two ways, because the criterion is ambiguous about failures."""
    sent = len(matching_results) + len(failing_results)
    started = sum(
        1 for r in matching_results + failing_results
        if r["run_id"] and any(e["event"] == "run_start" for e in grouped.get(r["run_id"], []))
    )

    matching_ok, failing_ok, detail = 0, 0, []
    for r in matching_results:
        events = grouped.get(r["run_id"], [])
        ok = (any(e["event"] == "run_start" for e in events)
              and any(e["event"] == "run_end" for e in events))
        matching_ok += ok
        detail.append(f"{r['run_id']} (matching): {'PASS' if ok else 'FAIL'}")
    for r in failing_results:
        events = grouped.get(r["run_id"], [])
        ok = (any(e["event"] == "run_start" for e in events)
              and any(e["event"] == "model_call" and not e.get("ok") for e in events))
        failing_ok += ok
        detail.append(f"{r['run_id']} (failing): {'PASS' if ok else 'FAIL'}")

    return {
        "sent": sent,
        "run_start_logged": started,
        "matching_pass": matching_ok, "matching_of": len(matching_results),
        "failing_pass": failing_ok, "failing_of": len(failing_results),
        "detail": detail,
        "rule": ("matching: run_start + run_end. failing: run_start + a failed model_call. "
                 "Both groups are reported; criterion 10 doesn't say which one it counts."),
    }


# ─── Main ───────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Run the criteria 6, 8, 9 and 10 trial.")
    parser.add_argument("--trial", type=int, required=True, help="which trial this is (1, 2 or 3)")
    args = parser.parse_args()

    config.CACHE_ENABLED = False
    print(f"Trial {args.trial}. Cache is OFF.\n")

    print(f"Running {MATCHING_RUNS} matching runs...")
    matching = []
    for i in range(1, MATCHING_RUNS + 1):
        result = run_one(MATCHING_QUERY)
        status = "error" if result["error"] else "ok"
        print(f"  matching {i}: {status}")
        matching.append(result)

    print(f"\nRunning {FAILING_RUNS} failing runs (model name set to {FAKE_MODEL!r})...")
    real_model = config.MODEL
    config.MODEL = FAKE_MODEL
    try:
        failing = []
        for i in range(1, FAILING_RUNS + 1):
            result = run_one(MATCHING_QUERY)
            kind = type(result["error"]).__name__ if result["error"] else "no exception"
            print(f"  failing {i}: {kind}")
            failing.append(result)
    finally:
        config.MODEL = real_model

    run_ids = {r["run_id"] for r in matching + failing if r["run_id"]}
    records = read_log(run_ids)
    grouped = group_by_run(records)

    scores = {
        6: score_speed(grouped),
        8: score_tokens(grouped),
        9: score_failure_message(failing),
        10: score_logging(matching, failing, grouped),
    }

    print("\n" + "=" * 60)
    print(f"Trial {args.trial} results")
    print("=" * 60)
    targets = {6: SPEED_TARGET, 8: TOKEN_TARGET, 9: FAILURE_TARGET}
    for number in (6, 8, 9):
        s = scores[number]
        need, out_of = targets[number]
        print(f"\nCriterion {number}: {s['pass']} of {s['of']}   (target: {need} of {out_of})")
        print(f"  rule: {s['rule']}")
    s10 = scores[10]
    need, out_of = LOGGING_TARGET
    print(f"\nCriterion 10: run_start logged for {s10['run_start_logged']} of {s10['sent']} runs sent")
    print(f"  matching runs passing: {s10['matching_pass']} of {s10['matching_of']}")
    print(f"  failing runs passing:  {s10['failing_pass']} of {s10['failing_of']}")
    print(f"  target: {need} of {out_of}")
    print(f"  rule: {s10['rule']}")

    print(f"\nCriterion 7 is manual: {COLD_START_RUNS} cold starts per trial, "
          f"each under {COLD_START_MS} ms. Do it now, or as a separate step:")
    print("  1. Leave the hosted service idle for 15+ minutes.")
    print("  2. Start the stopwatch when you send the ask message.")
    print("  3. Stop it when the response appears. Write the time in the table by hand.")

    write_report(args.trial, matching, failing, scores, records)


def write_report(trial, matching, failing, scores, records):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"criteria_trial_{trial}_{stamp}.md"

    lines = [
        f"# Criteria trial {trial}",
        "",
        "- Produced by: `criteria_test.py::main`",
        "- Loop: `agent.py::run_agent` · tools: `tools.py`",
        f"- Matching runs: {MATCHING_RUNS} · failing runs: {FAILING_RUNS} · cache off",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Counts",
        "",
    ]
    targets = {6: SPEED_TARGET, 8: TOKEN_TARGET, 9: FAILURE_TARGET}
    for number in (6, 8, 9):
        s = scores[number]
        need, out_of = targets[number]
        lines += [f"- Criterion {number}: {s['pass']} of {s['of']} (target {need} of {out_of}; {s['rule']})"]
    s10 = scores[10]
    lines += [
        f"- Criterion 10: run_start logged for {s10['run_start_logged']} of {s10['sent']} runs sent",
        f"  - matching runs passing: {s10['matching_pass']} of {s10['matching_of']}",
        f"  - failing runs passing: {s10['failing_pass']} of {s10['failing_of']}",
        f"- Criterion 7: manual, not in this file",
        "",
        "## Per-run detail",
        "",
        "```",
    ]
    for number in (6, 8, 9, 10):
        lines.append(f"criterion {number}:")
        lines += [f"  {d}" for d in scores[number]["detail"]]
    lines += ["```", "", "## Raw log lines for this trial", "", "```"]
    lines += [json.dumps(r) for r in records]
    lines += ["```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit this file before you commit the next trial.")


if __name__ == "__main__":
    main()
