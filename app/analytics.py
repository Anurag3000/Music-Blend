
import matplotlib.pyplot as plt
import numpy as np
import os

from joblib import load
import json

MODEL_DIR = "/content/drive/MyDrive/music-analytics/models"

scaler = load(f"{MODEL_DIR}/scaler.pkl")
kmeans = load(f"{MODEL_DIR}/kmeans.pkl")


with open(f"{MODEL_DIR}/cluster_labels.json") as f:
    cluster_labels = json.load(f)


os.makedirs(
    "outputs",
    exist_ok=True
)

audio_features = [
    'danceability',
    'energy',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo'
]

def genre_distribution(dtf3):

    genre_cols = [
        col for col in dtf3.columns
        if col.startswith("genre_")
    ]

    genre_counts = dtf3[genre_cols].sum(numeric_only=True)

    genre_df = genre_counts.reset_index()
    genre_df.columns = ["genre", "frequency"]

    plt.figure(figsize=(8,8))

    plt.pie(
        genre_df["frequency"].astype(float),
        labels=genre_df["genre"],
        autopct="%1.1f%%"
    )

    plt.title("Genre Distribution")

    plt.savefig(
        "outputs/genre_distribution.png",
        bbox_inches="tight"
    )

    plt.close()

    return genre_df

def top_artists(dtf3):
  artist_count=dtf3.iloc[:, 1].groupby(dtf3.iloc[:, 1]).count()
  top_5_artists = artist_count.sort_values(ascending=False).head(5)
  top_5_df = top_5_artists.rename('count').reset_index()

  artist_count = (
        dtf3.groupby("artist_name")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

  plt.figure(figsize=(10,5))

  artist_count.plot(
      kind="bar"
  )

  plt.title(
      "Top Artists"
  )

  plt.ylabel(
      "Play Count"
  )

  plt.tight_layout()

  plt.savefig(
      "outputs/top_artists.png"
  )

  plt.close()

  return top_5_df

def top_tracks(df):
  top_tracks = (
    df.groupby("song_name")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
  )
  plt.figure(figsize=(10,5))

  top_tracks.plot(
      kind="bar"
  )

  plt.title(
      "Top Tracks"
  )

  plt.ylabel(
      "Play Count"
  )

  plt.tight_layout()

  plt.savefig(
      "outputs/top_tracks.png"
  )

  plt.close()
  return top_tracks


def get_last_2_months(df):
  import pandas as pd

  df["year_month"] = pd.to_datetime(df["year_month"])
  latest_month = df["year_month"].max()
  last_2_months = df[
    df["year_month"] >= (latest_month - pd.DateOffset(months=1))
  ]
  return last_2_months

def total_minutes_last_2_months(last_2_months):
  total_minutes = last_2_months["totalMsPlayed"].sum() / (1000 * 60)

  return total_minutes

def top_artists_last_2_months(last_2_months):
  top_artists = (
    last_2_months
    .groupby("artist_name")["totalMsPlayed"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
  )

  top_artists["minutes_played"] = top_artists["totalMsPlayed"] / (1000 * 60)

  # print("\nTop Artists (Last 2 Months)")
  artists = (
        last_2_months
        .groupby("artist_name")
        ["totalMsPlayed"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        / (1000*60)
    )

  plt.figure(figsize=(10,5))

  artists.plot(
      kind="bar"
  )

  plt.ylabel(
      "Minutes Played"
  )

  plt.title(
      "Top Artists (Last 2 Months)"
  )

  plt.tight_layout()

  plt.savefig(
      "outputs/top_artists_last2months.png"
  )

  plt.close()
  return top_artists[["artist_name", "minutes_played"]].head(5)

def top_tracks_last_2_months(last_2_months):

  # --------------------------------------------------
  # 3. Top Tracks (Last 2 Months)
  # --------------------------------------------------
  top_tracks = (
      last_2_months
      .groupby(["song_name", "artist_name"])["totalMsPlayed"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
  )

  top_tracks["minutes_played"] = top_tracks["totalMsPlayed"] / (1000 * 60)

  tracks = (
        last_2_months
        .groupby("song_name")
        ["totalMsPlayed"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        / (1000*60)
    )

  plt.figure(figsize=(10,5))

  tracks.plot(
      kind="bar"
  )

  plt.ylabel(
      "Minutes Played"
  )

  plt.title(
      "Top Tracks (Last 2 Months)"
  )

  plt.tight_layout()

  plt.savefig(
      "outputs/top_tracks_last2months.png"
  )

  plt.close()
  return top_tracks[["song_name", "artist_name", "minutes_played"]].head(5)


def get_audio_profile(df_last2):

  weights = df_last2["totalMsPlayed"]

  profile = {
      "danceability": (df_last2["danceability"] * weights).sum() / weights.sum(),
      "energy": (df_last2["energy"] * weights).sum() / weights.sum(),
      "valence": (df_last2["valence"] * weights).sum() / weights.sum(),
      "acousticness": (df_last2["acousticness"] * weights).sum() / weights.sum(),
      "instrumentalness": (df_last2["instrumentalness"] * weights).sum() / weights.sum(),
      "speechiness": (df_last2["speechiness"] * weights).sum() / weights.sum(),
      "tempo": (df_last2["tempo"] * weights).sum() / weights.sum()
  }

  return profile

def classify_music_mood(profile):

    energy = profile["energy"]
    valence = profile["valence"]
    danceability = profile["danceability"]
    acousticness = profile["acousticness"]
    instrumentalness = profile["instrumentalness"]

    scores = {
        "Party / Energetic ":
            max(0, energy - 0.5) *
            max(0, valence - 0.5),

        "Workout / Aggressive ":
            max(0, energy - 0.5) *
            max(0, 0.5 - valence),

        "Acoustic / Relaxed ":
            acousticness * (1 - energy),

        "Focus / Study ":
            instrumentalness * (1 - energy),

        "Melancholic ":
            (1 - valence) * (1 - energy),

        "Dance / Groovy ":
            danceability * energy
    }

    total = sum(scores.values())

    if total == 0:
        percentages = {
            mood: 0
            for mood in scores
        }
    else:
        percentages = {
            mood: round(score / total * 100, 1)
            for mood, score in scores.items()
        }

    ranked = sorted(
        percentages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_mood = ranked[0][0]
    secondary_mood = ranked[1][0]

    # --------------------------
    # Donut Chart
    # --------------------------

    labels = list(percentages.keys())
    values = list(percentages.values())

    plt.figure(figsize=(8, 8))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.85
    )

    centre_circle = plt.Circle(
        (0, 0),
        0.70,
        fc="white"
    )

    ax = plt.gca()
    ax.add_artist(centre_circle)

    plt.text(
        0,
        0,
        primary_mood,
        ha="center",
        va="center",
        fontsize=10,
        wrap=True
    )

    plt.title(
        "Music Mood Distribution"
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/music_mood_distribution.png",
        bbox_inches="tight",
        dpi=300
    )

    plt.close()

    return {
        "primary_mood": primary_mood,
        "secondary_mood": secondary_mood,
        "scores": percentages
    }

def music_mood_last_2_months(df):

  df_last2 = get_last_2_months(df)

  profile = get_audio_profile(df_last2)

  mood = classify_music_mood(profile)

  return {
      "mood": mood,
      "profile": profile
  }


def plot_listener_mood(mood):

    plt.figure(figsize=(6,3))

    plt.text(
        0.5,
        0.5,
        mood,
        fontsize=18,
        ha="center"
    )

    plt.axis("off")

    plt.savefig(
        "outputs/listener_mood.png"
    )

    plt.close()

def get_cluster_overlap(user_df):

    X = user_df[audio_features]

    X_scaled = scaler.transform(
        X.fillna(0)
    )

    user_df["cluster"] = kmeans.predict(
        X_scaled
    )

    overlap = (
        user_df["cluster"]
        .value_counts(normalize=True)
        .sort_index()
        * 100
    )

    result = {}

    for cluster_id, pct in overlap.items():

        label = cluster_labels[str(cluster_id)]

        result[label] = round(
            float(pct),
            2
        )

    return result
