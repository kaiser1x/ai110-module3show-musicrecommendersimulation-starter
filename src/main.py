"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print("User profile:")
    print(f"  Genre:  {user_prefs['genre']}")
    print(f"  Mood:   {user_prefs['mood']}")
    print(f"  Energy: {user_prefs['energy']}")
    print()

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top recommendations:")
    print("-" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']} — {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Score: {score:.2f}")
        print(f"    Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()
