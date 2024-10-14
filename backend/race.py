from backend.car import Car
from backend.car_AI import AI
import random

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
        self.lap_count = 267
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

    def calc_dirty_air(self): # needs work
        """
        Calculates the effects of 'dirty air' on the cars. 'Dirty air' refers to reduced performance 
        due to aerodynamic turbulence when following closely behind another car. Cars affected by dirty 
        air have their total race time updated accordingly.
        
        The current implementation only penalizes cars that are close to another car based on race time.
        """

        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        for i in range(len(sorted_cars)):
            car = sorted_cars[i]
            if i == 0:
                pass
            else:
                gap_ahead = sorted_cars[i].total_race_time - sorted_cars[i-1].total_race_time
                if gap_ahead <= 0.06:
                    pass
                elif gap_ahead <= 0.4:
                    odds_of_pass = (sorted_cars[i-1].defending + abs(sorted_cars[i].passing)) / 2
                    odds_no_pass = abs(int((30 - odds_of_pass) * 100))
                    seconds_of_dirty_air = (int(random.randint(0, odds_no_pass)/100)) / 100
                    print(seconds_of_dirty_air)
                    sorted_cars[i].update_time_for_dirty_air(seconds_of_dirty_air)

    def get_standings(self):
        """
        Returns the current race standings by sorting the cars based on their total race time.

        Returns:
            list: A sorted list of cars, with the leading car (shortest race time) first.
        """

        self.standings = sorted(self.cars, key=lambda car: car.total_race_time)
        return self.standings

    def update_AI_push(self): # needs work
        """
        Adjusts the push level of AI-controlled cars based on their strategy and race conditions.
        This method checks if AI cars should increase their push level based on available tire life 
        or their proximity to other cars.
        """

        #meant to go before lap is run [avg_lap_time_for_strat, stops, laps_per_stint, push_avalible, init_push_level]
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        for slot in range(len(sorted_cars)):
            if isinstance(sorted_cars[slot], AI) and sorted_cars[slot].strategy[4] != 5:
                if sorted_cars[slot].strategy[3] > sorted_cars[slot].strategy[2]:
                    sorted_cars[slot].edit_push(sorted_cars[slot].strategy[4] + 1)
                elif slot != 0:
                    if sorted_cars[slot].total_race_time - sorted_cars[slot - 1].total_race_time < 0.4 and sorted_cars[slot].strategy[3] > 0:
                        sorted_cars[slot].edit_push(sorted_cars[slot].strategy[4] + 1)
                elif slot != 3:
                    if sorted_cars[slot + 1].total_race_time - sorted_cars[slot].total_race_time < 0.4 and sorted_cars[slot].strategy[3] > 0:
                        sorted_cars[slot].edit_push(sorted_cars[slot].strategy[4] + 1)
                else:
                    sorted_cars[slot].edit_push(sorted_cars[slot].strategy[4])

    def next_lap(self):
        """
        Advances the race by one lap, updating the AI push levels and recalculating dirty air effects.
        """

        self.update_AI_push()
        self.advance_lap()
        self.calc_dirty_air()

    def race_end(self):
        """
        Checks whether the race has reached its end based on the lap count.

        Returns:
            bool: True if the current lap is greater than or equal to the total lap count, False otherwise.
        """

        return self.lap >= self.lap_count
    

def start():
    """
    Initializes a race with a set of predefined cars (both human-controlled and AI) and adds them to the race.

    Returns:
        Race: The initialized race object with the cars added.
    """

    state = Race()
    cars = [
        #Driver | Car Num | Base Lap Time | Pass Eff. | Def. Rat. | Race State
        Car("CHA", 1, 30.5, 22.45, -10.65, state),
        Car("LAR", 5, 30.5, 24.68, -6.72, state),
        AI("HAM", 11, 30.5, 23.42,-13.02, state),
        AI("LOG", 22, 30.5, 20, -20, state)
    ]
    for car in cars: state.add_car(car)
    return state

def race_end(state):
    """
    Determines if the race has ended by checking the race's lap count.

    Args:
        state (Race): The current state of the race.

    Returns:
        bool: True if the race has ended, False otherwise.
    """

    return state.race_end()
