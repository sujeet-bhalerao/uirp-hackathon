let map;
let marker;
let lat = 0;
let lon = 0;

function initMap() {
    map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    map.on('click', function(e) {
        lat = e.latlng.lat;
        lon = e.latlng.lng;
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker([lat, lon]).addTo(map);
        getWeatherAndPlaylist();
    });
}

function getWeatherAndPlaylist() {
    // Get weather
    fetch('/get_weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lat, lon }),
    })
    .then(response => response.json())
    .then(weatherData => {
        document.getElementById('weather').innerHTML = `
            <div class="weather-info">
                <h2>${weatherData.city}, ${weatherData.country}</h2>
                <p>
                    <img src="http://openweathermap.org/img/wn/${weatherData.icon}@2x.png"
                         alt="${weatherData.description}">
                    ${weatherData.temp}°C, ${weatherData.description}
                </p>
            </div>
            <div class="weather-time">
                <p>Date: ${weatherData.date}</p>
                <p>Local Time: ${weatherData.time}</p>
            </div>
        `;
        return weatherData;
    })


    .then(weatherData => {
        const recoType = document.querySelector('input[name="recoType"]:checked').value;
        const musicPreference = document.getElementById('musicPreference').value;
        return fetch('/generate_playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                lat, 
                lon, 
                weather: weatherData.description,
                date: weatherData.date,
                recoType: recoType,
                musicPreference: musicPreference
            }),
        });
    })
    .then(response => response.json())
    .then(data => {
        const playlistDiv = document.getElementById('playlist');
        playlistDiv.classList.add('centered-content');
        playlistDiv.innerHTML = `
            <h2>Your Playlist for ${data.city}, ${data.country} (${data.weather}):</h2>
        `;

        // Display messages if any
        if (data.messages && data.messages.length > 0) {
            playlistDiv.innerHTML += '<div class="messages">';
            data.messages.forEach(message => {
                playlistDiv.innerHTML += `<p>${message}</p>`;
            });
            playlistDiv.innerHTML += '</div>';
        }

        data.playlist.forEach(song => {
            playlistDiv.innerHTML += `
                <div class="playlist-item">
                    <h3>${song.name} by ${song.artist}</h3>
                    ${song.preview_url ? `<audio controls src="${song.preview_url}"></audio>` : '<p>(Preview not available)</p>'}
                </div>
            `;
        });
    })


    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = initMap;