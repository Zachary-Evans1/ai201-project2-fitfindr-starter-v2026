# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr is a thrift-shopping agent that searches clothing listings based on a user's description, size, and maximum price. When it finds a matching listing, it uses the user's wardrobe to suggest outfits that would fit with the listing and creates a short fit-card caption for the item and outfit. If the user's wardrobe is empty, it will just give general styling advice about the selected item. If no listings match the user's search, the agent stops and tells the user what they could change.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does: Searches the listings data for items matching the description, and optionally filters by size and/or price ceiling.**
- **Inputs: 'description' (str), 'size' (str or None); A requested size matches a complete size component. An "M" would match to "S/M" but an "L" would not match to "XL", 'max_price' (float or None).**
- **Returns: list[dict] a list of matching items from the listings data file. Listings contain an id, title, description, category, style_tags, size, condition, price, colors, brand, and platform.**
- **When it has nothing: Returns an empty list when no listings match**

### `suggest_outfit`

- **What it does: Uses a thrifted item and a users wardrobe to suggest one or two outfits.**
- **Inputs: 'new_item' (dict), 'wardrobe' (dict).**
- **Returns: A string with one or two outfit suggestions.**
- **When it has nothing: Returns a string with general styling advice for the new item if the wardrobe is empty.**

### `create_fit_card`

- **What it does: Writes a short caption someone would actually post about an outfit.**
- **Inputs: 'outfit' (str), 'new_item' (dict).**
- **Returns: A two to four sentence string as a caption that contains the item, its price, its platform, and its vibe.**
- **When it has nothing: If outfit is empty, returns a descriptive message as a string.**

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule: If `search_listings` returns an empty list, the agent stores a message in the session explaining what the user could change and stops the planning loop. Otherwise, the agent takes the first result, stores it as the selected item, and continues to `suggest_outfit`.**

**Where it lives: agent.py::run_agent** `agent.py::run_agent`

**How the query is parsed: The agent will parse the user's query into a description, size, and maximum price by asking the model.** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session: The user's query will be stored in 'session["query"]', then the parsed description, size, and maximum price are stored in 'session["parsed"]'. The results from 'search_listings' are stored in 'session["search_results"]'. The first result is stored in 'session["selected_item"]', and passed with the wardrobe, stored in 'session["wardrobe"]' to 'suggest_outfit'. The outfit suggestion will be stored in 'session["outfit_suggestion"]', and passed with the selected item to 'create_fit_card', whose result is stored in 'session["fit_card"]'.** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask "vintage graphic tee under $30"

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit combinations using the Y2K butterfly baby tee and pieces you already own:

### Outfit 1: Casual Y2K Streetwear
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Footwear:** Chunky white sneakers
* **Outerwear/Layering:** Black cropped zip hoodie (worn open or tied around the waist)
* **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances out the volume of the baggy dark-wash jeans, leaning straight into authentic early-2000s proportions. Adding the black cropped hoodie and chunky white sneakers keeps the vibe effortlessly casual and cohesive.

### Outfit 2: Retro Smart-Casual
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Wide-leg khaki trousers
* **Footwear:** Black combat boots
* **Accessories:** Brown leather belt 

**Why it works:** Pairing the ultra-feminine, colorful butterfly tee with structured khaki trousers creates a great high-low contrast. Tucking the tee in with a brown leather belt defines the waist, while the black combat boots add a bit of edge to ground the softer pastel tones of the top.

  Fit card: Channeling total 2000s pop princess energy with this pastel butterfly baby tee! It’s in amazing condition and just listed on my Depop for $18. Grab it before I change my mind and keep it for myself! 🦋✨

1 model calls this session, 2 served from cache, 97 prompt + 28 output tokens
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit combinations using the new vintage Levi's 501s and pieces straight from your wardrobe:

### Outfit 1: Casual & Cozy (Effortless Everyday)
* **Top:** White ribbed tank top
* **Outerwear:** Oversized grey crewneck sweatshirt
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag
* **Why it works:** The straight-leg fit of the 501s balances the oversized, slouchy proportions of the grey crewneck. Layering the sweatshirt over the crisp white tank adds texture and dimension, while the chunky sneakers and black crossbody keep the look sporty, grounded, and practical for daily errands.

### Outfit 2: Edgy Contrast (Cool-Girl Casual)
* **Top:** White ribbed tank top
* **Outerwear:** Black cropped zip hoodie (worn open or layered under) OR Vintage black denim jacket
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt
* **Why it works:** Adding the brown leather belt defines your waist against the medium-wash denim, bringing a touch of polish to the vintage 501s. Pairing them with black combat boots and the black cropped hoodie introduces a tougher, streetwear-inspired edge that contrasts nicely with the classic, all-American feel of the jeans.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats the perfect pair of worn-in denim. These vintage Levi's 501 jeans have the best faded knees and look so good with crisp white sneakers for that effortless everyday uniform. Grab them on Depop for just$38 before I change my mind!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for: I asked ChatGPT to help me check the `create_fit_card` tool after it returned the same caption multiple times.*
- *What came back: It helped me figure out caching was enabled in the config file and how to disable it for a test rather than change the code.*
- *What I changed: I used the `$env:AI201_CACHE="0"` powershell command ChatGPT recommended to disable caching for that powershell session so I could test `create_fit_card`.*

**Moment 2**

- *What I asked for: I asked Claude to implement my `search_listings` function and I told it to make sure it was careful with size matching so a requested `L` would not match `XL` but a requested `M` or `S` could match `S/M`.*
- *What came back: Claude helped me figure out that the size check should compare complete size components rather than using a substring match.*
- *What I changed: With Claude's help, I implemented `search_listings` with the `_size_matches` helper function that used size tokens to split on non-alphanumeric characters and compare those tokens to the requested size. I then tested both `M` and `L` searches to make sure the filtering worked as intended*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) | 
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. selected item state matches outfit input | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 4. fit card includes item details | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 5. price ceiling is respected | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5)  |

**Real output from one try for each criterion**, pasted as text, naming the file and function
that produced it:

# Criterion 1:

Source: `agent.py` — `run_agent()`
```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```

Here are 2 outfit combinations using the Y2K Baby Tee and pieces you already own:

### Outfit 1: Casual Y2K Streetwear
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Footwear:** Chunky white sneakers
* **Outerwear:** Black cropped zip hoodie (worn open or tied around the waist)
* **Accessories:** Black crossbody bag

**Why it works:** The fitted, cropped silhouette of the baby tee balances out the volume of the baggy, dark wash jeans for a classic early-2000s proportion play. Paired with chunky white sneakers and the black cropped hoodie, it leans effortlessly into the Y2K aesthetic of the shirt. 

### Outfit 2: Elevated Contrast
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Wide-leg khaki trousers
* **Accessories:** Brown leather belt + Black crossbody bag
* **Footwear:** Black combat boots

**Why it works:** This look plays with high-low styling by mixing the ultra-feminine, playful butterfly tee with more structured, utilitarian pieces. Tucking the baby tee into the wide-leg khaki trousers and cinching it with the brown leather belt defines the waist, while the black combat boots add a cool, grounding edge to the pastel pink and purple graphic.
```

Fit card:

```
Channeling major 2000s pop star energy with this butterfly print Y2K baby tee 🦋 Grab it on Depop in excellent condition for just $18! Pair it with baggy jeans for everyday streetwear or dress it down with wide-leg trousers for that effortless high-low mix.
```

Trace:

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are 2 outfit combinations using the Y2K Baby Tee and pieces you already own:  ### Outfit 1: Casual Y2K St…
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channeling major 2000s pop star energy with this butterfly print Y2K baby tee 🦋 Grab it on Depop in excellent …
```
```
# Criterion 2:
Source: `agent.py` — `run_agent()`
```

- stopped early: yes — I couldn't find any listings matching your search. Try a different search than 'designer ballgown', a different size than XXS, a higher price limit than $5.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] empty_search_handler
      out: I couldn't find any listings matching your search. Try a different search than 'designer ballgown', a differen…
      →    branch: empty, stopping
```
```

# Criterion 3:
Source: `agent.py` — `run_agent()`
```

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 6

Outfit suggestion:

```
Here are two outfit combinations using the new light wash cropped denim jacket and pieces you already own:

**Outfit 1: High-Contrast Casual**
*   **Top:** White ribbed tank top
*   **Bottom:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Denim Jacket — Light Wash, Cropped
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* This creates a cool "double denim" look with intentional contrast. The dark wash jeans ground the outfit, while the light wash cropped jacket and white tank keep the top half bright and balanced. The chunky sneakers and crossbody bag add a relaxed, modern streetwear vibe.

**Outfit 2: Smart-Casual Mix**
*   **Top:** White ribbed tank top (worn layered under) + Oversized grey crewneck sweatshirt (worn draped over the shoulders or layered underneath depending on the fit)
*   **Bottom:** Wide-leg khaki trousers
*   **Outerwear:** Denim Jacket — Light Wash, Cropped
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt
*   *Why it works:* Pairing the structured, light wash denim with tailored khaki trousers creates a great high-low mix. Tucking the white tank in with the brown leather belt adds definition at the waist, and the cropped length of the jacket pairs naturally with high-waisted wide-leg pants. Finish with black combat boots to add a little edge to the polished trousers.
```

Fit card:

```
The ultimate blank canvas jacket just dropped on Poshmark for $42 and I'm obsessed with the structured shoulders. Thinking of styling it for double denim or dressing it down with some wide-leg trousers for that effortless high-low mix. Such a good find for transitional weather!
```

Trace:

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 6 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +3 more
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two outfit combinations using the new light wash cropped denim jacket and pieces you already own:  **…
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: The ultimate blank canvas jacket just dropped on Poshmark for $42 and I'm obsessed with the structured shoulde…
```
```

# Criterion 4:
Source: `agent.py` — `run_agent()`
```

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Here are two specific outfit combinations using the Y2K Butterfly Baby Tee and pieces you already own:

**Outfit 1: Casual 90s Streetwear**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Layer:** Vintage black denim jacket
*   **Footwear:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* This plays on the classic Y2K silhouette of a fitted top paired with baggy, relaxed bottoms. The black denim jacket ties in the grunge/vintage edge, while the chunky white sneakers and crossbody bag keep it casual and practical for everyday wear.

**Outfit 2: Elevated Retro-Casual**
*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Footwear:** Black combat boots
*   *Why it works:* Tucking the baby tee into the wide-leg khakis creates a balanced, waist-defining shape. Adding the brown leather belt and grounding the outfit with black combat boots gives it a cool, slightly subversive contrast to the sweet, feminine butterfly graphic.
```

Fit card:

```
Obsessed with this Y2K butterfly baby tee—the pink and purple print is just too good. ✨ I'm listing it on Depop for $18, and it’s giving major early 2000s streetwear vibes whether you style it with baggy denim or cool utility trousers. Grab it before it's gone! 🦋
```

Trace:

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two specific outfit combinations using the Y2K Butterfly Baby Tee and pieces you already own:  **Outf…
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Obsessed with this Y2K butterfly baby tee—the pink and purple print is just too good. ✨ I'm listing it on Depo…
```
```

# Criterion 5:
Source: `agent.py` — `run_agent()`
```

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Here are two specific outfit combinations using the Y2K baby tee and pieces from your current wardrobe:

**Outfit 1: Casual Y2K Streetwear**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Layer:** Black cropped zip hoodie
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   **Why it works:** The fitted, cropped silhouette of the baby tee balances out the volume of the baggy dark wash jeans. Throwing the black cropped zip hoodie over top keeps it warm while maintaining that quintessential early 2000s proportion, and the chunky white sneakers tie the casual look together.

**Outfit 2: Elevated Retro Casual**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Wide-leg khaki trousers
*   **Belt:** Brown leather belt
*   **Shoes:** Black combat boots
*   **Layer:** Vintage black denim jacket (optional for cooler weather)
*   **Why it works:** This pairs the ultra-feminine, fitted pink and purple butterfly graphic with the more tailored, structured wide-leg khaki trousers. Tucking the tee in and adding the brown leather belt pulls the waistline together, while the black combat boots add a bit of edge to ground the sweetness of the top.
```

Fit card:

```
Total butterfly era obsession over this Y2K baby tee! It’s giving major early 2000s streetwear vibes, especially paired with baggy denim or wide-leg trousers. Grab it on depop for just $18 before I change my mind and keep it in my own closet. ✨🦋
```

Trace:

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two specific outfit combinations using the Y2K baby tee and pieces from your current wardrobe:  **Out…
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Total butterfly era obsession over this Y2K baby tee! It’s giving major early 2000s streetwear vibes, especial…
```
```
---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | matching query completes | 4/5 | MET | The tests showed that a matching query completed 5/5 times, which was above the 4/5 required to meet the criterion. |
| 2 | impossible query stops early | 5/5 | MET | The tests showed that 5/5 tests with impossible queries stopped early. |
| 3 | selected item state matches outfit input | 5/5 | MET | While the tests did not directly show item state, every run completed and gave a recommendation about the given item, so the right item must have passed. |
| 4 | fit card includes item details | 4/5 | MET | Every test (5/5) had the fit card include the name, price, and platform, which meets my criteria. |
| 5 | price ceiling is respected | 4/5 | MET | In all 5 tests, the price ceiling was respected by the code. |

**Diagnoses**

All criteria were met, so I don't have anything to diagnose.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two outfit combinations using the Y2K butterfly baby tee and pieces you already own:  ### Outfit 1: C…
[4] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channeling total 2000s pop princess energy with this pastel butterfly baby tee! It’s in amazing condition and …
```

**Empty search**

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] empty_search_handler
      out: I couldn't find any listings matching your search. Try a different search than 'futuristic battle armor', a hi…
      →    branch: empty, stopping
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed: I added a new_item_id field to the suggest outfit trace.**

**Which failure it was meant to fix: While I believe criterion 3 is met,it is difficult to verify directly from the evaluation evidence. The new trace information will make it easier to check whether the two IDs match.**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4/5  | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 2. impossible query stops early | 5/5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. selected item state matches outfit input | 5/5  | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 4. fit card includes item details | 4/5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 5. price ceiling is respected | 4/5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |

**Did it help, and how do I know: My changed did help, it made it much easier to verify Criteria 3. I know because in each try the trace now contains this line: `ID check: selected_item=lst_002, new_item=lst_002` which shows if the selected item and the new item have the same ID.**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
