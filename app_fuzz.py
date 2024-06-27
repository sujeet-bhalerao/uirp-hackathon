from flask import Flask, render_template, request, jsonify
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import random
from datetime import datetime
import pytz
from spotipy.exceptions import SpotifyException
import unidecode
import urllib.parse
import json
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from openai import OpenAI

open_ai_api_key = os.environ["OPENAI_API_KEY"]
spotify_client_id = os.environ["SPOTIFY_CLIENT_ID"]
spotify_client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

all_genres = [
    "acoustic",
    "afrobeat",
    "alt-rock",
    "alternative",
    "ambient",
    "anime",
    "black-metal",
    "bluegrass",
    "blues",
    "bossanova",
    "brazil",
    "breakbeat",
    "british",
    "cantopop",
    "chicago-house",
    "children",
    "chill",
    "classical",
    "club",
    "comedy",
    "country",
    "dance",
    "dancehall",
    "death-metal",
    "deep-house",
    "detroit-techno",
    "disco",
    "disney",
    "drum-and-bass",
    "dub",
    "dubstep",
    "edm",
    "electro",
    "electronic",
    "emo",
    "folk",
    "forro",
    "french",
    "funk",
    "garage",
    "german",
    "gospel",
    "goth",
    "grindcore",
    "groove",
    "grunge",
    "guitar",
    "happy",
    "hard-rock",
    "hardcore",
    "hardstyle",
    "heavy-metal",
    "hip-hop",
    "holidays",
    "honky-tonk",
    "house",
    "idm",
    "indian",
    "indie",
    "indie-pop",
    "industrial",
    "iranian",
    "j-dance",
    "j-idol",
    "j-pop",
    "j-rock",
    "jazz",
    "k-pop",
    "kids",
    "latin",
    "latino",
    "malay",
    "mandopop",
    "metal",
    "metal-misc",
    "metalcore",
    "minimal-techno",
    "movies",
    "mpb",
    "new-age",
    "new-release",
    "opera",
    "pagode",
    "party",
    "philippines-opm",
    "piano",
    "pop",
    "pop-film",
    "post-dubstep",
    "power-pop",
    "progressive-house",
    "psych-rock",
    "punk",
    "punk-rock",
    "r-n-b",
    "rainy-day",
    "reggae",
    "reggaeton",
    "road-trip",
    "rock",
    "rock-n-roll",
    "rockabilly",
    "romance",
    "sad",
    "salsa",
    "samba",
    "sertanejo",
    "show-tunes",
    "singer-songwriter",
    "ska",
    "sleep",
    "songwriter",
    "soul",
    "soundtracks",
    "spanish",
    "study",
    "summer",
    "swedish",
    "synth-pop",
    "tango",
    "techno",
    "trance",
    "trip-hop",
    "turkish",
    "work-out",
    "world-music"
  ]

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    lat = request.json['lat']
    lon = request.json['lon']
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    response = requests.get(url)
    data = response.json()
    
    weather_code = data['current_weather']['weathercode']
    weather_descriptions = {
        0: {"description": "Clear sky", "icon": "01d"},
        1: {"description": "Mainly clear", "icon": "01d"}, 
        2: {"description": "Partly cloudy", "icon": "02d"}, 
        3: {"description": "Overcast", "icon": "04d"},
        45: {"description": "Fog", "icon": "50d"}, 
        48: {"description": "Depositing rime fog", "icon": "50d"},
        51: {"description": "Light drizzle", "icon": "09d"}, 
        53: {"description": "Moderate drizzle", "icon": "09d"}, 
        55: {"description": "Dense drizzle", "icon": "09d"},
        61: {"description": "Slight rain", "icon": "10d"}, 
        63: {"description": "Moderate rain", "icon": "10d"}, 
        65: {"description": "Heavy rain", "icon": "10d"},
        71: {"description": "Slight snow fall", "icon": "13d"}, 
        73: {"description": "Moderate snow fall", "icon": "13d"}, 
        75: {"description": "Heavy snow fall", "icon": "13d"},
        95: {"description": "Thunderstorm", "icon": "11d"}, 
        96: {"description": "Thunderstorm with slight hail", "icon": "11d"}, 
        99: {"description": "Thunderstorm with heavy hail", "icon": "11d"}
    }
    weather_info = weather_descriptions.get(weather_code, {"description": "Unknown", "icon": "50d"})

    location_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
    location_data = requests.get(location_url).json()
    
    city = location_data.get('city') or location_data.get('locality')
    country = location_data.get('countryName')
    
    if not city or not country or city.strip() == ',' or not city.strip():
        city = 'Middle of Nowhere'
        country = 'Unknown Waters'
    
    timezone_str = data['timezone']
    if timezone_str.startswith('Etc/'):
        offset = int(timezone_str.split('GMT')[-1])
        timezone_str = f"GMT{'+' if offset <= 0 else '-'}{abs(offset):02d}:00"
    
    try:
        timezone = pytz.timezone(timezone_str)
        current_datetime = datetime.now(timezone)
        current_date = current_datetime.strftime("%B %d, %Y")  # Format: Month Day, Year
        current_time = current_datetime.strftime("%I:%M %p")  # Format: Hour:Minute AM/PM
    except pytz.exceptions.UnknownTimeZoneError:
        timezone = pytz.UTC
        current_datetime = datetime.now(timezone)
        current_date = current_datetime.strftime("%B %d, %Y")
        current_time = current_datetime.strftime("%I:%M %p") + " UTC"

    return jsonify({
        'description': weather_info['description'],
        'icon': weather_info['icon'],
        'temp': data['current_weather']['temperature'],
        'city': city,
        'country': country,
        'date': current_date,
        'time': current_time,
        'timezone': timezone_str
    })


def get_query_bands_in(location_uri):
    return f"""
    SELECT DISTINCT ?Band ?Name WHERE {{
      {{
        ?Band foaf:name ?Name .
        ?Band a schema:MusicGroup .
        {{
          ?Band dbo:hometown <{location_uri}> .
        }} UNION {{
          ?Band dbo:birthPlace <{location_uri}> .
        }} UNION {{
          ?Band dbo:origin <{location_uri}> .
        }}
      }}
      UNION
      {{
        ?Band foaf:name ?Name .
        ?Band a schema:MusicGroup .
        {{
          ?Band dbo:hometown ?place .
        }} UNION {{
          ?Band dbo:birthPlace ?place .
        }} UNION {{
          ?Band dbo:origin ?place .
        }}
        ?place dbo:isPartOf* <{location_uri}> .
      }}
    }}
    LIMIT 100
    """

import re

def clean_location_name(name):
    name = re.sub(r'\b(the|a|an)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\([^)]*\)', '', name)
    name = name.strip().replace(' ', '_')
    return name

def get_bands_from_location(location):
    print(f"Querying DBpedia for bands from {location}")
    cleaned_location = clean_location_name(location)
    encoded_location = urllib.parse.quote(cleaned_location)
    location_uri = f"http://dbpedia.org/resource/{encoded_location}"
    band_query = get_query_bands_in(location_uri)
    
    url = f"https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query={urllib.parse.quote(band_query)}&format=application%2Fsparql-results%2Bjson"
    
    resp = requests.get(url)
    data = resp.json()
    
    artists = []
    for binding in data['results']['bindings']:
        if not binding['Band']['value'].startswith("http://dbpedia.org/resource/List_of_"):
            artists.append({
                'name': binding['Name']['value'],
                'id': binding['Band']['value']
            })
    
    # Remove duplicates
    artists = list({v['id']:v for v in artists}.values())
    
    print(f"Found {len(artists)} artists from DBpedia for {location}")
    for artist in artists[:10]:  # Print first 10 artists
        print(f"  - {artist['name']}")
    
    return artists



@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id,
                                                           client_secret=spotify_client_secret))
    print("Received request for playlist generation")
    lat = request.json['lat']
    lon = request.json['lon']
    weather = request.json['weather']
    date = request.json['date']
    reco_type = request.json['recoType']
    music_preference = request.json.get('musicPreference', '')
    print(f"Lat: {lat}, Lon: {lon}, Weather: {weather}, Date: {date}, Reco Type: {reco_type}")

    location_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
    location_data = requests.get(location_url).json()

    city = location_data.get('city', 'Unknown City')
    country = location_data.get('countryName', 'Unknown Country')

    try:
        playlist = []
        messages = []

        if reco_type == 'location':
            # Location-based recommendation code
            city_artists = get_bands_from_location(city)

            all_tracks = []
            for artist in city_artists:
                try:
                    results = sp.search(q=f"artist:{artist['name']}", type='track', limit=5)
                    for track in results['tracks']['items']:
                        if track['preview_url']:
                            all_tracks.append({
                                'name': track['name'],
                                'artist': track['artists'][0]['name'],
                                'preview_url': track['preview_url'],
                                'popularity': track['popularity'],
                                'reason': f"Artist from {city}"
                            })
                except Exception as e:
                    print(f"Error searching for {artist['name']}: {str(e)}")

            if len(all_tracks) < 10:
                print(f"Added {len(all_tracks)} tracks from {city}. Trying artists from {country}.")
                country_artists = get_bands_from_location(country)
    
                for artist in country_artists:
                    try:
                        results = sp.search(q=f"artist:{artist['name']}", type='track', limit=5)
                        for track in results['tracks']['items']:
                            if track['preview_url']:
                                all_tracks.append({
                                    'name': track['name'],
                                    'artist': track['artists'][0]['name'],
                                    'preview_url': track['preview_url'],
                                    'popularity': track['popularity'],
                                    'reason': f"Artist from {country}"
                                })
                    except Exception as e:
                        print(f"Error searching for {artist['name']}: {str(e)}")


            # Sort all tracks by popularity in descending order
            all_tracks.sort(key=lambda x: x['popularity'], reverse=True)

            # Take the top 15 tracks or all if less than 15
            playlist = all_tracks[:15]
            print(playlist)
            if len(playlist) < 10:
                print(f"Added {len(playlist)} tracks from {city}. Trying artists from {country}.")
                country_artists = get_bands_from_location(country)
                
                for artist in country_artists[:20]:
                    if len(playlist) >= 15:
                        break
                    try:
                        results = sp.search(q=f"artist:{artist['name']}", type='track', limit=1)
                        if results['tracks']['items']:
                            track = results['tracks']['items'][0]
                            if track['preview_url']:
                                playlist.append({
                                    'name': track['name'],
                                    'artist': track['artists'][0]['name'],
                                    'preview_url': track['preview_url'],
                                    'reason': f"Artist from {country}"
                                })
                    except Exception as e:
                        print(f"Error searching for {artist['name']}: {str(e)}")
        
        else:  # todo: GPT-based recommendations
            conditions = weather
            location_gpt = city + ", " + country
            

            def get_genres(location_gpt, weather, date, user_input):
                client = OpenAI(api_key=open_ai_api_key)

                completion_genres = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an engine that takes in a specific location (City, Country), weather data, date and return only a comma separated list of three music genres to match the vibe of that particular (City, Country), weather conditions, and date to be used in as keywords for Spotify search."},
                    {"role": "user", "content": f"Location: {location_gpt}; Weather: {weather}, {conditions}; Date: {date}"}
                ]
                )
                
                recommendations_targets = {'target_acousticness': 0.5, 'target_danceability': 0.6, 'target_energy': 0.7, 'target_liveness': 0.5, 'target_loudness': 0.6, 'target_popularity': 0.85}
                if user_input != '':
                    completion_feeling = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an engine that generates values on a scale of 0-1 for the following variables based on the user feeling input. The output should only be like a JSON where the variable is the key and the value is the score from 0-1. Variables: target_acousticness, target_danceability,  target_energy, target_liveness, target_loudness, target_popularity"},
                        {"role": "user", "content": user_input}
                    ]
                    )
                    try:
                        recommendations_targets = json.loads(completion_feeling.choices[0].message.content)
                    except:
                        recommendations_targets = {'target_acousticness': 0.5, 'target_danceability': 0.6, 'target_energy': 0.7, 'target_liveness': 0.5, 'target_loudness': 0.6, 'target_popularity': 0.8}

                try:
                    genres = completion_genres.choices[0].message.content.lower().split(", ")
                except:
                    genres = ["pop", "rock", "country"]
                return genres, recommendations_targets

            ######## Spotify API ########
            def get_tracks(genres, recommendations_targets, conditions):
                acceptable_genres = [cur_genre for cur_genre in genres if cur_genre in all_genres]
                if len(acceptable_genres) == 0:
                    acceptable_genres = ["pop", "rock", "country"]
                track_list = []
                # Search for tracks with the keyword 'summer' to get their ids

                results = sp.search(q=f'{conditions}', type='playlist', limit=10)

                num_results = len(results['playlists']['items'])
                random_playlist_idx = random.randint(0, num_results - 1)
                playlist_id = results['playlists']['items'][random_playlist_idx]['id']
                results = sp.playlist_tracks(playlist_id, limit=100)
                track_list = results['items']

                track_ids = [track['track']['id'] for track in track_list]

                if len(track_ids) < 4:
                    random_tracks = track_ids
                else:
                    random_tracks = random.sample(track_ids, 3)

                genre_arg = random.choice(acceptable_genres)

                # If no tracks were found with the keyword 'summer', print a message
                if not track_ids:
                    print("No tracks found with the keyword 'summer'.")
                else:
                    # Get recommendations based on the track IDs
                    print("Getting recommendations...")
                    recommendations = sp.recommendations(seed_tracks=[random_tracks[0]], limit=50, seed_genres=[genre_arg], kwargs=recommendations_targets)
                    final_tracks = []
                    for track in recommendations['tracks']:
                        if track['preview_url']:
                            final_tracks.append({
                                'name': track['name'],
                                'artist': track['artists'][0]['name'],
                                'preview_url': track['preview_url']
                            })
                    print("Recommendations received!")
                    return final_tracks
            
            genres, recommendations_targets = get_genres(location_gpt, weather, date, music_preference)
            playlist = get_tracks(genres, recommendations_targets, conditions)
                

        # If we still don't have enough tracks, fill with global top tracks
        if len(playlist) < 15:
            print(f"Not enough tracks ({len(playlist)}). Filling with popular tracks.")
            messages.append(f"Added {len(playlist)} tracks from {city if reco_type == 'location' else 'GPT recommendations'}. Filling the rest with popular tracks.")
            global_tracks = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=50)['items']
            for item in global_tracks:
                if len(playlist) >= 15:
                    break
                track = item['track']
                if track['preview_url']:
                    playlist.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'preview_url': track['preview_url'],
                        'reason': "Popular track"
                    })
        
        random.shuffle(playlist)
        
        print(f"Generated playlist with {len(playlist)} tracks")
        return jsonify({
            'playlist': playlist,
            'weather': weather,
            'city': city,
            'country': country,
            'messages': messages
        })
    except Exception as e:
        print(f"Unexpected error in generate_playlist: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500


if __name__ == '__main__':
    app.run(debug=True)