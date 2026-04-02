# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a content-based music recommender that scores songs against a user taste profile using weighted feature matching. It simulates how real recommenders turn data into ranked suggestions, using a 20-song catalog spanning 10 genres and 10 moods, with features including genre, mood, energy, valence, tempo, danceability, and acousticness.

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from massive behavioral datasets — what you skip, replay, or save — and find patterns across millions of users. My version is a simplified, transparent simulation: instead of learning from behavior, it uses a manually designed scoring formula based on explicit user preferences. The user supplies a favorite genre, a preferred mood, and a target energy level. The system then loops over every song in the catalog, computes a score for each one based on how closely it matches those preferences, and returns the top-k highest-scoring songs. This prioritizes explainability over personalization depth.

### User Profile

```python
user_prefs = {
    "genre":  "hip-hop",   # favorite genre
    "mood":   "energetic", # desired mood
    "energy": 0.85,        # target energy (0.0–1.0)
}
```

This profile can clearly differentiate "intense rock" from "chill lofi": a rock/intense song scores +2.0 (genre) + 0 (mood mismatch) + proximity(energy) whereas a lofi/chill song scores 0 + 0 + a large energy penalty. The profile is intentionally narrow by design — a wide profile (e.g., no genre preference) would need a fallback weight strategy.

### Song Features

| Feature | Type | Description |
|---|---|---|
| `genre` | categorical | pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, electronic, folk, metal, country, blues |
| `mood` | categorical | happy, chill, intense, relaxed, moody, focused, energetic, sad, nostalgic, euphoric, melancholic, upbeat, romantic, angry |
| `energy` | float 0–1 | Intensity and loudness |
| `valence` | float 0–1 | Musical positivity (high = cheerful, low = dark) |
| `tempo_bpm` | float | Beats per minute |
| `danceability` | float 0–1 | Suitability for dancing |
| `acousticness` | float 0–1 | Acoustic vs. electronic character |

### Algorithm Recipe

**Step 1 — Score each song individually:**

```
genre_score  = 2.0  if song.genre == user.genre  else 0.0
mood_score   = 1.0  if song.mood  == user.mood   else 0.0
energy_score = 1.0 - abs(song.energy - user.target_energy)  # proximity: 1.0 = perfect match

total_score = genre_score + mood_score + energy_score
```

Genre is worth 2× a mood match because genre mismatch is immediately audible and usually a dealbreaker. Mood is worth 1× because two songs of the same genre can feel completely different emotionally. Energy uses proximity scoring — a song too quiet or too intense for the user loses points proportionally.

**Step 2 — Rank all songs:**

```
ranked = sorted(all_songs, key=lambda s: score(s, user), reverse=True)
return ranked[:k]
```

### Data Flow

```mermaid
flowchart LR
    A([User Profile\ngenre · mood · energy]) --> B[Loop over\nevery song in CSV]
    B --> C{Score each song\ngenre +2 · mood +1\nenergy proximity}
    C --> D[Sort all scores\ndescending]
    D --> E([Top-K\nRecommendations])
```

### Expected Biases

- **Genre dominance:** A genre match alone (+2.0) outweighs a perfect mood+energy match (max +2.0 combined). Great songs that match the user's mood and energy but miss on genre will be buried.
- **Mood sparsity:** The catalog has uneven mood coverage — moods like `euphoric` and `nostalgic` have only one song each, so those users get limited choices regardless of score.
- **Energy is linear:** The proximity formula treats `0.1` above target the same as `0.1` below. In practice, users often tolerate songs that are slightly more energetic than preferred more than songs that are significantly less.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Terminal Output

Running `python -m src.main` with the default `pop / happy / 0.8` profile:

![CLI Verification](CLI%20Verification.png)

```
Loaded songs: 20

User profile:
  Genre:  pop
  Mood:   happy
  Energy: 0.8

Top recommendations:
------------------------------------------------------------
#1  Sunrise City — Neon Echo
    Genre: pop  |  Mood: happy  |  Energy: 0.82
    Score: 3.98
    Why:   genre match (+2.0) | mood match (+1.0) | energy proximity (0.82 vs target 0.80, +0.98)

#2  Gym Hero — Max Pulse
    Genre: pop  |  Mood: intense  |  Energy: 0.93
    Score: 2.87
    Why:   genre match (+2.0) | energy proximity (0.93 vs target 0.80, +0.87)

#3  Rooftop Lights — Indigo Parade
    Genre: indie pop  |  Mood: happy  |  Energy: 0.76
    Score: 1.96
    Why:   mood match (+1.0) | energy proximity (0.76 vs target 0.80, +0.96)

#4  Gold Chain Bounce — Crate Kings
    Genre: hip-hop  |  Mood: upbeat  |  Energy: 0.8
    Score: 1.00
    Why:   energy proximity (0.80 vs target 0.80, +1.00)

#5  Night Drive Loop — Neon Echo
    Genre: synthwave  |  Mood: moody  |  Energy: 0.75
    Score: 0.95
    Why:   energy proximity (0.75 vs target 0.80, +0.95)
```

The results match expectations: `#1` hits all three criteria (genre + mood + close energy), `#2` matches genre but misses mood, and lower ranks rely on energy proximity alone.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

