document.addEventListener('DOMContentLoaded', () => {
    // Initialize elements
    const navButton = document.getElementById('nav-button');
    const navMenu = document.getElementById('nav-menu');
    const clockButton = document.getElementById('clock-button');
    const tableBody = document.getElementById("standings-table-body");
    let showDate = false;
    let player_racer_array = [];
    let player_car_1_pit_boolean = false;
    let player_car_2_pit_boolean = false;

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

    // Navigation menu toggle
    navButton.onclick = () => {
        navMenu.style.display = navMenu.style.display === 'block' ? 'none' : 'block';
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
            updateRaceStandings(data);
            updatePlayerControlCenters();
        } catch (error) {
            console.error('Error fetching race data:', error);
        }
    }

    async function advanceLap() {
        try {
            await fetch('/api/race/lap', { method: 'POST' });
            getRaceData();
            player_car_1_pit_boolean = false;
            player_car_2_pit_boolean = false;
        } catch (error) {
            console.error('Error advancing lap:', error);
        }
    }

    async function resetRace() {
        try {
            await fetch('/api/race/reset', { method: 'POST' });
            getRaceData();
            resetStrategySelections();
        } catch (error) {
            console.error('Error resetting race:', error);
        }
    }

    function handlePitStop(carIndex, carNumber) {
        if (carIndex === 0 && player_car_1_pit_boolean) return;
        if (carIndex === 1 && player_car_2_pit_boolean) return;

        const pitBooleanVar = carIndex === 0 ? 'player_car_1_pit_boolean' : 'player_car_2_pit_boolean';
        window[pitBooleanVar] = true;

        fetch('/api/race/pit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number: carNumber })
        })
        .then(getRaceData)
        .catch(error => console.error(`Error performing pit stop for Car #${carNumber}:`, error));
    }

    function handleStrategyChange(carIndex, strategyLevel) {
        fetch('/api/race/strategy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number: player_racer_array[carIndex].number, push_level: strategyLevel })
        })
        .then(getRaceData)
        .catch(error => console.error(`Error updating strategy for Car #${carIndex + 1}:`, error));
    }

    function updatePlayerCars(cars) {
        player_racer_array = cars.filter(car => car.ai_or_player !== 3);
        if (player_racer_array[0]) {
            document.getElementById('car-1-title').textContent = `#${player_racer_array[0].number} ${player_racer_array[0].name}`;
        }
        if (player_racer_array[1]) {
            document.getElementById('car-2-title').textContent = `#${player_racer_array[1].number} ${player_racer_array[1].name}`;
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
        if (player_racer_array[0]) {
            document.getElementById('player-car-1-current-strategy').textContent = `Strategy Level: ${player_racer_array[0].push_tire}`;
            document.getElementById('player-car-1-tire').textContent = `Tire %: ${player_racer_array[0].tire_life.toFixed(2)}%`;
            document.getElementById('player-car-1-fuel').textContent = `Fuel %: ${player_racer_array[0].fuel_level.toFixed(2)}%`;
        }
        if (player_racer_array[1]) {
            document.getElementById('player-car-2-current-strategy').textContent = `Strategy Level: ${player_racer_array[1].push_tire}`;
            document.getElementById('player-car-2-tire').textContent = `Tire %: ${player_racer_array[1].tire_life.toFixed(2)}%`;
            document.getElementById('player-car-2-fuel').textContent = `Fuel %: ${player_racer_array[1].fuel_level.toFixed(2)}%`;
        }
    }

    function resetStrategySelections() {
        document.querySelectorAll('input[name="strategy1"], input[name="strategy2"]').forEach(radio => radio.checked = false);
    }

    // Event Listeners for Pit and Strategy Buttons
    document.getElementById('player-car-1-pit').addEventListener('click', () => handlePitStop(0, player_racer_array[0].number));
    document.getElementById('player-car-2-pit').addEventListener('click', () => handlePitStop(1, player_racer_array[1].number));
    document.querySelectorAll('input[name="strategy1"]').forEach(radio => 
        radio.addEventListener('change', () => handleStrategyChange(0, radio.value)));
    document.querySelectorAll('input[name="strategy2"]').forEach(radio => 
        radio.addEventListener('change', () => handleStrategyChange(1, radio.value)));

    // Other Initializations
    document.getElementById('lap-button').addEventListener('click', advanceLap);
    document.getElementById('reset-button').addEventListener('click', resetRace);

    // Load player data from localStorage
    const player1Data = { name: localStorage.getItem("player1Name") || "Player 1", car: localStorage.getItem("player1Car") || "00", pic: localStorage.getItem("player1Picture") || "profile1.png" };
    const player2Data = { name: localStorage.getItem("player2Name") || "Player 2", car: localStorage.getItem("player2Car") || "00", pic: localStorage.getItem("player2Picture") || "profile2.png" };

    document.getElementById("car-1-title").textContent = `${player1Data.name} - Car #${player1Data.car}`;
    document.getElementById("car-2-title").textContent = `${player2Data.name} - Car #${player2Data.car}`;
    document.getElementById("player1-profile").style.backgroundImage = `url('/static/images/profiles/${player1Data.pic}')`;
    document.getElementById("player2-profile").style.backgroundImage = `url('/static/images/profiles/${player2Data.pic}')`;

    // Start and fetch initial race data
    startRace();
    getRaceData();
});
