"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print("\nUser profile:")
    print(f"  Genre:  {user_prefs['genre']}")
    print(f"  Mood:   {user_prefs['mood']}")
    print(f"  Energy: {user_prefs['energy']}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:")
    print("-" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} - {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Score: {score:.2f}")
        print(f"    Why:   {explanation}")


if __name__ == "__main__":
    main()
