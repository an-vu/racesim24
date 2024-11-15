""" Module that imports the Car and AI classed to run the races """

import random
from backend.car_ai import AI

class Race:
    """
    Represents a race with multiple cars, where the race progresses lap by lap.
    
    Attributes:
        lap (int): The current lap number of the race.
        cars (list): A list of Car and AI objects participating in the race.
        lap_count (int): The total number of laps in the race (default is 267).
        standings (list): A sorted list of cars based on their total race time.
    """

    def __init__(self):
        """
        Initializes the Race object with default values for lap, cars, lap_count, and standings.
        """

        self.lap = 1
        self.cars = []
        self.lap_count = 25
        self.standings = [] # sorted list of cars

    def add_car(self, car):
        """
        Adds a car to the race.

        Args:
            car (Car or AI): The car to be added to the race.
        """

        self.cars.append(car)

    def advance_lap(self):
        """
        Advances the race by one lap and updates the state of each car by calling their drive method.
        """

        self.lap += 1
        for car in self.cars:
            car.drive()
        # self.get_standings()

    def calc_dirty_air(self, force_dirty_air=False): # needs work
        """
        Calculates the effects of 'dirty air' on the cars. 'Dirty air' refers to reduced performance 
        due to aerodynamic turbulence when following closely behind another car. Cars affected by dirty 
        air have their total race time updated accordingly.
        
        The current implementation only penalizes cars that are close to another car based on race time.
        """
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        updates_needed = [0]

        for i in range(1, len(sorted_cars)):
            car = sorted_cars[i]
            gap_ahead = sorted_cars[i-1].total_race_time - car.total_race_time
            # If force_dirty_air is True, skip probability calculation and apply 100% dirty air
            if force_dirty_air:
                seconds_of_dirty_air = 40  # Maximum dirty air penalty applied
                # Apply dirty air penalty
                updates_needed.append(seconds_of_dirty_air)
                print(f"Force Dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")
            else:
                if gap_ahead <= 0.4:
                    # Still close but less intense dirty air effect
                    odds_of_pass = (sorted_cars[i-1].defending + abs(car.passing)) / 2
                    odds_no_pass = abs(int((3 - odds_of_pass) * 100))  # Smaller range for less intense effect
                    seconds_of_dirty_air = int(random.randint(0, odds_no_pass) / 2) / 100
                    updates_needed.append(seconds_of_dirty_air)
                    print(f"Moderate dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")

                else:
                    updates_needed.append(0)
                    # Cars are far apart, no dirty air effect
                    print(f"No dirty air effect applied to {car.name}")

        for i in range(1, len(sorted_cars)):
            car.update_time_for_dirty_air(updates_needed[i])



    def get_standings(self):
        """
        Returns the current race standings by sorting the cars based on their total race time.

        Returns:
            list: A sorted list of cars, with the leading car (shortest race time) first.
        """
        self.cars.sort(key=lambda car: car.total_race_time)
        return self.cars

    def update_ai_push(self): # needs work
        """
        Adjusts the push level of AI-controlled cars based on their strategy and race conditions.
        This method checks if AI cars should increase their push level based on available tire life 
        or their proximity to other cars.
        """

        #meant to go before lap is run [avg_lap_time_for_strat, stops, laps_per_stint, push_avalible, init_push_level]
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        for slot, car in enumerate(sorted_cars):
            # Call check_pit_stop() for AI cars before updating push level
            if isinstance(car, AI):
                car.check_pit_stop()  # Check if the AI car needs to pit
                if car.strategy[4] != 5:
                    if car.strategy[3] > car.strategy[2]:
                        car.edit_push(car.strategy[4] + 1)
                    elif slot != 0:
                        if car.total_race_time - sorted_cars[slot - 1].total_race_time < 0.4 and car.strategy[3] > 0:
                            car.edit_push(car.strategy[4] + 1)
                    elif slot != 3:
                        if sorted_cars[slot + 1].total_race_time - car.total_race_time < 0.4 and car.strategy[3] > 0:
                            car.edit_push(car.strategy[4] + 1)
                    else:
                        car.edit_push(car.strategy[4])



    def get_best_time(self):
        """
        Iterates through the cars and returns the best current total time.
        """
        # Initialize a variable to store the car with the smallest total race time
        smallest_race_time = float('inf')  # Start with a large number so any race time will be smaller
        # Loop through all cars to find the one with the smallest total race time
        for car in self.cars:
            smallest_race_time = min(smallest_race_time, car.total_race_time)

        for car in self.cars:
            car.best_race_time = smallest_race_time
            car.to_leader = car.total_race_time - car.best_race_time

    def next_lap(self):
        """
        Advances the race by one lap, updating the AI push levels and recalculating dirty air effects.
        """
        self.update_ai_push()
        self.advance_lap()
        self.calc_dirty_air()
        for car in self.cars:
            car.force_pit()
        self.get_best_time()


    def race_end(self):
        """
        Checks whether the race has reached its end based on the lap count.

        Returns:
            bool: True if the current lap is greater than or equal to the total lap count, False otherwise.
        """
        return self.lap >= self.lap_count

def restart(race_instance):
    """
    Restarts the race by resetting the lap number, total race time, and other relevant attributes of the provided Race instance.
    
    Args:
        race_instance (Race): The race object to be restarted.
    """
    race_instance.lap = 1
    for car in race_instance.cars:
        car.reset_for_race()  # Call reset on each car
    race_instance.standings = []
    print("Race has been reset.")

def race_end(state):
    """
    Determines if the race has ended by checking the race's lap count.

    Args:
        state (Race): The current state of the race.

    Returns:
        bool: True if the race has ended, False otherwise.
    """
    return state.race_end()
