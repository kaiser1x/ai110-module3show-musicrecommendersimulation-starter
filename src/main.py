"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a labeled recommendation block for one user profile."""
    print(f"\n{'=' * 60}")
    print(f"Profile: {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print(f"{'=' * 60}")

    results = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"#{rank}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Score: {score:.2f}")
        print(f"    Why:   {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Standard profiles ---
    print_recommendations(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.9},
        songs,
    )

    print_recommendations(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.35},
        songs,
    )

    print_recommendations(
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.95},
        songs,
    )

    # --- Adversarial / edge-case profiles ---
    print_recommendations(
        "Adversarial: High Energy + Sad Mood (conflicting)",
        {"genre": "r&b", "mood": "sad", "energy": 0.9},
        songs,
    )

    print_recommendations(
        "Adversarial: Genre with Zero Catalog Matches (classical + angry)",
        {"genre": "classical", "mood": "angry", "energy": 0.5},
        songs,
    )

    print_recommendations(
        "Adversarial: Perfect Middle (no strong preference)",
        {"genre": "jazz", "mood": "relaxed", "energy": 0.5},
        songs,
    )


if __name__ == "__main__":
    main()
