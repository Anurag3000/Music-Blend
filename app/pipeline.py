
# ==========================================
# IMPORTS
# ==========================================

import os
import pandas as pd

from dotenv import load_dotenv

# preprocessing
from preprocess import (
    create_monthly_summary
)

# spotify enrichment
from generate_track_artists_ids import (
    enrich_track_artist_ids
)

from generate_audio_genres_features import (
    enrich_audio_and_genres
)

# genre encoding
from genre_encoding import (
    one_hot_encode_genres
)

# analytics
from analytics import (
    genre_distribution,
    top_artists,
    top_tracks,
    get_last_2_months,
    total_minutes_last_2_months,
    top_artists_last_2_months,
    top_tracks_last_2_months,
    music_mood_last_2_months,
    classify_music_mood,
    get_cluster_overlap
)

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
print(CLIENT_ID)
# ==========================================
# RAPID API HEADERS
# ==========================================

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host":
    "spotify-extended-audio-features-api.p.rapidapi.com"
}


# ==========================================
# MAIN PIPELINE
# ==========================================

def run_pipeline(json_file):

    print("\nSTEP 1 : Monthly Summary")
    print("-"*50)

    summary_df = create_monthly_summary(
        json_file
    )

    print(summary_df.head())


    # ======================================
    # STEP 2
    # ======================================

    print("\nSTEP 2 : Artist & Song IDs")
    print("-"*50)

    ids_df = enrich_track_artist_ids(
        summary_df,
        CLIENT_ID,
        CLIENT_SECRET
    )

    ids_df.to_csv(
        "track_artist_ids.csv",
        index=False
    )

    print(ids_df.head())


    # ======================================
    # STEP 3
    # ======================================

    print("\nSTEP 3 : Audio Features + Genres")
    print("-"*50)

    feature_cols = [
        "danceability",
        "energy",
        "valence",
        "tempo",
        "acousticness",
        "instrumentalness",
        "liveness",
        "speechiness",
        "genres"
    ]

    for col in feature_cols:

        if col not in ids_df.columns:
            ids_df[col] = pd.NA


    enriched_df = enrich_audio_and_genres(
        ids_df,
        HEADERS
    )

    enriched_df.to_csv(
        "spotify_enriched.csv",
        index=False
    )

    print(enriched_df.head())


    profile = get_cluster_overlap(
    enriched_df
    )

    print(profile)

    profile_df = pd.DataFrame(
    profile.items(),
    columns=["Genre","Percent"]
    )

    profile_df.to_csv("profileUsingKMEANS.csv")

    # ======================================
    # STEP 4
    # ======================================

    print("\nSTEP 4 : Genre Encoding")
    print("-"*50)

    encoded_df = one_hot_encode_genres(
        enriched_df
    )

    encoded_df.to_csv(
        "spotify_final_dataset.csv",
        index=False
    )

    print(encoded_df.shape)


    # ======================================
    # STEP 5
    # ======================================

    print("\nSTEP 5 : Analytics")
    print("-"*50)

    # Genre Pie Chart

    genre_distribution(encoded_df)


    # --------------------------------------
    # Top Artists
    # --------------------------------------

    print("\nTop Artists")

    print(
        top_artists(encoded_df)
    )


    # --------------------------------------
    # Top Tracks
    # --------------------------------------

    print("\nTop Tracks")

    print(
        top_tracks(encoded_df)
    )


    # --------------------------------------
    # Last 2 Months Stats
    # --------------------------------------

    last2 = get_last_2_months(
        encoded_df
    )

    minutes = total_minutes_last_2_months(
        last2
    )

    print(
        f"\nTotal Minutes Played "
        f"(Last 2 Months): "
        f"{minutes:.2f}"
    )


    print(
        "\nTop Artists "
        "(Last 2 Months)"
    )

    print(
        top_artists_last_2_months(
            last2
        )
    )


    print(
        "\nTop Tracks "
        "(Last 2 Months)"
    )

    print(
        top_tracks_last_2_months(
            last2
        )
    )


    # --------------------------------------
    # Music Mood
    # --------------------------------------

    mood_result = music_mood_last_2_months(
        encoded_df
    )

    print(
        "\nDetected Music Mood:"
    )

    print(
        mood_result["mood"]
    )


    print(
        "\nAudio Profile:"
    )

    print(
        mood_result["profile"]
    )


    classify_music_mood(
        mood_result["profile"]
    )

    print(
        "\nMusic profile radar chart saved."
    )

    print(
        "\nPIPELINE COMPLETED SUCCESSFULLY"
    )

    return encoded_df


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    JSON_FILE = "StreamingHistory_music_0.json"

    final_df = run_pipeline(
        JSON_FILE
    )
