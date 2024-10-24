document.addEventListener('DOMContentLoaded', function () {
    const navButton = document.getElementById('nav-button');
    const navMenu = document.getElementById('nav-menu');
    const clockButton = document.getElementById('clock-button');
    let showDate = false;

    navButton.onclick = function () {
        navMenu.style.display = (navMenu.style.display === 'block' ? 'none' : 'block');
    };

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
