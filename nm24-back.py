import random

class Car:
    def __init__(self, name, number, fast_lap_time, passing, defending):
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
            1: lambda: self.update_drive(0.025, 1.5, 0.7),
            2: lambda: self.update_drive(0.0375, 1.75, 0.35),
            3: lambda: self.update_drive(0.05, 2, 0),
            4: lambda: self.update_drive(0.065, 2.25, -0.4),
            5: lambda: self.update_drive(0.08, 2.5, -0.8)
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


class Race:
    def __init__(self):
        self.lap = 1
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)
        print(f"Added {car.name} to the race")

    def advance_lap(self):
        for car in self.cars:
            car.drive()

    def calc_dirty_air(self):
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
                    odds_no_pass = abs(int((70 - odds_of_pass) * 100))
                    seconds_of_dirty_air = (int(random.randint(0, odds_no_pass)/100)) / 100
                    print(seconds_of_dirty_air)
                    sorted_cars[i].update_time_for_dirty_air(seconds_of_dirty_air)

    def display_standings(self):
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        print(f"Lap {self.lap}/267 --- {267 - self.lap + 1} to go")
        for slot in range(len(sorted_cars)):
            print(  f'{slot + 1}\t'
                    f'{sorted_cars[slot].number}\t'
                    f'{sorted_cars[slot].name}\t'
                    f'{"---" if slot == 0 else f"{sorted_cars[0].total_race_time - sorted_cars[slot].total_race_time:.2f}"}\t'
                    f'{"---" if slot == 0 else f"{sorted_cars[slot - 1].total_race_time - sorted_cars[slot].total_race_time:.2f}"}\t'
                    f'{sorted_cars[slot].tire_life:.0f}\t'
                    f'{sorted_cars[slot].fuel_level:.0f}'
                )

    def print_cars_list(self):
        slot = 0
        for car in self.cars:
            print(  f'{slot}\t'
                    f'{car.number}\t'
                    f'{car.name}\t'
                    f'Push: {car.push_tire}\t'
            )
            slot += 1
        print()

    def pit_in(self):
        more_changes = 'y'
        while more_changes == 'y':
            self.print_cars_list()
            slot_to_edit = int(input("Car slot to pit: "))
            self.cars[slot_to_edit].pit_stop()
            more_changes = input('Make more strategy changes? y/n: ')

    def edit_strategy(self):
        more_changes = 'y'
        while more_changes == 'y':
            self.print_cars_list()
            slot_to_edit = int(input("Car slot to edit: "))
            push_level_update = int(input("Set push level 1/2/3/4/5 Conservative -> aggressive: "))
            self.cars[slot_to_edit].edit_push(push_level_update)
            more_changes = input('Make more strategy changes? y/n: ')

    def go_racing(self):
        if self.lap <= 267:
            self.calc_dirty_air()
            self.advance_lap()
            self.display_standings()
            advance = input('Advance[ENTER], Stratagy[s], Pit[p]:')
            if advance == "s":
                print()
                self.edit_strategy()
            elif advance == 'p':
                self.pit_in()
            self.lap += 1
            self.go_racing()
        else:
            print()
            print()
            print()
            print("Results")
            print()
            self.display_standings()




car1 = Car("CHA", 1, 30.5, 22.45, -10.65)
car5 = Car("LAR", 5, 30.5, 24.68, -6.72)
car11 = Car("HAM", 11, 30.5, 23.42,-13.02)

race = Race()
race.add_car(car1)
race.add_car(car5)
race.add_car(car11)
race.go_racing()