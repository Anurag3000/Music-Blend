
from spotify_api import (
    get_audio_features,
    get_artist_genres
)
from generate_track_artists_ids import API_KEYS

import pandas as pd
import time

def enrich_audio_and_genres(dtf2, headers):
  # headers={
  #     "x-rapidapi-key": "8814ea78a1msh30614356e5ec298p15f105jsnbbc911375a5f",
  #     "x-rapidapi-host": "spotify-extended-audio-features-api.p.rapidapi.com"
  # }

  headers = headers

  # ==========================================
  # FIND UNPROCESSED ROWS
  # ==========================================

  # if danceability OR genres missing,
  # treat as unprocessed

  # unprocessed_mask = (

  #     (
  #         dtf2['danceability'].isna()
  #         |
  #         dtf2['genres'].isna()
  #     )

  #     &

  #     dtf2['song_id'].notna()

  # )


  # # ==========================================
  # # TAKE NEXT 5 ROWS
  # # ==========================================

  # batch_to_process = dtf2[
  #     unprocessed_mask
  # ]


  # # ==========================================
  # # PROCESS BATCH
  # # ==========================================

  # if batch_to_process.empty:

  #     print("ALL TRACKS PROCESSED")

  # else:

  #     print(
  #         f"Processing next "
  #         f"{len(batch_to_process)} tracks..."
  #     )

  #     BATCH_SIZE = 5

  #     for batch_num, start in enumerate(
  #         range(0, len(batch_to_process), BATCH_SIZE)):
  #         batch = batch_to_process.iloc[
  #             start:start+BATCH_SIZE
  #         ]

  #         api_key = API_KEYS[
  #             batch_num % len(API_KEYS)
  #         ]

  #         headers = {
  #             "x-rapidapi-key": api_key,
  #             "x-rapidapi-host":
  #             "spotify-extended-audio-features-api.p.rapidapi.com"
  #         }

  #         print(
  #             f"\nUsing API Key "
  #             f"{batch_num % len(API_KEYS)+1}"
  #         )

  #         print(
  #             f"Using API Key {batch_num+1}"
  #         )

  #         print(
  #             f"Processing rows {start} to "
  #             f"{min(start+BATCH_SIZE-1, len(batch_to_process)-1)}"
  #         )
  #         for idx, row in batch.iterrows():

  #             track_id = row['song_id']
  #             artist_id = row['artist_id']

  #             print(
  #                 f"\nProcessing:\n"
  #                 f"Track: {track_id}\n"
  #                 f"Artist: {artist_id}"
  #             )

  #             # ==================================
  #             # AUDIO FEATURES
  #             # ==================================

  #             audio_features = get_audio_features(
  #                 track_id, headers
  #             )

  #             # ==================================
  #             # GENRES
  #             # ==================================

  #             genres = get_artist_genres(
  #                 artist_id, headers
  #             )

  #             # ==================================
  #             # UPDATE DATAFRAME
  #             # ==================================

  #             for key, value in audio_features.items():

  #                 dtf2.at[idx, key] = value

  #             dtf2.at[idx, 'genres'] = genres

  #             print("DONE")

  # # ==========================================
  # # SAVE UPDATED CSV
  # # ==========================================

  # dtf2.to_csv(
  #     "userHistoryPreprocessed.csv",
  #     index=False
  # )

  # print(
  #     "\nUPDATED CSV SAVED"
  # )
  dtf2=pd.read_csv("userHistoryPreprocessed.csv")
  return dtf2
