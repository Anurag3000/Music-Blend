
from spotify_api import (
    get_token,
    get_track_and_artist_id
)

import time
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()  # loads the .env file

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_KEYS = [
    os.getenv("RAPIDAPI_KEY_1"),
    os.getenv("RAPIDAPI_KEY_2"),
    os.getenv("RAPIDAPI_KEY_3"),
    os.getenv("RAPIDAPI_KEY_4"),
    os.getenv("RAPIDAPI_KEY_5"),
    os.getenv("RAPIDAPI_KEY_6"),
    os.getenv("RAPIDAPI_KEY_7"),
    os.getenv("RAPIDAPI_KEY_8"),
    os.getenv("RAPIDAPI_KEY_9"),
    os.getenv("RAPIDAPI_KEY_10"),
    os.getenv("RAPIDAPI_KEY_11")
]

API_KEYS = [
    key for key in API_KEYS
    if key is not None
]

def enrich_track_artist_ids(df,CLIENT_ID, CLIENT_SECRET):
#   # =========================================
#   # GET TOKEN
#   # =========================================

#   token = get_token(CLIENT_ID, CLIENT_SECRET)


#   # =========================================
#   # CREATE NEW DATAFRAME
#   # =========================================

#   processed_data = []


#   for index, row in df.iterrows():

#       artist = row["artistName"]
#       song = row["trackName"]

#       print(f"Processing: {song} - {artist}")

#       result = get_track_and_artist_id(
#           song,
#           artist,
#           token
#       )

#       if result is not None:

#           processed_data.append({

#               "artist_id": result["artist_id"],

#               "artist_name": result["artist_name"],

#               "song_id": result["song_id"],

#               "song_name": result["song_name"],

#               "count": row["playCount"],

#               "totalMsPlayed": row["totalMsPlayed"],
#               "year_month": row["year_month"]

#           })

#       else:

#           processed_data.append({

#               "artist_id": None,

#               "artist_name": artist,

#               "song_id": None,

#               "song_name": song,

#               "count": row["playCount"],

#               "totalMsPlayed": row["totalMsPlayed"],
#               "year_month": row["year_month"]

#           })

#       # avoid rate limiting
#       time.sleep(0.2)


#   # =========================================
#   # CREATE FINAL DATAFRAME
#   # =========================================

# dtf1 = pd.DataFrame(processed_data)
  dtf1 = pd.read_csv("track_artist_ids.csv")
  sample_df = (
    dtf1[
        dtf1["song_id"].notna()
    ]
    .head(200)
    .sample(
        n=min(
            50,
            len(dtf1)
        ),
        random_state=42
    )
  )
# =========================================
# SAVE CSV
# =========================================

  return sample_df
