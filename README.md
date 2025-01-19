# NASCAR Manager '24

**NASCAR Manager '24** is a Flask-based race simulation platform using **real-world racer data**. Players step into the role of a race strategist, managing drivers, pit crews, and race-day strategies to lead their team to victory.

---

## Features

- **Race Simulation**: Advance laps, manage pit stops, and monitor car performance metrics like lap times, tire wear, and fuel levels.
- **API Integration**: Interact with race data via RESTful API endpoints for customization and automation.
- **Dynamic Dashboard**: View real-time race status and car metrics on a seamless, responsive web interface.
- **Real-World Data**: Built on actual racer performance for an authentic experience.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, JavaScript (Fetch API)
- **Testing**: Pytest
- **CI/CD**: GitLab CI pipelines
- **Containerization**: Docker for deployment

---

## Getting Started

### Prerequisites
- Docker installed on your machine.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/an-vu/racesim24.git
   cd racesim24
   ```

2. Build and run the Docker image:
   ```bash
   docker build -t nascar-manager .
   docker run -p 5000:5000 nascar-manager
   ```

3. Access the application:
   - Open `http://localhost:5000` in your browser.

---

## API Endpoints

- **GET `/api/race`**: Retrieve current race data.
- **POST `/api/race/lap`**: Advance the race by one lap.
- **POST `/api/race/pit`**: Request a pit stop for a specific car.
- **POST `/api/race/reset`**: Reset the race simulation.

---

## Running the Application

1. Start the application using Docker or a local Flask server:
   ```bash
   flask run
   ```

2. Access the web interface at `http://localhost:5000`.

---

## Testing

Run unit tests using Pytest:
```bash
pytest
```

---

## Deployment

To deploy with Docker:
1. Build the Docker image:
   ```bash
   docker build -t nascar-manager .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 nascar-manager
   ```

---
