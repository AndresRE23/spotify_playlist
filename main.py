from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

URL = "https://www.billboard.com/charts/billboard-global-200/"
response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
songs = soup.find_all("h3", class_="c-title a-font-basic u-letter-spacing-0010 u-max-width-397 "
                                   "lrv-u-font-size-16 lrv-u-font-size-14@mobile-max u-line-height-22px "
                                   "u-word-spacing-0063 u-line-height-normal@mobile-max a-truncate-ellipsis-2line "
                                   "lrv-u-margin-b-025 lrv-u-margin-b-00@mobile-max")
playlist = []

for i, song in enumerate(songs):
    if i >= 20:
        break
    name = song.get_text(strip=True)
    playlist.append(name)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:8888/callback",
                                               scope="playlist-modify-private"))

user = sp.current_user()
user_id = user["id"]

song_uris = []
for song in playlist:
    result = sp.search(song, type="track", limit=1)
    if result['tracks']['items']:
        song_uris.append(result['tracks']['items'][0]['uri'])
    else:
        print(f"No encontrado en Spotify: {song}")


playlist_name = "Top 20 Billboard"
new_playlist = sp.user_playlist_create(user_id, playlist_name, False)
playlist_id = new_playlist["id"]
sp.playlist_add_items(playlist_id, song_uris)

