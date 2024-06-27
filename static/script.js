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
            <h2>${weatherData.city}, ${weatherData.country}</h2>
            <p>
                <img src="http://openweathermap.org/img/wn/${weatherData.icon}@2x.png" alt="${weatherData.description}">
                ${weatherData.temp}°C, ${weatherData.description}
            </p>
            <p>Date: ${weatherData.date}</p>
            <p>Local Time: ${weatherData.time}</p>
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

        if (data.messages && data.messages.length > 0) {
            const messagesDiv = document.createElement('div');
            messagesDiv.classList.add('messages');
            data.messages.forEach(message => {
                const messageP = document.createElement('p');
                messageP.textContent = message;
                messagesDiv.appendChild(messageP);
            });
            playlistDiv.appendChild(messagesDiv);
        }


        const playlistItemsContainer = document.createElement('div');
        playlistItemsContainer.classList.add('playlist-items-container');
    
        data.playlist.forEach(song => {
            const songDiv = document.createElement('div');
            songDiv.classList.add('playlist-item');
            songDiv.innerHTML = `
                <h3>${song.name} by ${song.artist}</h3>
                <p><em>Reason: ${song.reason}</em></p>
                ${song.preview_url ? `<audio controls src="${song.preview_url}"></audio>` : '<p>(Preview not available)</p>'}
            `;
            playlistItemsContainer.appendChild(songDiv);
        });

    
        playlistDiv.appendChild(playlistItemsContainer);
    })



    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = initMap;