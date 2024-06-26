This project develops a customized Spotify Recommender system that leverages user location, current weather conditions, and the user's emotional state to recommend songs tailored to the user's environment and mood.


Overview:

The system utilizes data from various APIs to provide a personalized song recommendation experience:

    Weather Data: Retrieved from the OpenWeather API (https://openweathermap.org/api) to obtain the current weather conditions based on the user's location.
  
    Spotify Data: Utilizes the Spotify API (https://developer.spotify.com/documentation/web-api) to fetch music recommendations and information about songs.
  
    Location Services: Integrates Google API (https://developers.google.com/maps/documentation/javascript) for geolocation services to pinpoint the user's location accurately.


Functionality:

  Upon user input regarding their location and mood, the system:

    Fetches Weather Information: Retrieves real-time weather data using the OpenWeather API based on the user-provided location.
  
    Determines User Mood: Allows the user to input their current emotional state or mood.
  
    Generates Song Recommendations: Combines weather data, mood input, and Spotify's music recommendation capabilities to suggest songs that match the user's context.
  
    User Interface: Provides a user-friendly interface where users can input their location and mood, and receive personalized song recommendations along with detailed weather information.
