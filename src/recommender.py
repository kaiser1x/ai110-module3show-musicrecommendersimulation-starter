import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class ScoringStrategy:
    """
    Strategy interface for scoring a song against a user profile.
    Lets the weighting scheme change (e.g. weight-shift experiments)
    without touching Recommender or its callers.
    """
    def score(self, user: "UserProfile", song: Song) -> float:
        raise NotImplementedError

    def explain(self, user: "UserProfile", song: Song) -> str:
        raise NotImplementedError


class WeightedScoring(ScoringStrategy):
    """
    Default scoring: genre match, mood match, energy proximity,
    each weighted independently.
    """
    def __init__(self, genre_weight: float = 2.0, mood_weight: float = 1.0):
        self.genre_weight = genre_weight
        self.mood_weight = mood_weight

    def score(self, user: "UserProfile", song: Song) -> float:
        genre_score = self.genre_weight if song.genre == user.favorite_genre else 0.0
        mood_score = self.mood_weight if song.mood == user.favorite_mood else 0.0
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        return genre_score + mood_score + energy_score

    def explain(self, user: "UserProfile", song: Song) -> str:
        parts = []
        if song.genre == user.favorite_genre:
            parts.append(f"genre match (+{self.genre_weight:.1f})")
        if song.mood == user.favorite_mood:
            parts.append(f"mood match (+{self.mood_weight:.1f})")
        energy_gap = abs(song.energy - user.target_energy)
        parts.append(f"energy proximity ({song.energy:.2f} vs target {user.target_energy:.2f}, +{1.0 - energy_gap:.2f})")
        return " | ".join(parts)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: Optional[ScoringStrategy] = None):
        self.songs = songs
        self.strategy = strategy or WeightedScoring()

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [
            (self.strategy.score(user, song), song)
            for song in self.songs
        ]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return self.strategy.explain(user, song)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []
    genre_score = 0.0
    if song["genre"] == user_prefs["genre"]:
        genre_score = 2.0
        reasons.append("genre match (+2.0)")

    mood_score = 0.0
    if song["mood"] == user_prefs["mood"]:
        mood_score = 1.0
        reasons.append("mood match (+1.0)")

    energy_gap = abs(song["energy"] - user_prefs["energy"])
    energy_score = 1.0 - energy_gap
    reasons.append(
        f"energy proximity ({song['energy']:.2f} vs target {user_prefs['energy']:.2f}, +{energy_score:.2f})"
    )

    total = genre_score + mood_score + energy_score
    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, " | ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
