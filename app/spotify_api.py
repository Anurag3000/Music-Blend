
import pandas as pd
import time
import base64
import requests

# =========================
# GET ACCESS TOKEN
# =========================

def get_token(CLIENT_ID, CLIENT_SECRET):

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"

    auth_base64 = base64.b64encode(
        auth_string.encode()
    ).decode()

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = requests.post(
        url,
        headers=headers,
        data=data
    )


    # result = requests.post(
    # url,
    # headers=headers,
    # data=data
    # )

    print("Status Code:", result.status_code)
    print("Response:", result.text)

    token = result.json()["access_token"]

    return token


def get_track_and_artist_id(song, artist, token):

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query = f"track:{song} artist:{artist}"

    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    # ERROR CHECK
    if response.status_code != 200:
        print("ERROR:", response.status_code)
        return None

    data = response.json()

    items = data["tracks"]["items"]

    # NO RESULTS
    if len(items) == 0:
        return None

    track = items[0]

    # TRACK ID
    track_id = track["id"]

    # TRACK NAME
    track_name = track["name"]

    # ARTIST INFO
    artist_info = track["artists"][0]

    artist_id = artist_info["id"]
    artist_name = artist_info["name"]

    return {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "song_id": track_id,
        "song_name": track_name
    }


def get_audio_features(track_id, headers):

    if pd.isna(track_id):
        return {}

    url = (
        "https://spotify-extended-audio-features-api.p.rapidapi.com"
        f"/v1/audio-features/{track_id}"
    )

    try:

        response = requests.get(
            url,
            headers=headers
        )

        time.sleep(1)

        if response.status_code == 200:

            data = response.json()

            return {

                'danceability': data.get('danceability'),

                'energy': data.get('energy'),

                'valence': data.get('valence'),

                'tempo': data.get('tempo'),

                'acousticness': data.get('acousticness'),

                'instrumentalness': data.get('instrumentalness'),

                'liveness': data.get('liveness'),

                'speechiness': data.get('speechiness')

            }

        else:

            print(
                f"AUDIO API ERROR for {track_id}: "
                f"{response.status_code}"
            )

            return {}

    except Exception as e:

        print(
            f"AUDIO REQUEST FAILED for "
            f"{track_id}: {e}"
        )

        return {}



# ==========================================
# GET ARTIST GENRES
# ==========================================

def get_artist_genres(artist_id, headers):

    if pd.isna(artist_id):
        return None

    url = (
        "https://spotify-extended-audio-features-api.p.rapidapi.com"
        f"/v1/artists/{artist_id}"
    )

    try:

        response = requests.get(
            url,
            headers=headers
        )

        time.sleep(1)

        if response.status_code == 200:

            data = response.json()

            genres = data.get("genres", [])

            # convert list → string
            genre_string = ", ".join(genres)

            return genre_string

        else:

            print(
                f"ARTIST API ERROR for "
                f"{artist_id}: {response.status_code}"
            )

            return None

    except Exception as e:

        print(
            f"ARTIST REQUEST FAILED for "
            f"{artist_id}: {e}"
        )

        return None
