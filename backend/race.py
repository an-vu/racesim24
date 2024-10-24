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
        # self.get_standings()

    def calc_dirty_air(self, force_dirty_air=False): # needs work
        """
        Calculates the effects of 'dirty air' on the cars. 'Dirty air' refers to reduced performance 
        due to aerodynamic turbulence when following closely behind another car. Cars affected by dirty 
        air have their total race time updated accordingly.
        
        The current implementation only penalizes cars that are close to another car based on race time.
        """
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)

        for i in range(1, len(sorted_cars)):
            car = sorted_cars[i]
            gap_ahead = car.total_race_time - sorted_cars[i-1].total_race_time
            
            # If force_dirty_air is True, skip probability calculation and apply 100% dirty air
            if force_dirty_air:
                seconds_of_dirty_air = 40  # Maximum dirty air penalty applied
                # Apply dirty air penalty
                car.update_time_for_dirty_air(seconds_of_dirty_air)
                print(f"Force Dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")
            else:
                if gap_ahead <= 0.06:
                    # Cars are extremely close, higher likelihood of dirty air
                    # Apply the strongest dirty air penalty or effect
                    odds_of_pass = (sorted_cars[i-1].defending + abs(car.passing)) / 2
                    odds_no_pass = abs(int((10 - odds_of_pass) * 100))  # Smaller range for stronger effect
                    seconds_of_dirty_air = (int(random.randint(0, odds_no_pass)) / 100)
                    car.update_time_for_dirty_air(seconds_of_dirty_air)
                    print(f"Strong dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")

                elif gap_ahead <= 0.4:
                    # Still close but less intense dirty air effect
                    odds_of_pass = (sorted_cars[i-1].defending + abs(car.passing)) / 2
                    odds_no_pass = abs(int((30 - odds_of_pass) * 100))  # Less intense effect
                    seconds_of_dirty_air = (int(random.randint(0, odds_no_pass)) / 100)
                    car.update_time_for_dirty_air(seconds_of_dirty_air)
                    print(f"Moderate dirty air effect: {seconds_of_dirty_air} seconds applied to {car.name}")

                else:
                    # Cars are far apart, no dirty air effect
                    print(f"No dirty air effect applied to {car.name}")

    # def get_standings(self):
    #     """
    #     Returns the current race standings by sorting the cars based on their total race time.

    #     Returns:
    #         list: A sorted list of cars, with the leading car (shortest race time) first.
    #     """
    #     self.standings = sorted(self.cars, key=lambda car: car.total_race_time)
    #     return self.standings

    def update_AI_push(self): # needs work
        """
        Adjusts the push level of AI-controlled cars based on their strategy and race conditions.
        This method checks if AI cars should increase their push level based on available tire life 
        or their proximity to other cars.
        """

        #meant to go before lap is run [avg_lap_time_for_strat, stops, laps_per_stint, push_avalible, init_push_level]
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        for slot in range(len(sorted_cars)):
            car = sorted_cars[slot]
            
            # Call check_pit_stop() for AI cars before updating push level
            if isinstance(car, AI):
                car.check_pit_stop()  # Check if the AI car needs to pit

                if isinstance(car, AI) and car.strategy[4] != 5:
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
        # Initialize a variable to store the car with the smallest total race time
        smallest_race_time = float('inf')  # Start with a large number so any race time will be smaller
        print(smallest_race_time)
        # Loop through all cars to find the one with the smallest total race time
        for car in self.cars:
            if car.total_race_time < smallest_race_time:
                smallest_race_time = car.total_race_time
                #print(smallest_race_time)
            
        for car in self.cars:
            car.best_race_time = smallest_race_time
            #print(car.number, car.best_race_time, car.total_race_time, 'car.')
            car.to_leader = car.total_race_time - car.best_race_time
            print(car.to_leader)

    def next_lap(self):
        """
        Advances the race by one lap, updating the AI push levels and recalculating dirty air effects.
        """
        self.get_best_time()
        self.update_AI_push()
        self.advance_lap()
        self.calc_dirty_air()
        for car in self.cars:
            car.force_pit()
        

    def race_end(self):
        """
        Checks whether the race has reached its end based on the lap count.

        Returns:
            bool: True if the current lap is greater than or equal to the total lap count, False otherwise.
        """
        print("checking race end")
        return self.lap >= self.lap_count
    
def restart(race_instance):
    """
    Restarts the race by resetting the lap number, total race time, and other relevant attributes of the provided Race instance.
    
    Args:
        race_instance (Race): The race object to be restarted.
    """
    print("Restarting the race...")
    race_instance.lap = 1
    for car in race_instance.cars:
        car.reset_for_race()  # Call reset on each car
    race_instance.standings = []
    print("Race has been reset.")

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
