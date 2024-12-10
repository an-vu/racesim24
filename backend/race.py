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
        self.lap_map = None
        self.lap_count = 267
        self.standings = [] # sorted list of cars
        self.lap_data = {} # init dictionary for lap data
        self.starting_gaps = [i * 0.2 for i in range(16)]

    def add_car(self, car):
        """
        Adds a car to the race.

        Args:
            car (Car or AI): The car to be added to the race.
        """

        self.cars.append(car)
        random_number = random.choice(self.starting_gaps)
        car.set_starting_pos(random_number)
        self.starting_gaps.remove(random_number)


    def advance_lap(self):
        """
        Advances the race by one lap and updates the state of each car by calling their drive method.
        """

        self.lap += 1
        for car in self.cars:
            car.drive()
        

    def calc_dirty_air(self, force_dirty_air=False):
        """
        Calculates the effects of 'dirty air' on the cars. 'Dirty air' refers to reduced performance 
        due to aerodynamic turbulence when following closely behind another car. Cars affected by dirty 
        air have their total race time updated accordingly.
        
        The current implementation only penalizes cars that are close to another car based on race time.
        """
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        updates_needed = {}

        for i in range(1, len(sorted_cars)):
            car = sorted_cars[i]
            gap_ahead = sorted_cars[i-1].total_race_time - car.total_race_time
            # If force_dirty_air is True, skip probability calculation and apply 100% dirty air
            if force_dirty_air:
                seconds_of_dirty_air = 40  # Maximum dirty air penalty applied
                # Apply dirty air penalty
                updates_needed[car.number] = seconds_of_dirty_air
                # print(f"Force Dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")
            else:
                if gap_ahead <= 0.4:
                    # Still close but less intense dirty air effect
                    odds_of_pass = (sorted_cars[i-1].defending + abs(car.passing)) / 2
                    odds_no_pass = abs(int((3 - odds_of_pass) * 100))  # Smaller range for less intense effect
                    seconds_of_dirty_air = int(random.randint(0, odds_no_pass) / 2) / 100
                    updates_needed[car.number] = seconds_of_dirty_air
                    # print(f"Moderate dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")

                else:
                    updates_needed[car.number] = 0
                    # Cars are far apart, no dirty air effect
                    # print(f"No dirty air effect applied to {car.name}")

        for car_number, time in updates_needed.items():
            car = next(c for c in sorted_cars if c.number == car_number)
            car.update_time_for_dirty_air(time)



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
        self.maybe_crash()
        self.get_best_time()
        self.map_helper()


    def race_end(self):
        """
        Checks whether the race has reached its end based on the lap count.

        Returns:
            bool: True if the current lap is greater than or equal to the total lap count, False otherwise.
        """
        return self.lap >= self.lap_count

    def map_helper(self):
        """
        Map Helper Function
        """
        standings = self.get_standings()

        for car in self.cars:
            if car.number in self.lap_data: # Check if the car's data exists
                # Update last lap time and append it to the lap times list
                last_lap_time_rounded = round(self.lap_data[car.number]["last_lap_time"], 2)
                self.lap_data[car.number]["lap_times"].append(last_lap_time_rounded)
                self.lap_data[car.number]["last_lap_time"] = round(car.last_lap_time, 2)
                self.lap_data[car.number]["total_time"] = round(car.total_race_time, 2)
                for i, car_posn in enumerate(standings):
                    if car_posn.number == car.number:
                        self.lap_data[car.number]["place"] = i + 1
            else:
                self.lap_data[car.number] = {
                    "last_lap_time" : round(car.last_lap_time, 2),
                    "lap_times" : [], # init lap times list
                    "total_time" : round(car.total_race_time, 2),
                    "place" : next(
                        (idx + 1 for idx, standing_car in enumerate(standings) if standing_car.number == car.number),
                        0
                    )
                }

    def crash(self):
        """
        When a crash happens bring the cars closer together and move the crashed car to last.
        """

        increment = 0.5
        standings = self.get_standings()
        best_time = standings[0].total_race_time
        current_time = best_time

        # Update each car's time, starting from the leader
        for i, car in enumerate(standings):
            if i == 0:
                # Leader keeps their best time
                car.total_race_time = best_time
            else:
                # Each subsequent car is spaced by increment more than the previous
                current_time += increment
                car.total_race_time = current_time

    def maybe_crash(self):
        """
        Makes a car crash?
        """
        is_crash = random.randint(0,1000)

        if is_crash <= 50: # 5% Chance of crash

            # Choose which car it happened to
            crashed_index = random.randint(0, 15)

            crashed_car = self.cars[crashed_index]
            print(f"CRASH! {crashed_car.name} crashed!")
            # Call the crash method to reposition and tighten the pack
            self.crash()

            # After crash() has recalibrated times, apply additional logic:
            # Move the crashed car to last place
            # First, sort by updated times
            self.get_standings()

            # Ensure the crashed car is placed at the end
            # Remove it from its current position and re-insert at the end
            self.cars.remove(crashed_car)
            self.cars.append(crashed_car)

            # Add penalty to crashed car
            crashed_car.total_race_time = self.cars[len(self.cars)-1].total_race_time + 1

            # Re-sort after adjustments if needed
            self.get_standings()



def restart(race_instance):
    """
    Restarts the race by resetting the lap number, total race time, and other relevant attributes of the provided Race instance.
    
    Args:
        race_instance (Race): The race object to be restarted.
    """
    race_instance.lap = 1
    race_instance.cars = []
    race_instance.standings = []
    race_instance.lap_data = {} # init dictionary for lap data
    race_instance.starting_gaps = [i * 0.2 for i in range(16)] # re init for reset
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
