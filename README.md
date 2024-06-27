
# Wandertunes
Welcome to the Wandertunes, a location and vibes-based music playlist generator! This project is designed to create a music playlist based on your current location, mood and weather conditions. It uses data from various APIs to provide a personalized music experience.

### Data Integration
The project seamlessly integrates data from multiple sources:

- **Weather Data**: Uses [Open-Meteo API](https://open-meteo.com/en/docs) to fetch current weather conditions.
- **Location Data**: Uses [BigDataCloud API](https://www.bigdatacloud.com/free-api/free-reverse-geocode-to-city-api) for reverse geocoding to get city and country information.
- **Music Data**: Uses [Spotify's API](https://developer.spotify.com/documentation/web-api) for finding and recommending tracks and creating playlists.
- **GPT-3 Integration**: Uses [OpenAI's GPT-3](https://platform.openai.com/docs/api-reference) to provide genre recommendations based on weather, date, and user input.


### Features
- Location-Based Recommendations: Finds artists from your chosen city/country and suggests their popular tracks.
- Vibes-Based GPT-3 Enhanced Recommendations: Generates playlists based on current weather conditions. Uses GPT-3 to recommend genres based on weather, date, and user input.
- Popular Tracks Fallback: Fills the playlist with popular tracks if enough recommendations are not found.

### Installation
1. Clone the repository:

```
git clone https://github.com/sujeet-bhalerao/uirp-hackathon.git
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Set up environment variables for API keys:

```
export SPOTIFY_CLIENT_ID='your-spotify-client-id'
export SPOTIFY_CLIENT_SECRET='your-spotify-client-secret'
export OPENAI_API_KEY='your-openai-api-key'
```

4. Run the Flask app:
```
python app_fuzz.py

```

### Usage
- Landing Page: Navigate to the root URL to access the landing page.
- Main Page: Select a location on the map and scroll down to see the selected location, the weather, and the recommended playlist. The user can choose between location based playlists or vibes based playlists, and can optionally add input in a text box to further refine results.

