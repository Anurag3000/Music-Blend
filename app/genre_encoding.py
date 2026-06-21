

def create_genre_list(dtf3):
  dtf3.dropna(inplace=True)
  dtf3['genre_list'] = dtf3.head(40)['genres'].apply(lambda x: x.split(', '))

  all_unique_genres = dtf3['genre_list'].dropna().explode().unique()
  return all_unique_genres

def one_hot_encode_genres(dtf3):
  all_unique_genres=create_genre_list(dtf3)
  for genre_name in all_unique_genres:
      print(f"Processing genre: {genre_name}")
      dtf3[genre_name] = dtf3['genre_list'].apply(lambda x: 1 if isinstance(x, list) and genre_name in x else 0)
  return dtf3
