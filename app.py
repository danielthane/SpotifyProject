from flask import Flask, flash, redirect, render_template, request, session, url_for
import spotipy
import time
import os
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = 'NOT SCRET KEY'
app.config['SESSION_COOKIE_NAME'] = 'SW50 App'
TOKEN_INFO = "token_info"


@app.route("/")
def landing():
    return render_template("login.html")
    
@app.route("/login")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectBack():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("get_info", _external=True))

@app.route("/get_info")
def get_info():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        redirect(url_for("login", _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_user = get_user(sp)
    songs, popularity_avg = get_songs(sp)
    artists = get_top_artists(sp)
    top_artist = songs[0]
    genres = get_genres(sp)
    genres_list = [i for i in genres]
    top_genre = next(iter(genres))
    return render_template('test.html', 
                           current_user=current_user,
                           songs = songs, 
                           popularity=popularity_avg,
                           artists=artists, 
                           genres=genres,
                           genres_list=genres_list,
                           top_genre=top_genre,
                           top_artist = top_artist)


    

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

scope = "user-library-read user-read-recently-played user-top-read"
def create_spotify_oauth():
    return SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"), 
                        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), 
                        redirect_uri=url_for('redirectBack', _external=True), 
                        scope=scope)


def get_songs(sp):
    items = sp.current_user_top_tracks(limit=6)['items']
    songs = []
    pop_total = 0
    for i in range(len(items)):
        song = {}
        name = items[i]['name']
        img_link = items[i]['album']['images'][2]['url']
        song['title'] = name
        song['image'] = img_link
        if i == 0:
            song['big_image'] = items[i]['album']['images'][0]['url']
        song['artist'] = items[i]['artists'][0]['name']
        songs.append(song)
        pop_total += items[i]['popularity']
    popularity_avg = round(pop_total / len(items)) 
    return songs, popularity_avg

def get_top_artists(sp):
    artists = []
    items = sp.current_user_top_artists(limit=5, time_range="long_term")['items']
    for i in range(len(items)):
        artist = {}
        artist['name'] = items[i]['name']
        artist['image'] = items[i]['images'][2]['url']
        artists.append(artist)
    return artists

def get_genres(sp):
    all_genres = []
    items = sp.current_user_top_artists(limit=50, time_range="short_term")['items']
    for i in range(len(items)):
        for genre in items[i]['genres']:
            all_genres.append(genre)
    genres = {}
    for genre in all_genres:
        if genre not in genres:
            genres[genre] = 1
        elif genre in genres:
            genres[genre] += 1
    sorted_genres = sorted(genres.items(), key=lambda x:x[1], reverse=True)
    sorted_genres = dict(sorted_genres)
    return sorted_genres

def get_user(sp):
    current_user={}
    user = sp.current_user()
    current_user['name'] = user['display_name'].split()[0]
    current_user['image'] = user['images'][0]['url']
    current_user['followers'] = user['followers']['total']
    return current_user

# def get_genres_plot(genres):
#     labels =[]
#     sizes =[]

#     for genre,value in genres.items():
#         if value > 1:
#             labels.append(genre)
#             sizes.append(value)
    
#     plt.pie(sizes, labels=labels)
#     plt.axis('equal')
#     plt.show()




    