# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target: I chose 4/5 because the search uses keyword matching, so some user queries may not match a listing even when a similar item exists, but the system should still complete the full process most of the time.**

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target: If a query matches no listing, the agent should stop before calling `suggest_outfit` because the system could throw an error if  `suggest_outfit` is called with no data. I chose 5/5 because the system throwing an error means the system will not work correctly  and I need to be sure it isn't happening.**



---

## 3. Something about state

Given a query that returns a listing, the id of session["selected_item"] matches the id of what is passed to `suggest_outfit` 5/5 times.



**Why this target: I chose this target because for the system to work correctly the id of session["selected_item"] needs to match what is sent to `suggest_outfit`. I chose 5/5 because the state passing variables should be consistent rather than failing occasionally.**



---

## 4. Something about the fit card

A fit card should include the name of the item, its price, and its platform, at least once in 4/5 tries.


**Why this target: I chose this target because the wording of the generated fit card can vary, but it should still contain the important information I chose above about an item. I chose 4/5 because the system should be overall consistent, but generation can miss a detail once and the system can still work fine otherwise.**



---

## 5. Your choice

In 4/5 cases if a query contains a maximum price, every listing returned by `search_listings` is at or below the user's price ceiling.


**Why this target: If a user gives a price ceiling, the search should be considering that consistently. I chose 4/5, because while it should be consistent, an occasional item above the user's maximum price being returned would not prevent the rest of the system from functioning**



---

## UNIT 9 Criteria

## 6. Speed of a normal request

A normal not rate limited completed CLI run measured with `run_end.ms` should take no more than 6000ms to answer in 8/10 runs.

**Why this target: 6000ms is 5 seconds, through all the calls the system has to do, I think 6000ms is a good limit as the median run time was 4.9 seconds or 4900 ms, its a reasonable goal for 8/10 runs.**

## 7. Speed of a cold start request from render

A request from the cold start, or a run after 15 minutes of inactiveness, of a service should take no longer than 66000ms (1 minute and 6 seconds) to give an answer, measured manually by me through my phone's stop watch, starting when I send the ask message, and ending when I see the response. In 2/2 Runs.

**Why this target: Render claims that their free tier wake-up time is about one minute, plus 6000ms from the request means that it a cold start request should take around 66000ms. 2/2 because I have to wait 16 minutes between runs and don't want to wait two and a half hours.**

## 8. Total model tokens used per run with cache off

A full complete service run, that generates a fit card, should stay at or under 1200 total tokens in 8/10 runs.

**Why this target: 1200 total tokes seems like a good limit for input+output tokens as my cost per run was averaged to 1087 tokens. 8/10 runs means a rate of 80%, which means the system isn't wasting too much tokens.**

## 9. When a run fails the system will give the user a message and not crash

When a run fails, the system will give the user a message and not crash in 10/10 runs.

**Why this target: A failed run shouldn't crash the system, and tell the user it happened, it should do this with every failed run so a user gets feedback.**

## 10. Every run appears in the log

For every run its run_start, model and mcp calls, and run_end for completed or stopped runs, will be logged success or fail in 10/10 runs.

**Why this target: The point of the log is to record everything, so every run should be logged.**