document.addEventListener('DOMContentLoaded', function () {
    // Navigation Menu and Clock
    const navButton = document.getElementById('nav-button');
    const navMenu = document.getElementById('nav-menu');
    const clockButton = document.getElementById('clock-button');
    let showDate = false;

    navButton.onclick = function () {
        navMenu.style.display = (navMenu.style.display === 'block' ? 'none' : 'block');
    };

    // Toggle clock between date and time
    function updateClock() {
        const now = new Date();
        clockButton.textContent = showDate ? now.toLocaleDateString() : now.toLocaleTimeString();
    }
    setInterval(updateClock, 1000);
    clockButton.addEventListener('click', () => {
        showDate = !showDate;
        updateClock();
    });

    // Only run the following if we are on home.html
    if (document.getElementById('lap-button')) {
        startRace();
        getRaceData();
        handlePitButtons();
        handleStrategyButtons();

        document.getElementById('lap-button').addEventListener('click', advanceLap);
        document.getElementById('reset-button').addEventListener('click', resetRace);

        // Retrieve and display player information from localStorage
        const player1Name = localStorage.getItem("player1Name") || "Player 1";
        const player1Car = localStorage.getItem("player1Car") || "00";
        const player1Picture = localStorage.getItem("player1Picture") || "profile1.png";
        
        const player2Name = localStorage.getItem("player2Name") || "Player 2";
        const player2Car = localStorage.getItem("player2Car") || "00";
        const player2Picture = localStorage.getItem("player2Picture") || "profile2.png";

        document.getElementById("car-1-title").textContent = `${player1Name} - Car #${player1Car}`;
        document.getElementById("car-2-title").textContent = `${player2Name} - Car #${player2Car}`;

        document.getElementById("player1-profile").style.backgroundImage = `url('/static/images/profiles/${player1Picture}')`;
        document.getElementById("player2-profile").style.backgroundImage = `url('/static/images/profiles/${player2Picture}')`;
    };

    // GAME LOGIC ETC
    let player_racer_array = [];
        let player_car_1_pit_boolean = [];
        let player_car_2_pit_boolean = [];
    
        // Data for the cars
        const carData = Array.from({ length: 16 }, (_, i) => ({
            position: i + 1,
            carNumber: '--',
            driver: '--',
            toLeader: '--',
            totalTime: '--',
            tire: '--',
            fuel: '--'
        }));
    
        const tableBody = document.getElementById("standings-table-body");
    
        // Generate rows dynamically based on carData
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
    
        async function startRace() {
            try {
                const response = await fetch('/api/race');
                const data = await response.json();
                
                // Identify player-controlled cars
                player_racer_array = data.cars.filter(car => car.ai_or_player != 3);
                
                if (player_racer_array[0]) {
                    document.getElementById('car-1-title').textContent = `#${player_racer_array[0].number} ${player_racer_array[0].name}`;
                }
                if (player_racer_array[1]) {
                    document.getElementById('car-2-title').textContent = `#${player_racer_array[1].number} ${player_racer_array[1].name}`;
                }
    
            } catch (error) {
                console.error('Error starting race', error);
            }
        }
    
        async function getRaceData() {
            try {
                const response = await fetch('/api/race');
                const data = await response.json();
                
                player_racer_array = data.cars.filter(car => car.ai_or_player != 3);
                player_racer_array.sort((a, b) => a.ai_or_player - b.ai_or_player);


                // Update lap count
                document.getElementById('standings-title').textContent = `Standings - Lap: ${data.lap} of ${data.lap_count}`;
    
                // Update standings for each car
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
    
                // Update Player Car Control Centers
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
    
            } catch (error) {
                console.error('Error fetching race data:', error);
            }
        }
    
        async function advanceLap() {
            try {
                await fetch('/api/race/lap', { method: 'POST' });
                getRaceData();  // Refresh data after advancing the lap
                player_car_1_pit_boolean = false;
                player_car_2_pit_boolean = false;
            } catch (error) {
                console.error('Error advancing lap:', error);
            }
        }
    
        function handlePitButtons() {
            document.getElementById('player-car-1-pit').addEventListener('click', async () => {
                try {
                    if (player_car_1_pit_boolean != true) {
                        player_car_1_pit_boolean = true;
                        await fetch('/api/race/pit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ number: player_racer_array[0].number })
                        });
                        console.log(`${player_racer_array[0].number} Entered pit`);
                        getRaceData();  // Refresh data after performing pit stop
                    } else {
                        console.log(`${player_racer_array[0]} already entered pit!`)
                    }
                } catch (error) {
                    console.error('Error performing pit stop for Car #1:', error);
                }
            });
    
            document.getElementById('player-car-2-pit').addEventListener('click', async () => {
                try {
                    if (player_car_2_pit_boolean != true) {
                        player_car_2_pit_boolean = true;
                        await fetch('/api/race/pit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ number: player_racer_array[1].number })
                        });
                        console.log(`${player_racer_array[1].number} Entered pit`);
                        getRaceData();  // Refresh data after performing pit stop
                    } else {
                        console.log(`${player_racer_array[1]} already entered pit!`)
                    }
                } catch (error) {
                    console.error('Error performing pit stop for Car #2:', error);
                }
            });
        }
    
        function handleStrategyButtons() {
            document.querySelectorAll('input[name="strategy1"]').forEach(radio => {
                radio.addEventListener('change', async () => {
                    const strategyLevel = radio.value;
                    try {
                        await fetch('/api/race/strategy', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ number: player_racer_array[0].number, push_level: strategyLevel })
                        });
                        getRaceData();  // Refresh data after updating strategy
                    } catch (error) {
                        console.error('Error updating strategy for Car #1:', error);
                    }
                });
            });
    
            document.querySelectorAll('input[name="strategy2"]').forEach(radio => {
                radio.addEventListener('change', async () => {
                    const strategyLevel = radio.value;
                    try {
                        await fetch('/api/race/strategy', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ number: player_racer_array[1].number, push_level: strategyLevel })
                        });
                        getRaceData();  // Refresh data after updating strategy
                    } catch (error) {
                        console.error('Error updating strategy for Car #2:', error);
                    }
                });
            });
        }
    
        async function resetRace() {
            try {
                await fetch('/api/race/reset', { method: 'POST' });
                getRaceData();  // Refresh data after resetting the race
                
                // Unselect all strategy1 radio buttons
                document.querySelectorAll('input[name="strategy1"]').forEach(radio => {
                    radio.checked = false;
                });

                // Unselect all strategy2 radio buttons
                document.querySelectorAll('input[name="strategy2"]').forEach(radio => {
                    radio.checked = false;
                });

            } catch (error) {
                console.error('Error resetting race:', error);
            }
        }


    // WEBSITE FUNCTION VISUAL ETC

    // Toggle between time and date display on the clock button
    function updateClock() {
        const now = new Date();
        let display = now.toLocaleTimeString(); // Default to time
        if (showDate) {
            const options = { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' };
            display = now.toLocaleDateString('en-US', options).replace(',', ''); // Change to full date
        }
        clockButton.textContent = display;
    }

    // Toggle date/time display on clock button click
    clockButton.addEventListener('click', () => {
        showDate = !showDate; // Toggle between time and date display
        updateClock(); // Immediate update
    });

    setInterval(updateClock, 1000); // Update the clock every second

    // // Hide the nav menu when clicking outside of it
    // document.addEventListener('click', function (event) {
    //     if (!navButton.contains(event.target) && !navMenu.contains(event.target)) {
    //         navMenu.style.display = 'none';
    //     }
    // });
});
