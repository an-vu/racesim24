from backend import car
import random

class AI(car.Car):
    """
    AI class representing a car controlled by an algorithm.
    Inherits from the 'Car' class and adds strategic race decision-making functionality.

    Attributes:
        strategy (list): List of calculated strategy values for the AI's race plan.
    """

    def __init__(self, name, number, fast_lap_time, passing, defending, race_state):
        """
        Initializes the AI object with car attributes and selects a race strategy.

        Args:
            name (str): Name of the car or driver.
            number (int): Car's number in the race.
            fast_lap_time (float): Car's fastest lap time.
            passing (int): The car's passing skill rating.
            defending (int): The car's defending skill rating.
            race_state (RaceState): The current state of the race, containing lap count and other relevant details.
        
        Attributes:
            strategy (list): The chosen race strategy based on lap count and performance metrics.
        """

        super().__init__(name, number, fast_lap_time, passing, defending, race_state)
        self.strategy = self.choose_strat(race_state.lap_count)

    def calc_strat(self, laps_to_go, laps_able_to_go_on_tires, base_lap_time, tire_falloff, wear_percent, init_push_level):
        """
        Calculates the race strategy based on remaining laps, tire wear, and other factors.

        Args:
            laps_to_go (int): The number of laps remaining in the race.
            laps_able_to_go_on_tires (int): The number of laps the car can drive before needing to change tires.
            base_lap_time (float): The base time it takes the car to complete a lap under normal conditions.
            tire_falloff (float): The rate at which tire performance declines per lap.
            wear_percent (float): The percentage of tire wear per lap.
            init_push_level (int): The initial aggressiveness or "push" level for the stint.

        Returns:
            list: A list containing the following strategy details:
                - avg_lap_time_for_strat (float): The average lap time for this strategy.
                - stops (int): The number of pit stops required for this strategy.
                - laps_per_stint (int): The number of laps driven per stint between pit stops.
                - push_available (float): The remaining ability to "push" during the race based on tire wear.
                - init_push_level (int): The initial push level for this strategy.
        """
        
        stops = laps_to_go // laps_able_to_go_on_tires
        stints = stops + 1
        laps_per_stint = laps_to_go // stints
        stints_with_x_lap = laps_to_go - (laps_per_stint * stints)
        fall_off_to_add = (tire_falloff * laps_per_stint) * stints_with_x_lap
        init_lap_time_to_add = base_lap_time * stints_with_x_lap
        total_pit_time = 40 * stops
        total_track_time = (laps_per_stint * base_lap_time) * stints + (sum(range(laps_per_stint-1)) * tire_falloff) * stints + fall_off_to_add + init_lap_time_to_add + total_pit_time
        avg_lap_time_for_strat = total_track_time / laps_to_go
        push_avalible = (100 - (laps_per_stint * wear_percent)) / wear_percent
        return [avg_lap_time_for_strat, stops, laps_per_stint, push_avalible, init_push_level]

    def choose_strat(self, laps_to_go):
        """
        Chooses the optimal race strategy from a set of predefined strategies based on the remaining laps.

        Args:
            laps_to_go (int): The number of laps remaining in the race.

        Returns:
            list: The selected strategy that balances lap time and pit stop frequency.
        """

        conserve_strat = self.calc_strat(laps_to_go, 56, 30.8, 0.038, 1.78, 1)
        light_strat = self.calc_strat(laps_to_go, 53, 30.65, 0.044, 1.89, 2)
        standard_strat = self.calc_strat(laps_to_go, 50, 30.5, 0.05, 2, 3)
        push_strat = self.calc_strat(laps_to_go, 47, 30.35, 0.056, 2.11, 4)
        attack_strat = self.calc_strat(laps_to_go, 45, 30.2, 0.062, 2.22, 5)
        strats = [conserve_strat, light_strat, standard_strat, push_strat, attack_strat]
        strats.sort(key=lambda x: x[0])
        random_number = random.randint(1,100)
        if strats[1][0] - strats[0][0] < 2:
            if random_number < 70:
                return strats[0]
            else:
                return strats[1]
        elif strats[1][0] - strats[0][0] < 5:
            if random_number < 86:
                return strats[0]
            else:
                return strats[1]
        else:
            return strats[0]
        