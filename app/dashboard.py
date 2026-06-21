
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Spotify Analytics",
    layout="wide"
)

df = pd.read_csv(
    "spotify_final_dataset.csv"
)


from analytics import (
    top_artists,
    top_tracks,
    get_last_2_months,
    total_minutes_last_2_months,
    top_artists_last_2_months,
    top_tracks_last_2_months,
    music_mood_last_2_months
)


st.title(
    "🎵 Spotify Music Analytics Dashboard"
)

last2 = get_last_2_months(df)
minutes = total_minutes_last_2_months(last2)
# mood_result = music_mood_last_2_months(df)
unique_artists = df["artist_name"].nunique()


col1, col2, col3 = st.columns(3)

mood_data = music_mood_last_2_months(df)

st.metric(
    "Primary Mood",
    mood_data["mood"]["primary_mood"]
)
st.metric(
    "Secondary Mood",
    mood_data["mood"]["secondary_mood"]
)
with col2:
    st.metric(
        "Minutes Played",
        round(minutes)
    )

with col3:
    st.metric(
        "Unique Artists",
        unique_artists
    )


col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Top Artists"
    )

    st.dataframe(
        top_artists(df)
    )

with col2:

    st.subheader(
        "Top Tracks"
    )

    st.dataframe(
        top_tracks(df)
    )

st.subheader("Genre Distribution")
st.image("outputs/genre_distribution.png")
st.subheader("Music Profile")
st.image("outputs/music_profile_radar.png")
st.subheader("Last 2 Months")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(top_artists_last_2_months(last2))

with col2:
    st.dataframe(top_tracks_last_2_months(last2))
