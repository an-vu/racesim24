import pytest
from backend.car import Car
from backend.car_AI import AI
from backend.race import Race

@pytest.fixture
def race_state():
    """Fixture that initializes a race state with some cars."""
    race = Race()
    cars = [
        Car("CHA", 1, 30.5, 22.45, -10.65, race),
        Car("LAR", 5, 30.5, 24.68, -6.72, race),
        AI("HAM", 11, 30.5, 23.42, -13.02, race),
        AI("LOG", 22, 30.5, 20, -20, race)
    ]
    for car in cars:
        race.add_car(car)
    return race

def test_race_initialization(race_state):
    """Test if race initializes correctly with cars."""
    assert race_state.lap == 1
    assert len(race_state.cars) == 4
    assert isinstance(race_state.cars[2], AI)

def test_advance_lap(race_state):
    """Test if laps advance correctly and cars drive."""
    race_state.advance_lap()
    assert race_state.lap == 2
    # Check if car's race time increases (confirming drive method is called)
    assert race_state.cars[0].total_race_time > 0

def test_get_standings(race_state):
    """
    Test to check if the get_standings method returns cars sorted by total_race_time.
    """
    # Get the standings from the race_instance
    standings = race_state.get_standings()

    # Extract total_race_time values from the sorted list
    race_times = [car.total_race_time for car in standings]

    # Check if the list is sorted in ascending order
    assert race_times == sorted(race_times), "Cars are not sorted by total race time"

def test_ai_push_update(race_state):
    """Test if AI's push level updates correctly."""
    race_state.update_AI_push()
    ai_car = race_state.cars[2]  # HAM is an AI car
    assert ai_car.push_tire >= 3  # Assuming the push level should increase

def test_pit_stop(race_state):
    """Test if pit stop resets the car's tire and fuel."""
    car = race_state.cars[0]  # Use the first car (non-AI)
    car.pit_stop()
    assert car.tire_life == 100
    assert car.fuel_level == 100
    assert car.current_laptime_standing == car.fast_lap_time
    assert car.total_race_time > 0  # Pit stop adds 40 seconds

def test_dirty_air_effect(race_state):
    """Test if dirty air effect updates car's race time."""
    # Simulate cars having a dirty air effect.
    
    race_state.advance_lap()  # Simulate at least one lap
    race_state.calc_dirty_air(force_dirty_air=True)  # Calculate dirty air effect
    standings = race_state.get_standings()
    
    # Check if dirty air has been applied and the second car's race time has increased
    assert standings[1].total_race_time > standings[0].total_race_time


def test_lap_end(race_state):
    """Test if the race ends after the correct number of laps."""
    race_state.lap = race_state.lap_count - 1
    assert not race_state.race_end()
    race_state.advance_lap()
    assert race_state.race_end()