""" Module providing the Car class """

class Car:
    """
    Car class representing a race car with attributes related to its performance, tire life, fuel, and race time.
    
    Attributes:
        name (str): The name of the car or driver.
        number (int): The car's number in the race.
        passing (int): The car's passing skill rating.
        defending (int): The car's defending skill rating.
        total_race_time (float): The total time spent on the race track.
        fast_lap_time (float): The car's fastest lap time.
        current_laptime_standing (float): The current lap time considering performance impacts.
        tire_life (float): The percentage of tire life remaining (100 = new tires, 0 = worn out).
        fuel_level (float): The fuel level percentage (100 = full tank, 0 = empty).
        push_tire (int): The current push level of the car, impacting tire and lap time performance.
        to_leader (float): The current time off the lead car.
    """

    def __init__(self, name, number, fast_lap_time, passing, defending, race_state, ai_or_player):
        """
        Initializes the Car object with the above attributes.

        Args:
            name (str): Name of the car or driver.
            number (int): Car's number in the race.
            fast_lap_time (float): Fastest lap time for the car.
            passing (int): Passing skill rating.
            defending (int): Defending skill rating.
            race_state (RaceState): The current state of the race.
        """

        self.name = name
        self.number = number
        self.passing = passing
        self.defending = defending
        self.total_race_time = 0
        self.fast_lap_time = fast_lap_time
        self.current_laptime_standing = fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.push_tire = 3
        self.best_race_time = 0.0
        self.to_leader = self.best_race_time - self.total_race_time
        self.ai_or_player = ai_or_player

    def drive(self):
        """
        Updates the car's performance based on the current push level (push_tire).
        The push level impacts lap time, tire wear, and overall race time. Uses a mapping
        of push levels to appropriate performance actions.
        """

        # Define a dictionary to map push_tire values to the corresponding actions
        actions = {
            1: lambda: self.update_drive(0.038, 1.78, 0.3),
            2: lambda: self.update_drive(0.044, 1.89, 0.15),
            3: lambda: self.update_drive(0.05, 2, 0),
            4: lambda: self.update_drive(0.056, 2.11, -0.15),
            5: lambda: self.update_drive(0.062, 2.22, -0.3)
        }

        # Call the corresponding action based on the value of self.push_tire
        action = actions.get(self.push_tire)
        if action:
            action()  # Execute the action

    def update_drive(self, lap_time_increase, tire_decrease, race_time_adjustment):
        """
        Helper function to update the car's lap time, tire life, fuel level, and race time.

        Args:
            lap_time_increase (float): The amount by which the lap time increases due to tire wear or performance adjustments.
            tire_decrease (float): The amount by which tire life decreases after each lap.
            race_time_adjustment (float): Adjustments to the race time due to racing conditions (positive or negative).
        """
        self.current_laptime_standing += lap_time_increase
        self.tire_life -= tire_decrease
        self.fuel_level -= 1.6  # Constant fuel level decrease
        self.total_race_time += self.current_laptime_standing + race_time_adjustment

    def update_time_for_dirty_air(self, dirty_air_update):
        """
        Updates the total race time when the car is affected by 'dirty air', which can reduce performance.

        Args:
            dirty_air_update (float): The time penalty added to the total race time due to 'dirty air' effect.
        """

        self.total_race_time += dirty_air_update

    def pit_stop(self):
        """
        Simulates a pit stop for the car. Resets the car's tire life and fuel level to 100%.
        Also adds a fixed amount of time to the total race time for the pit stop.
        """

        self.current_laptime_standing = self.fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.total_race_time += 40

    def edit_push(self, push_level):
        """
        Adjusts the push level of the car, impacting tire wear, lap time, and race performance.

        Args:
            push_level (int): The new push level, ranging from 1 (conservative) to 5 (aggressive).
        """

        self.push_tire = push_level

    def force_pit(self):
        """
        Checks for blown tire or no gas and forces a pit stop and applies a penalty.
        """

        if min(self.tire_life, self.fuel_level) <= 0:
            self.pit_stop()
            self.total_race_time += 80
            print(f"{self} Tire blown or ran out of fuel, penalty applied!")

    def reset_for_race(self):
        """
        Resets race-specific attributes for the car.
        """
        self.total_race_time = 0.0
        self.tire_life = 100.0
        self.fuel_level = 100.0
        self.best_race_time = 0
        self.to_leader = 0
        self.push_tire = 3

    def __str__(self):
        """
        Returns a string representation of the car, showing its number and name.
        
        Returns:
            str: The car's number and name in a formatted string.
        """

        return f'{self.number}\t{self.name}'
