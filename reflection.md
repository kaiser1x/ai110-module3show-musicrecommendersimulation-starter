# Reflection

## Comparing Profile Outputs

### High-Energy Pop vs. Chill Lofi

These two profiles produced the most opposite results, which is exactly what should happen. The pop/happy/0.9 profile surfaced Sunrise City at #1 (upbeat, fast, bright), while the lofi/chill/0.35 profile surfaced Library Rain at #1 (slow, quiet, studious). What changed: genre flipped completely, mood flipped completely, and energy went from the high end to the low end of the scale. The system correctly pushed every song to opposite ends of the ranking for each profile. This confirms the scoring logic is working — the math actually separates these two listener types.

The chill lofi profile also scored a perfect 4.00 because Library Rain matched all three criteria exactly (genre + mood + energy). The pop profile scored 3.92 because the best pop/happy song (Sunrise City) had energy 0.82 against a target of 0.90 — a small gap, but not zero. This shows the energy proximity score is doing real work even when genre and mood already match.

### Deep Intense Rock vs. Jazz Relaxed (Middle Profile)

Both profiles have a clear genre preference, but the rock catalog is thin (only one rock song: Storm Runner), while jazz has Coffee Shop Stories as a clean match. The rock profile's #1 was the obvious single match; positions #2–5 had to fall back on mood/energy proximity across totally different genres. The jazz profile felt more satisfying because the top result genuinely felt correct — a slow, warm jazz track for someone asking for relaxed jazz at energy 0.5.

The takeaway: a scoring system is only as good as the catalog behind it. Storm Runner ranking #1 for the rock user is not impressive — it was the only option. Coffee Shop Stories ranking #1 for the jazz user means something because there were real alternatives to compare against.

### Adversarial: High Energy + Sad (r&b) vs. Classical + Angry

Both adversarial profiles exposed the same underlying problem from different angles. The r&b/sad/0.9 user wanted high-energy sad music — a legitimate combination (think intense emotional ballads). The system gave them 3AM Letters at energy 0.33 because it was the only song matching both genre and mood, and genre+mood bonuses (3.0 points total) overwhelmed the energy penalty (only 0.57 gap, costing 0.57 points). The energy request was essentially ignored.

The classical/angry user faced the opposite problem: no song in the catalog has both classical genre AND angry mood. The system gave them Cathedral Echo (#1 by genre) and Iron Gates (#2 by mood), but neither was what they asked for. It is like asking a store clerk for "classical angry music" and they hand you one classical piece and one metal piece separately, unable to combine them.

These two profiles together reveal that the system cannot handle niche or conflicting taste combinations — it always finds the closest individual match, never a true intersection of preferences.

### Weight-Shift Experiment: Original vs. Doubled Energy

Switching from genre weight 2.0 to 1.0 (and doubling energy weight) did not change the #1 result for most profiles — the top song was usually correct either way. What changed was the gap between positions #1 and #2, and which non-matching songs appeared lower in the list. With higher energy weight, songs that were "close enough in energy" from unrelated genres crept upward. For the adversarial high-energy sad profile, Storm Runner (rock, energy 0.91) nearly overtook the r&b genre match because the energy gap penalty was now twice as large.

This means the weights are not just decoration — they control whose preferences the system respects more. A genre-loyal listener is better served by the original weights. A listener who cares mostly about "how it feels" (energy, intensity) is better served by the shifted weights. A real product would let users control this directly.
