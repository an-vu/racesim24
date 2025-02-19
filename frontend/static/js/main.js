document.addEventListener('DOMContentLoaded', () => {
    const bodyId = document.body.id;

    if (bodyId === 'setup-page') {
        initializeSetupPage();
    } else if (bodyId === 'home-page') {
        initializeHomePage();
    } else if (bodyId === 'end-page') {
        initializeEndPage();
    }
});

// Set Up Page (setup.html)
function initializeSetupPage() {
    console.log("Initializing setup.html");

    // Profile image logic
    const profileImages = ["profile1.png", "profile2.png", "profile3.png", "profile4.png", "profile5.png", "profile6.png", "profile7.png", "profile8.png", "profile9.png", "profile10.png", "profile11.png", "profile12.png"];
    const player1Picture = document.getElementById("player1-picture");
    const player2Picture = document.getElementById("player2-picture");

    let player1Index = Math.floor(Math.random() * profileImages.length);
    let player2Index = Math.floor(Math.random() * profileImages.length);

    if (player1Picture && player2Picture) {
        player1Picture.style.backgroundImage = `url('/static/images/profiles/${profileImages[player1Index]}')`;
        player2Picture.style.backgroundImage = `url('/static/images/profiles/${profileImages[player2Index]}')`;

        player1Picture.addEventListener("click", () => {
            player1Index = (player1Index + 1) % profileImages.length;
            player1Picture.style.backgroundImage = `url('/static/images/profiles/${profileImages[player1Index]}')`;
        });

        player2Picture.addEventListener("click", () => {
            player2Index = (player2Index + 1) % profileImages.length;
            player2Picture.style.backgroundImage = `url('/static/images/profiles/${profileImages[player2Index]}')`;
        });
    }

    // Start race logic
    window.startRace = function () {
        const player1Name = document.getElementById("player1-name").value;
        const player2Name = document.getElementById("player2-name").value;

        if (!player1Name || !player2Name) {
            alert("Please enter names for both Player 1 and Player 2.");
            return;
        }

        localStorage.setItem("player1Name", player1Name);
        localStorage.setItem("player1Picture", profileImages[player1Index]);
        localStorage.setItem("player2Name", player2Name);
        localStorage.setItem("player2Picture", profileImages[player2Index]);

        const data = {
            player1_name: player1Name,
            player2_name: player2Name,
        };

        fetch("/initialize_race", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = "/home";
            } else {
                alert("Error initializing players.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    };
}

// Home Page (home.html)
function initializeHomePage() {
    console.log("Initializing home.html");

    // Initialize elements
    const aboutButton = document.getElementById('about-button');
    const clockButton = document.getElementById('clock-button');
    const tableBody = document.getElementById("standings-table-body");
    
    // Flag to toggle between showing time and date on the clock button
    let showDate = false;

    // Array to store information about player-controlled cars (populated from game data)
    let player_racer_array = [];
    
    // Object to track whether each player's car has entered a pit stop
    let pitStops = {
        player_car_1: false,
        player_car_2: false
    }

    // Clock update function
    function updateClock() {
        const now = new Date();
        clockButton.textContent = showDate 
            ? now.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }).replace(',', '') 
            : now.toLocaleTimeString();
    }

    // Toggle between time and date
    clockButton.addEventListener('click', () => {
        showDate = !showDate;
        updateClock();
    });

    setInterval(updateClock, 1000);

    // About button toggle
    aboutButton.onclick = function () {
        window.location.href = '/about';
    };

    // Initialize car standings
    const carData = Array.from({ length: 16 }, (_, i) => ({
        position: i + 1,
        carNumber: '--',
        driver: '--',
        toLeader: '--',
        totalTime: '--',
        tire: '--',
        fuel: '--'
    }));

    carData.forEach(car => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${car.position}</td>
            <td id="car-${car.position}-num">${car.carNumber}</td>
            <td id="car-${car.position}-driver">${car.driver}</td>
            <td id="car-${car.position}-to-leader">${car.toLeader}</td>
            <td id="car-${car.position}-time-total">${car.totalTime}</td>
            <td id="car-${car.position}-tire">${car.tire}</td>
            <td id="car-${car.position}-fuel">${car.fuel}</td>
        `;
        tableBody.appendChild(row);
    });

    // Race control functions
    async function fetchRaceData() {
        try {
            const response = await fetch('/api/race');
            const data = await response.json();
            updatePlayerCars(data.cars);
            updateMap()
        } catch (error) {
            console.error('Error starting race:', error);
        }
    }

    async function getRaceData() {
        try {
            const response = await fetch('/api/race');
            const data = await response.json();
            
            if(data.lap == (data.lap_count+1)){
                endRace();
            } else {
                updateRaceStandings(data);
                updatePlayerCars(data.cars);
                updatePlayerControlCenters();
            }

            } catch (error) {
            console.error('Error fetching race data:', error);
        }
    }

    async function advanceLap() {
        try {
            await fetch('/api/race/lap', { method: 'POST' });
            getRaceData();
            updateMap();
            pitStops['player_car_1'] = false;
            pitStops['player_car_2'] = false;
        } catch (error) {
            console.error('Error advancing lap:', error);
        }
    }

    async function resetRace() {
        try {
            await fetch('/api/race/reset', { method: 'POST' });
            window.location.href = "/";
        } catch (error) {
            console.error('Error resetting race:', error);
        }
    }

    function handlePitStop(carIndex, carNumber) {
        const carKey = carIndex === 0 ? 'player_car_1' : 'player_car_2';
        // Check if the car is already set to pit
        if (pitStops[carKey]) {
            alert(`${carKey === 'player_car_1' ? 'Player Car 1' : 'Player Car 2'} is already set to pit after this lap.`);
            return;  // If true, exit early
        }
        // Mark the car as in the pit stop
        pitStops[carKey] = true;

        fetch('/api/race/pit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number: carNumber })
        })
        .catch(error => console.error(`Error performing pit stop for Car #${carNumber}:`, error));
    }

    function handleStrategyChange(carNumber, strategyLevel) {
        fetch('/api/race/strategy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number: carNumber, push_level: strategyLevel })
        })
        .then(getRaceData)
        .catch(error => console.error(`Error updating strategy for Car #${carIndex + 1}:`, error));
    }

    function updatePlayerCars(cars) {
        player_racer_array = cars.filter(car => car.ai_or_player !== 3);
        car1 = player_racer_array.find(car => car.number === 2);
        car2 = player_racer_array.find(car => car.number === 3);

        if (car1) {
            document.getElementById('car-1-title').textContent = `#${car1.number} ${car1.name}`;
        }
        if (car2) {
            document.getElementById('car-2-title').textContent = `#${car2.number} ${car2.name}`;
        }
    }

    function updateRaceStandings(data) {
        document.getElementById('standings-title').textContent = `Standings - Lap: ${data.lap} of ${data.lap_count}`;
        data.cars.forEach((car, index) => {
            if (car) {
                document.getElementById(`car-${index + 1}-num`).textContent = car.number;
                document.getElementById(`car-${index + 1}-driver`).textContent = car.name;
                document.getElementById(`car-${index + 1}-to-leader`).textContent = car.to_leader.toFixed(2);
                document.getElementById(`car-${index + 1}-time-total`).textContent = car.total_race_time.toFixed(2);
                document.getElementById(`car-${index + 1}-tire`).textContent = `${car.tire_life.toFixed(2)}%`;
                document.getElementById(`car-${index + 1}-fuel`).textContent = `${car.fuel_level.toFixed(2)}%`;
            }
        });
    }

    function updatePlayerControlCenters() {
        car1 = player_racer_array.find(car => car.number === 2);
        car2 = player_racer_array.find(car => car.number === 3);
    
        if (car1) {
            document.getElementById('player-car-1-current-strategy').textContent = `Strategy Level: ${car1.push_tire}`;
            document.getElementById('player-car-1-tire').textContent = `Tire %: ${car1.tire_life.toFixed(2)}%`;
            document.getElementById('player-car-1-fuel').textContent = `Fuel %: ${car1.fuel_level.toFixed(2)}%`;
        }
        if (car2) {
            document.getElementById('player-car-2-current-strategy').textContent = `Strategy Level: ${car2.push_tire}`;
            document.getElementById('player-car-2-tire').textContent = `Tire %: ${car2.tire_life.toFixed(2)}%`;
            document.getElementById('player-car-2-fuel').textContent = `Fuel %: ${car2.fuel_level.toFixed(2)}%`;
        }
    }

    function updateMap() {
        // Fetch the race map data from the Flask API
        fetch('/api/map')
            .then(response => response.json()) // Parse JSON response
            .then(data => {
                // Sort the cars based on their placement
                const sortedCars = Object.entries(data)
                    .sort((a, b) => a[1].place - b[1].place); // Sort by carData["place"]
    
                // Get track dimensions and calculate the oval radii
                const track = document.querySelector(".track");
                const trackWidth = track.offsetWidth;
                const trackHeight = track.offsetHeight;
    
                const centerX = trackWidth / 2;
                const centerY = trackHeight / 2;
                const radiusX = trackWidth / 2.2; // Adjust for horizontal radius
                const radiusY = trackHeight / 2.5; // Adjust for vertical radius
                
                // Use only 75% of the track
                const startAngle = 1.5; // Starting angle (0 degrees)
                const endAngle = 2 * Math.PI; // Ending angle (270 degrees)

                carCount = sortedCars.length

                // Update each car div based on its sorted position
                sortedCars.forEach(([carNumber, carData], index) => {
                    const carDiv = document.getElementById((index + 1).toString()); // Get the div by its rank ID
                    if (carDiv) {
                        // Calculate position on the oval based on index
                        const angle = startAngle + (index / carCount) * (endAngle - startAngle);

                        const x = centerX + radiusX * Math.cos(angle) - carDiv.offsetWidth / 2;
                        const y = centerY + radiusY * Math.sin(angle) - carDiv.offsetHeight / 2;
    
                        // Set position and update text
                        carDiv.style.left = `${x}px`;
                        carDiv.style.top = `${y}px`;
                        carDiv.textContent = carNumber; // Display car number
    
                        // Update color based on the place
                        if (carData.place === 1) {
                            carDiv.style.backgroundColor = 'gold'; // First place
                        } else if (carData.place === 2) {
                            carDiv.style.backgroundColor = 'silver'; // Second place
                        } else if (carData.place === 3) {
                            carDiv.style.backgroundColor = 'red'; // Third place
                        } else {
                            carDiv.style.backgroundColor = 'blue'; // Others
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching race map data:', error));
    }

    async function endRace() {
        try{
            await fetch('/end', {method: 'POST'});
            window.location.href = "/end";
        } catch (error) {
            console.error('Error ending the race', error);
        }
    }

    // Event Listeners for Pit and Strategy Buttons
    document.getElementById('player-car-1-pit').addEventListener('click', () => handlePitStop(0, 2));
    document.getElementById('player-car-2-pit').addEventListener('click', () => handlePitStop(1, 3));
    document.querySelectorAll('input[name="strategy1"]').forEach(radio => 
        radio.addEventListener('change', () => handleStrategyChange(2, radio.value)));
    document.querySelectorAll('input[name="strategy2"]').forEach(radio => 
        radio.addEventListener('change', () => handleStrategyChange(3, radio.value)));

    // Lap Button & Reset Button
    document.getElementById('lap-button').addEventListener('click', advanceLap);
    document.getElementById('reset-button').addEventListener('click', resetRace);

    // Load player data from localStorage
    const player1Data = { name: localStorage.getItem("player1Name") || "Player 1", car: 2 || "00", pic: localStorage.getItem("player1Picture") || "profile1.png" };
    const player2Data = { name: localStorage.getItem("player2Name") || "Player 2", car: 3 || "00", pic: localStorage.getItem("player2Picture") || "profile2.png" };

    document.getElementById("car-1-title").textContent = `${player1Data.name} - Car #2`;
    document.getElementById("car-2-title").textContent = `${player2Data.name} - Car #3`;
    document.getElementById("player1-profile").style.backgroundImage = `url('/static/images/profiles/${player1Data.pic}')`;
    document.getElementById("player2-profile").style.backgroundImage = `url('/static/images/profiles/${player2Data.pic}')`;

    // Start and fetch initial race data
    fetchRaceData();
    getRaceData();

    let resizeTimeout;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            updateMap(); // Call updateMap after resizing is complete
        }, 100); // Adjust debounce delay as needed
    });

    // Go to Github button
    document.getElementById('git-button').addEventListener('click', function () {
        window.open('https://github.com/an-vu/racesim24', '_blank');
    });
}

// End Page (end.html)
function initializeEndPage() {
    console.log("Initializing End Page...");

    // Initialize car standings
    const tableBody = document.getElementById("end-standings-table-body");
    const carData = Array.from({ length: 16 }, (_, i) => ({
        position: i + 1,
        carNumber: '--',
        driver: '--',
        toLeader: '--',
        totalTime: '--',
    }));

    carData.forEach(car => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${car.position}</td>
            <td id="car-${car.position}-num">${car.carNumber}</td>
            <td id="car-${car.position}-driver">${car.driver}</td>
            <td id="car-${car.position}-to-leader">${car.toLeader}</td>
            <td id="car-${car.position}-time-total">${car.totalTime}</td>
        `;
        tableBody.appendChild(row);
    });

    // Reset race button logic
    document.getElementById('reset-button-2').addEventListener('click', async () => {
        try {
            await fetch('/api/race/reset', { method: 'POST' });
            window.location.href = "/";
        } catch (error) {
            console.error('Error resetting race:', error);
        }
    });

    // Fetch and update race data
    async function getRaceData() {
        try {
            const response = await fetch('/api/race');
            const data = await response.json();
            updateRaceStandings(data);
            updateWinnerName(data);
        } catch (error) {
            console.error('Error fetching race data:', error);
        }
    }

    function updateRaceStandings(data) {
        data.cars.forEach((car, index) => {
            if (car) {
                document.getElementById(`car-${index + 1}-num`).textContent = car.number;
                document.getElementById(`car-${index + 1}-driver`).textContent = car.name;
                document.getElementById(`car-${index + 1}-to-leader`).textContent = car.to_leader.toFixed(2);
                document.getElementById(`car-${index + 1}-time-total`).textContent = car.total_race_time.toFixed(2);
            }
        });
    }

    function updateWinnerName(data) {
        const winnerElement = document.getElementById('winner');
        data.cars.forEach(car => {
            if (car.to_leader === 0) {
                if ([2, 3].includes(car.number)) {
                    winnerElement.textContent = `Winner: ${car.name}, good job!`;
                } else {
                    winnerElement.textContent = `Winner: ${car.name}, better luck next time!`;
                }
            }
        });
    }

    // Initial call to fetch and display data
    getRaceData();
}
