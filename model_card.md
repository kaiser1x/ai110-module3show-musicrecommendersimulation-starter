# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder tries to suggest songs you might enjoy based on three things you tell it: your favorite genre, the mood you are in, and how high-energy you want the music to feel. It does not learn from your behavior — it just scores every song in the catalog against your stated preferences and picks the best matches.

---

## 3. Data Used

- **Size:** 20 songs total (10 original + 10 added for variety)
- **Features per song:** genre, mood, energy (0.0–1.0), tempo, valence, danceability, acousticness
- **Genres covered:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, electronic, folk, metal, country, blues
- **Moods covered:** happy, chill, intense, relaxed, moody, focused, energetic, sad, nostalgic, euphoric, melancholic, upbeat, romantic, angry
- **Limits:** Very small catalog. Several moods only have one song. No world music, K-pop, or non-English genres represented. All songs are made-up for this simulation.

---

## 4. Algorithm Summary

The system works like a point system. For each song in the catalog, it asks three questions:

1. **Does the genre match?** If yes, award 2 points.
2. **Does the mood match?** If yes, award 1 point.
3. **How close is the energy?** Award up to 1 point — the closer the song's energy is to what the user asked for, the more points it gets.

Every song gets a total score. The top 5 highest-scoring songs are the recommendations. Genre is worth the most because a genre mismatch is usually the first thing you notice. Mood comes second. Energy fine-tunes the result.

---

## 5. Observed Behavior / Biases

**Genre takes over.** Because a genre match is worth 2 points, it can outweigh mood and energy combined. When we tested a profile asking for high-energy sad r&b, the system returned a very low-energy sad r&b song at #1 — just because it matched genre and mood. The user's energy request was basically ignored. A song from a different genre that actually matched the energy had no chance.

**Some moods only have one song.** If you ask for "euphoric" or "nostalgic," there is only one song in the catalog that qualifies. The system picks it automatically — not because it is the best match, but because it is the only option.

**The system cannot combine preferences it has never seen.** A user who wants "classical angry" music gets no real answer, because no song in the catalog is both classical AND angry at the same time. It returns the best partial matches instead.

---

## 6. Evaluation Process

Six profiles were tested:

| Profile | What we found |
|---|---|
| High-Energy Pop | Top result matched all three criteria. Felt right. |
| Chill Lofi | Perfect score (4.00). Best-case scenario when catalog coverage is good. |
| Deep Intense Rock | Only one rock song exists, so #1 was obvious. Not a real test of the system. |
| High Energy + Sad r&b (adversarial) | Genre weight dominated. Got a low-energy song despite asking for high energy. |
| Classical + Angry (adversarial) | No song matches both. System split the result — one classical, one angry. |
| Jazz + Relaxed (middle ground) | Clean, correct result. Felt genuinely accurate. |

We also ran a weight-shift experiment: halved the genre weight and doubled the energy weight. The top results stayed mostly the same, but songs from different genres crept higher when their energy was a close match. This showed the system is sensitive to how weights are set.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Learning how recommendation systems work
- Exploring how scoring rules affect results
- Classroom experimentation

**Not intended for:**
- Real music discovery (catalog is too small and made-up)
- Representing any real user's actual taste
- Making decisions about what music people "should" hear

---

## 8. Ideas for Improvement

1. **Expand the catalog** so each mood has at least 5 songs — right now, some moods have only one, so the system has nothing to compare.
2. **Allow partial genre matches** — for example, "indie pop" should count as a partial match for someone who likes "pop," not a zero.
3. **Let users set an energy range** instead of a single target — "somewhere between 0.6 and 0.9" is more realistic than "exactly 0.8."

---

## 9. Personal Reflection

The biggest thing I learned was that the weights matter more than the math. The formula itself is simple addition — what was actually hard was deciding how much a genre match should be worth compared to an energy match. There is no obviously correct answer. I just had to pick numbers, test them, and see what happened.

Using AI tools helped a lot in the early stages — getting the CSV loaded, figuring out how to structure the scoring function, and thinking through what "proximity scoring" even means. But I had to double-check a lot of the output. A few times the AI suggested code that worked but did something slightly different from what I intended, so actually reading the output and running test profiles was important.

What surprised me most was how much the results could "feel" right even though the system is just doing basic addition. When the "Chill Lofi" profile returned Library Rain at a perfect 4.00, it genuinely felt like a good recommendation — not because the math was fancy, but because the features lined up. That made me realize real recommenders are not magic. They are doing something similar, just with way more data and learned weights instead of hand-picked ones.

If I kept going, I would want to add real songs, let the system learn weights from what I actually skip or replay, and see if the "right feeling" holds up at a larger scale.
