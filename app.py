from flask import Flask, flash, redirect, render_template, request, session, url_for
import spotipy
import time
import os
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


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
    songs, popularity_avg = get_songs(sp)
    artists = get_top_artists(sp)
    return render_template('test.html', songs = songs, popularity=popularity_avg, artists=artists)


    

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

scope = "user-library-read user-read-recently-played"
def create_spotify_oauth():
    return SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"), 
                        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), 
                        redirect_uri=url_for('redirectBack', _external=True), 
                        scope=scope)


def get_songs(sp):
    items = sp.current_user_recently_played(limit=10)['items']
    songs = []
    pop_total = 0
    for i in range(len(items)):
        song = {}
        name = items[i]['track']['name']
        img_link = (items[i]['track']['album']['images'][2]['url'])
        song['title'] = name
        song['image'] = img_link
        songs.append(song)
        pop_total += items[i]['track']['popularity']
    popularity_avg = round(pop_total / len(items)) 
    return songs, popularity_avg

def get_top_artists(sp):
    artists = []
    items = sp.current_user_top_artists(limit=10, time_range="long_term")['items']
    for i in range(len(items)):
        artist = {}
        artist['name'] = items[i]['name']
        artist['image'] = items[i]['images'][2]['url']
        artists.append(artist)
    return artists





    