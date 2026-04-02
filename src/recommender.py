import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio/metadata attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences for recommendations."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        """Initialize with a catalog of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs sorted by score for the given user profile."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dicts = [
            {
                "id": s.id,
                "title": s.title,
                "artist": s.artist,
                "genre": s.genre,
                "mood": s.mood,
                "energy": s.energy,
                "tempo_bpm": s.tempo_bpm,
                "valence": s.valence,
                "danceability": s.danceability,
                "acousticness": s.acousticness,
            }
            for s in self.songs
        ]
        results = recommend_songs(prefs, song_dicts, k=k)
        ranked_titles = [r[0]["title"] for r in results]
        return sorted(self.songs, key=lambda s: ranked_titles.index(s.title) if s.title in ranked_titles else 999)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
        }
        _, reasons = score_song(prefs, song_dict)
        return "; ".join(reasons) if reasons else "No strong match found"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score, reasons).

    Scoring recipe:
      +2.0 for genre match
      +1.0 for mood match
      +proximity for energy  (1.0 - abs(song_energy - target_energy))
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match — highest weight because genre mismatch is immediately audible
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy proximity — rewards closeness, not just high or low values
    target_energy = user_prefs.get("energy", 0.5)
    song_energy = song.get("energy", 0.5)
    energy_score = round(1.0 - abs(song_energy - target_energy), 3)
    score += energy_score
    reasons.append(f"energy proximity ({song_energy:.2f} vs target {target_energy:.2f}, +{energy_score:.2f})")

    return round(score, 3), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank by score descending, and return the top-k results.

    Returns a list of (song_dict, score, explanation) tuples.
    Uses sorted() rather than list.sort() to avoid mutating the original catalog.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() returns a new list — the original `songs` list is never mutated
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
