# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Implement the TODO stubs in `src/recommender.py` (`load_songs`, `score_song`, `recommend_songs`, `Recommender.recommend`, `Recommender.explain_recommendation`) so the CLI in `src/main.py` actually runs and produces the scored, ranked output described in the README and model card.

**Prompts used:**

"Fill in recommender.py TODOs using the Algorithm Recipe from the README (genre +2, mood +1, energy proximity). Fix main.py's import so `python -m src.main` works. Expand the 10-song catalog to 20 songs to match model_card.md."

**What did the agent generate or change?**

- `src/recommender.py`: CSV loader (csv.DictReader), scoring function, sort-and-slice ranking, dataclass-based `Recommender.recommend`/`explain_recommendation`.
- `src/main.py`: fixed `from recommender import` (broke under `python -m src.main`) to `from src.recommender import`; reformatted print output to match target terminal layout.
- `data/songs.csv`: added 10 rows to bring catalog to 20 songs across hip-hop, r&b, classical, metal, blues, country, electronic, folk.

**What did you verify or fix manually?**

Ran `pytest` (2 passed) and `python -m src.main` and diffed the printed scores/reasons against the target screenshots line by line to confirm genre/mood/energy math matched exactly (e.g. Sunrise City score 3.98, Gold Chain Bounce energy-proximity 1.00). Also swapped an em dash in the output for a plain hyphen since Windows console (cp1252) garbled it.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy.

**How did AI help you brainstorm or implement it?**

The README documents a "weight-shift experiment" (genre weight 2.0 → 1.0, energy doubled) that originally required editing the scoring formula inline inside `Recommender._score`. Asked the agent how to make that experiment a config change instead of a code change — it suggested pulling the scoring formula out into a `ScoringStrategy` interface with a default `WeightedScoring` implementation, injected into `Recommender` at construction time.

**How does the pattern appear in your final code?**

`src/recommender.py`: `ScoringStrategy` (interface with `score`/`explain`) and `WeightedScoring(genre_weight, mood_weight)` (default implementation). `Recommender.__init__(songs, strategy=None)` takes an optional strategy and defaults to `WeightedScoring()`. Running the weight-shift experiment is now `Recommender(songs, WeightedScoring(genre_weight=1.0))` instead of editing the scoring method.
