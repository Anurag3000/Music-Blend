
def load_streaming_history(json_file):
  import pandas as pd
  import numpy as np

  df = pd.read_json(json_file)


  # =========================================
  # CREATE YYYY-MM COLUMN
  # =========================================

  # Convert endTime to datetime
  df["endTime"] = pd.to_datetime(df["endTime"])

  # Extract only year-month
  df["year_month"] = df["endTime"].dt.strftime("%Y-%m")
  return df

def create_monthly_summary(json_file):
  df=load_streaming_history(json_file)
  summary = (
    df.groupby(
        ["year_month", "artistName", "trackName"]
    )
    .agg(
        playCount=("trackName", "count"),
        totalMsPlayed=("msPlayed", "sum")
    )
    .reset_index()
  )

  summary.to_csv(
    "spotify_summary.csv",
    index=False
  )
  return summary
