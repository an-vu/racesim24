""" Module to run tests for CI Pipeline """

import pytest
from backend.car import Car
from backend.car_ai import AI
from backend.race import Race

@pytest.fixture
def race_state():
    """Fixture that initializes a race state with some cars."""
    race = Race()
    cars = [
        Car("Player 1", 2, 30.4, 22.45, -10.65, race, 1),
        Car("Player 2", 3, 30.5, 24.68, -6.72, race, 2),
        AI("HAM", 11, 30.6, 23.42, -13.02, race, 3),
        AI("LOG", 22, 30.7, 20, -20, race, 3)
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
    race_state.update_ai_push()
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

def test_calc_strat(race_state):
    """
    Tests the calc_strat function
    """
    strat = AI("TES", 11, 30.5, 23.42, -13.02, race_state, 3)
    laps_to_go = 80
    laps_able_to_go_on_tires = 50
    base_lap_time = 30.5
    tire_falloff = 0.05
    wear_percent = 2.0
    init_push_level = 3


    result = strat.calc_strat(
        laps_to_go,
        laps_able_to_go_on_tires,
        base_lap_time,
        tire_falloff,
        wear_percent,
        init_push_level,
    )


    expected_avg_lap_time = 31.92625
    expected_stops = 1
    expected_laps_per_stint = 40
    expected_push_available = 10
    expected_init_push_level = init_push_level

    assert result[0] == pytest.approx(expected_avg_lap_time, 0.01)
    assert result[1] == expected_stops
    assert result[2] == expected_laps_per_stint
    assert result[3] == pytest.approx(expected_push_available, 0.01)
    assert result[4] == expected_init_push_level

def test_crash(race_state, mocker):
    """
    Tests the crash mechanics by mocking random values to ensure a crash occurs
    and verifying the resulting standings and time adjustments.
    """
    # Ensure deterministic behavior:
    # First random call (0-1000) must trigger a crash: return a number <= 50, say 10.
    # Second random call (0-15) chooses the crashed car index, say 1.
    mocker.patch('random.randint', side_effect=[10, 1])

    standings_before = race_state.get_standings()
    crashed_car_pre = standings_before[1]  # Car at index 1 will "crash"
    times_before = [car.total_race_time for car in standings_before]

    # Trigger the crash logic
    race_state.maybe_crash()

    standings_after = race_state.get_standings()
    crashed_car_post = standings_after[-1]  # The crashed car should now be at the end

    # Check that the same car ended up last
    assert crashed_car_pre is crashed_car_post, "The expected crashed car did not end up last."

    # Check that the leader's time remains the same
    assert standings_after[0].total_race_time == pytest.approx(times_before[0], 0.01), \
        "Leader's time should remain unchanged after crash."

    # Check incremental spacing of 0.5 seconds for cars after the leader
    increment = 0.5
    for i, car in enumerate(standings_after):
        if i == 0:
            # Leader unchanged
            continue
        else:
            # Each subsequent car (except for the crashed car's final penalty) should follow increments
            # The code sets crashed_car time at the end after all increments, so check that specifically.
            if car is not crashed_car_post:
                expected_time = standings_after[0].total_race_time + (i * increment)
                assert car.total_race_time == pytest.approx(expected_time, 0.01), \
                    f"Car at position {i} does not have the expected incremented time."
    
    # Finally, check the crashed car's penalty time:
    # The code sets crashed_car total_race_time = self.cars[len(self.cars)-1].total_race_time + 1
    # After reordering, this should still be correct:
    # crashed_car_post should be at the end with 1 second more than the time of the (now second-to-last) car.
    second_to_last_car_time = standings_after[-2].total_race_time
    assert crashed_car_post.total_race_time == pytest.approx(second_to_last_car_time + 1, 0.01), \
        "Crashed car should have a 1-second penalty added to the next-to-last car's time."
