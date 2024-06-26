from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


moods = ['Happy', 'Sad', 'Energetic', 'Relaxed']
weathers = ['Sunny', 'Rainy', 'Cloudy', 'Snowy']
genres = ['Pop', 'Rock', 'Hip-Hop', 'Classical', 'Electronic']

@app.route('/')
def index():
    return render_template('index.html', moods=moods, weathers=weathers)

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    lat = request.json['lat']
    lon = request.json['lon']
    mood = request.json['mood']
    weather = request.json['weather']
    
    
    playlist = [
        {'name': f"Song for {mood} mood", 'artist': 'Artist1'},
        {'name': f"Track for {weather} weather", 'artist': 'Artist2'},
        {'name': f"Tune for location ({lat:.2f}, {lon:.2f})", 'artist': 'Artist3'},
    ]
    
    for _ in range(7):  
        playlist.append({
            'name': f"Random {random.choice(genres)} Song",
            'artist': f"Random Artist {random.randint(1, 100)}"
        })
    
    return jsonify(playlist)

if __name__ == '__main__':
    app.run(debug=True)
