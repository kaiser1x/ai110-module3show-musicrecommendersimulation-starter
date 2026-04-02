# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration — not for real users. It assumes a user can clearly state a single favorite genre and mood, which is rarely true in real life.

---

## 3. How the Model Works

Imagine you are a music store clerk. A customer walks in and says: "I like pop, I want something happy, and I want it high energy." You walk down the shelf and mentally grade every album: +2 points if it's pop, +1 point if the vibe is happy, and up to +1 point if the energy matches what they described. The album with the highest total is your first recommendation.

That is exactly what VibeFinder does. It checks every song in the catalog and assigns points based on three criteria — genre match, mood match, and how close the song's energy is to what the user asked for. The energy score uses proximity math: a song with energy 0.82 scores almost full points for a user targeting 0.80, while a song at 0.30 scores near zero. The songs are then sorted by total points and the top five are returned.

---

## 4. Data

The catalog contains 20 songs across 10 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, electronic, folk, metal, country, and blues. Moods represented include happy, chill, intense, relaxed, moody, focused, energetic, sad, nostalgic, euphoric, melancholic, upbeat, romantic, and angry. 10 songs were added to the original 10-song starter file to improve genre and mood diversity. The data reflects mainstream Western music tastes and does not include world music, reggae, K-pop, or non-English genres.

---

## 5. Strengths

The system works best when the user's preferred genre is well-represented in the catalog. The "Chill Lofi" profile returned a perfect 4.00 score for Library Rain because all three criteria (genre, mood, energy) aligned exactly. The scoring is fully transparent — every recommendation comes with a plain-language reason, making it easy to audit. Simple, well-defined user profiles (one genre, one mood, one energy target) consistently produce intuitive results.

---

## 6. Limitations and Bias

**Genre dominance.** A genre match alone awards +2.0 points — the same as a perfect mood + perfect energy combined. This means a pop song with the wrong mood and wrong energy can still outrank a non-pop song that matches both mood and energy perfectly. During testing, the adversarial "High Energy + Sad" r&b profile exposed this clearly: `3AM Letters` (r&b, sad, energy 0.33) ranked #1 despite having an energy gap of 0.57 from the target, simply because it matched genre and mood. The user asked for high-energy sad music; they got the only sad r&b track regardless of energy.

**Catalog sparsity.** Several moods have only one song each (euphoric, nostalgic, angry, romantic). A user targeting those moods gets that single song in #1 by default — the system has no real choice to make.

**Energy is symmetric but human preference is not.** The proximity formula treats "too quiet" and "too loud" equally. In practice, users tend to tolerate songs that are slightly more energetic than requested more than songs that are far too quiet.

**No cross-genre discovery.** A rock fan will never see a metal or blues song unless energy proximity pushes it into the top 5. The genre wall prevents serendipitous recommendations.

---

## 7. Evaluation

### Profiles tested

| Profile | Key finding |
|---|---|
| High-Energy Pop | Works as expected. #1 hit all three criteria (Sunrise City, score 3.92). #2 missed mood but matched genre + energy closely. |
| Chill Lofi | Perfect result. #1 scored 4.00 — exact energy match plus genre + mood. System behaves best when catalog coverage is dense. |
| Deep Intense Rock | Only one rock song in catalog → #1 is obvious. #2–5 rely on mood/energy proximity across unrelated genres. |
| Adversarial: High Energy + Sad (r&b) | Genre weight dominates. The system recommended the only sad r&b track (energy 0.33) over multiple high-energy non-r&b tracks. User wanted energy 0.9; they got 0.33. |
| Adversarial: Classical + Angry | The only classical song (nostalgic, not angry) ranked #1 on genre weight alone. The only angry song (metal) ranked #2. System cannot serve users who want a genre/mood combination that does not exist in the catalog. |
| Adversarial: Jazz + Relaxed + 0.5 energy | Clean result. Jazz is represented, relaxed mood exists. Coffee Shop Stories scored 3.87 and felt genuinely correct. |

### Weight-shift experiment

Halving genre weight (2.0 → 1.0) and doubling energy multiplier (1.0 × 2.0) changed the rankings:

- **High-Energy Pop:** Top 3 order unchanged, but `Rooftop Lights` (indie pop, wrong genre) jumped to #3 ahead of `Storm Runner` — energy proximity now matters more than genre exactness.
- **Adversarial High Energy + Sad:** `Storm Runner` (rock/intense, energy 0.91) jumped to #3, nearly matching the r&b genre+mood winner. With even higher energy weight, it would overtake — showing the system's sensitivity to weight choice.

**Conclusion:** The original weights favor genre loyalty. The shifted weights favor energy accuracy. Neither is objectively correct — it depends on whether the user cares more about *what type* of music or *how it feels*.

---

## 8. Future Work

- Add partial genre matching (e.g., "indie pop" counts as a 0.5 match for a "pop" user)
- Expand the catalog so each mood has at least 5 songs — currently some moods have only 1
- Let users specify an acceptable energy *range* (e.g., 0.7–0.9) rather than a single target
- Add a diversity filter so the same artist cannot appear more than once in the top 5
- Track implicit feedback (skips, replays) to adjust weights automatically over time

---

## 9. Personal Reflection

Building VibeFinder made clear that the *weights* are the real design decision in a rule-based recommender — the math is straightforward, but choosing how much a genre match should be worth compared to energy closeness requires genuine judgment about human taste. The adversarial "high energy + sad" profile was the most instructive test: it revealed that the system would rather give you a low-energy sad song than a high-energy song with the wrong mood, simply because genre and mood bonuses are flat (all-or-nothing) while energy is gradual. Real recommenders solve this by learning weights from millions of user interactions rather than guessing them — which explains why Spotify's recommendations often feel more nuanced than a simple scoring rule could achieve.
