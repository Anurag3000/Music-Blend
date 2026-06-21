
import time
import pandas as pd

def enrich_track_artist_ids(df):
  # =========================================
  # GET TOKEN
  # =========================================

  token = get_token()


  # =========================================
  # CREATE NEW DATAFRAME
  # =========================================

  processed_data = []


  for index, row in df.iterrows():

      artist = row["artistName"]
      song = row["trackName"]

      print(f"Processing: {song} - {artist}")

      result = get_track_and_artist_id(
          song,
          artist,
          token
      )

      if result is not None:

          processed_data.append({

              "artist_id": result["artist_id"],

              "artist_name": result["artist_name"],

              "song_id": result["song_id"],

              "song_name": result["song_name"],

              "count": row["playCount"],

              "totalMsPlayed": row["totalMsPlayed"],
              "year_month": row["year_month"]

          })

      else:

          processed_data.append({

              "artist_id": None,

              "artist_name": artist,

              "song_id": None,

              "song_name": song,

              "count": row["playCount"],

              "totalMsPlayed": row["totalMsPlayed"],
              "year_month": row["year_month"]

          })

      # avoid rate limiting
      time.sleep(0.2)


  # =========================================
  # CREATE FINAL DATAFRAME
  # =========================================

  dtf1 = pd.DataFrame(processed_data)


  # =========================================
  # SAVE CSV
  # =========================================

  dtf1.to_csv(
      "userHistoryPreprocessed.csv",
      index=False
  )


  print("\nDONE")

def enrich_audio_and_genres(dtf2):
  headers = {
      "x-rapidapi-key": "8814ea78a1msh30614356e5ec298p15f105jsnbbc911375a5f",
      "x-rapidapi-host": "spotify-extended-audio-features-api.p.rapidapi.com"
  }

  # ==========================================
  # FIND UNPROCESSED ROWS
  # ==========================================

  # if danceability OR genres missing,
  # treat as unprocessed

  unprocessed_mask = (

      (
          dtf2['danceability'].isna()
          |
          dtf2['genres'].isna()
      )

      &

      dtf2['song_id'].notna()

  )


  # ==========================================
  # TAKE NEXT 5 ROWS
  # ==========================================

  batch_to_process = dtf2[
      unprocessed_mask
  ].head(5)


  # ==========================================
  # PROCESS BATCH
  # ==========================================

  if batch_to_process.empty:

      print("ALL TRACKS PROCESSED")

  else:

      print(
          f"Processing next "
          f"{len(batch_to_process)} tracks..."
      )

      for idx, row in batch_to_process.iterrows():

          track_id = row['song_id']
          artist_id = row['artist_id']

          print(
              f"\nProcessing:\n"
              f"Track: {track_id}\n"
              f"Artist: {artist_id}"
          )

          # ==================================
          # AUDIO FEATURES
          # ==================================

          audio_features = get_audio_features(
              track_id, headers
          )

          # ==================================
          # GENRES
          # ==================================

          genres = get_artist_genres(
              artist_id, headers
          )

          # ==================================
          # UPDATE DATAFRAME
          # ==================================

          for key, value in audio_features.items():

              dtf2.at[idx, key] = value

          dtf2.at[idx, 'genres'] = genres

          print("DONE")

  # ==========================================
  # SAVE UPDATED CSV
  # ==========================================

  dtf2.to_csv(
      "userHisoryPreprocessed.csv",
      index=False
  )

  print(
      "\nUPDATED CSV SAVED"
  )
