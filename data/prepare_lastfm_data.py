"""
Prepare LastFM-2K HetRec 2011 dataset for the hybrid recommender system.

Converts the LastFM format to match the expected schema:
- Music Info.csv: track_id, name, artist, year, tags, spotify_preview_url,
                  danceability, energy, speechiness, acousticness,
                  instrumentalness, liveness, valence, tempo, loudness,
                  duration_ms, key, time_signature
- User Listening History.csv: user_id, track_id, playcount

Since LastFM data is at the artist level (not track level), each artist
is treated as a "track" for recommendation purposes.
Audio features are generated using deterministic random values seeded by
the artist ID to ensure reproducibility.
"""

import pandas as pd
import numpy as np
import os


def generate_audio_features(artist_id: int, seed_base: int = 42) -> dict:
    """Generate deterministic realistic audio features from artist ID."""
    rng = np.random.RandomState(seed_base + artist_id)

    return {
        "danceability": rng.beta(5, 3),        # 0-1, skewed toward 0.6
        "energy": rng.beta(4, 3),              # 0-1
        "speechiness": rng.beta(1.5, 10),      # 0-1, mostly low
        "acousticness": rng.beta(2, 5),        # 0-1
        "instrumentalness": rng.beta(1.2, 8),  # 0-1, mostly low
        "liveness": rng.beta(2, 6),            # 0-1
        "valence": rng.beta(4, 4),             # 0-1, centered
        "tempo": rng.normal(120, 30),          # BPM, ~60-180
        "loudness": rng.normal(-8, 4),         # dB, ~-20 to 0
        "duration_ms": int(rng.normal(240000, 60000)),  # ~3-5 min
        "key": rng.randint(0, 12),             # 0-11
        "time_signature": rng.choice([3, 4, 5], p=[0.1, 0.8, 0.1]),
    }


def prepare_data():
    """Convert LastFM-2K to project schema."""
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # Load LastFM data
    print("Loading LastFM-2K data...")
    artists = pd.read_csv(os.path.join(data_dir, "artists.dat"), sep="\t")
    user_artists = pd.read_csv(os.path.join(data_dir, "user_artists.dat"), sep="\t")
    tags_df = pd.read_csv(os.path.join(data_dir, "tags.dat"), sep="\t", encoding="latin-1")
    user_tags = pd.read_csv(os.path.join(data_dir, "user_taggedartists.dat"), sep="\t")

    print(f"  Artists: {len(artists)}")
    print(f"  User-Artist interactions: {len(user_artists)}")
    print(f"  Tags: {len(tags_df)}")

    # Build artist tags: aggregate all tags per artist
    print("Building artist tags...")
    tag_map = tags_df.set_index("tagID")["tagValue"].to_dict()
    user_tags["tag_name"] = user_tags["tagID"].map(tag_map)
    artist_tags = (
        user_tags.groupby("artistID")["tag_name"]
        .apply(lambda x: " ".join(x.dropna().unique()[:20]))  # Top 20 unique tags
        .reset_index()
    )
    artist_tags.columns = ["artistID", "tags"]

    # Build year from tagging timestamps (average tag year as proxy)
    artist_years = (
        user_tags.groupby("artistID")["year"]
        .median()
        .astype(int)
        .reset_index()
    )
    artist_years.columns = ["artistID", "year"]

    # Merge artist info
    print("Building Music Info...")
    music_info = artists[["id", "name"]].copy()
    music_info.columns = ["track_id", "name"]

    # Use artist name as both name and artist (since data is artist-level)
    music_info["artist"] = music_info["name"]
    music_info["track_id"] = music_info["track_id"].astype(str)

    # Ensure consistent types for merging
    artist_tags["artistID"] = artist_tags["artistID"].astype(str)
    artist_years["artistID"] = artist_years["artistID"].astype(str)

    # Merge tags
    music_info = music_info.merge(
        artist_tags, left_on="track_id", right_on="artistID", how="left"
    ).drop(columns=["artistID"], errors="ignore")
    music_info["tags"] = music_info["tags"].fillna("no_tags")

    # Merge years
    music_info = music_info.merge(
        artist_years, left_on="track_id",
        right_on="artistID", how="left"
    ).drop(columns=["artistID"], errors="ignore")
    music_info["year"] = music_info["year"].fillna(2009).astype(int)

    # Generate audio features
    print("Generating audio features...")
    audio_features = []
    for tid in music_info["track_id"]:
        audio_features.append(generate_audio_features(int(tid)))

    audio_df = pd.DataFrame(audio_features)
    music_info = pd.concat([music_info, audio_df], axis=1)

    # Clip to realistic ranges
    music_info["tempo"] = music_info["tempo"].clip(40, 220)
    music_info["loudness"] = music_info["loudness"].clip(-25, 0)
    music_info["duration_ms"] = music_info["duration_ms"].clip(60000, 600000)

    # Add placeholder spotify preview URL
    music_info["spotify_preview_url"] = ""

    # Reorder columns to match expected schema
    column_order = [
        "track_id", "name", "artist", "year", "tags", "spotify_preview_url",
        "danceability", "energy", "speechiness", "acousticness",
        "instrumentalness", "liveness", "valence", "tempo", "loudness",
        "duration_ms", "key", "time_signature"
    ]
    music_info = music_info[column_order]

    # Save Music Info
    music_info_path = os.path.join(data_dir, "Music Info.csv")
    music_info.to_csv(music_info_path, index=False)
    print(f"  Saved Music Info: {len(music_info)} tracks -> {music_info_path}")

    # Build User Listening History
    print("Building User Listening History...")
    user_history = user_artists[["userID", "artistID", "weight"]].copy()
    user_history.columns = ["user_id", "track_id", "playcount"]
    user_history["user_id"] = user_history["user_id"].astype(str)
    user_history["track_id"] = user_history["track_id"].astype(str)

    history_path = os.path.join(data_dir, "User Listening History.csv")
    user_history.to_csv(history_path, index=False)
    print(f"  Saved User Listening History: {len(user_history)} interactions -> {history_path}")

    # Print summary stats
    print("\n=== Dataset Summary ===")
    print(f"  Tracks (artists): {len(music_info)}")
    print(f"  Users: {user_history['user_id'].nunique()}")
    print(f"  Interactions: {len(user_history)}")
    sparsity = 1 - len(user_history) / (len(music_info) * user_history['user_id'].nunique())
    print(f"  Sparsity: {sparsity:.4f}")
    print(f"  Avg interactions/user: {len(user_history) / user_history['user_id'].nunique():.1f}")
    print(f"  Unique tags: {len(tags_df)}")


if __name__ == "__main__":
    prepare_data()
