class Car:
    def __init__(self, name, number, fast_lap_time, passing, defending, race_state):
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

    def drive(self):
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
        #Helper function to update lap time, tire life, fuel level, and race time
        self.current_laptime_standing += lap_time_increase
        self.tire_life -= tire_decrease
        self.fuel_level -= 1.6  # Constant fuel level decrease
        self.total_race_time += self.current_laptime_standing + race_time_adjustment

    def update_time_for_dirty_air(self, dirty_air_update):
        self.total_race_time += dirty_air_update

    def pit_stop(self):
        self.current_laptime_standing = self.fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.total_race_time += 40

    def edit_push(self, push_level):
        self.push_tire = push_level

    def __str__(self):
        return f'{self.number}\t{self.name}'
