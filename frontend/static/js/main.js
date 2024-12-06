document.addEventListener('DOMContentLoaded', () => {
    // Initialize elements
    const aboutButton = document.getElementById('about-button');
    const clockButton = document.getElementById('clock-button');
    const tableBody = document.getElementById("standings-table-body");
    
    let showDate = false;
    let player_racer_array = [];
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

    // About button toggle
    aboutButton.onclick = function () {
        window.location.href = '/about';
    };

    setInterval(updateClock, 1000);

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
    async function startRace() {
        try {
            const response = await fetch('/api/race');
            const data = await response.json();
            updatePlayerCars(data.cars);
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
            .then(response => response.json())  // Parse JSON response
            .then(data => {
                // Sort the cars based on their placement
                const sortedCars = Object.entries(data)
                    .sort((a, b) => a[1].place - b[1].place);  // Sort by carData["place"]

                // Update each pre-placed car div based on its position in the standings
                sortedCars.forEach(([carNumber, carData], index) => {
                    const carDiv = document.getElementById((index + 1).toString());  // Get the div by its rank ID
                    if (carDiv) {
                        carDiv.textContent = carNumber;  // Display the car number in the div

                        // Optionally, update other properties like color based on the car's place
                        if (carData.place === 1) {
                            carDiv.style.backgroundColor = 'gold';  // First place car gets gold
                        } else if (carData.place === 2) {
                            carDiv.style.backgroundColor = 'silver';  // Second place car gets silver
                        } else if (carData.place === 3) {
                            carDiv.style.backgroundColor = 'red';  // Third place car gets bronze
                        } else {
                            carDiv.style.backgroundColor = 'blue';  // Default color for others
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
    startRace();
    getRaceData();

});
