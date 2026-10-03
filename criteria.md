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

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
