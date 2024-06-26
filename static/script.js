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
        generatePlaylist();
    });
}

function generatePlaylist() {
    const mood = document.getElementById('mood').value;
    const weather = document.getElementById('weather').value;

    fetch('/generate_playlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lat, lon, mood, weather }),
    })
    .then(response => response.json())
    .then(data => {
        const playlistDiv = document.getElementById('playlist');
        playlistDiv.innerHTML = '<h2>Your Playlist:</h2>';
        data.forEach(song => {
            playlistDiv.innerHTML += `<p>${song.name} by ${song.artist}</p>`;
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

window.onload = initMap;
