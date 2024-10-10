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


class AiCar:
    def __init__(self, name, number, fast_lap_time, passing, defending):
        self.name = name
        self.number = number
        self.passing = passing
        self.defending = defending
        self.total_race_time = 0
        self.fast_lap_time = fast_lap_time
        self.current_laptime_standing = fast_lap_time
        self.strategy = []
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
        self.strategy[2] -= 1

    def update_time_for_dirty_air(self, dirty_air_update):
        self.total_race_time += dirty_air_update

    def pit_stop(self):
        self.current_laptime_standing = self.fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.total_race_time += 40

    def edit_push(self, push_level):
        self.push_tire = push_level

    def calc_strat(self, laps_to_go, laps_able_to_go_on_tires, base_lap_time, tire_falloff, wear_percent, init_push_level):
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







class Race:
    def __init__(self):
        self.lap = 1
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)
        print(f"Added {car.name} to the race")
    
    def set_Ai_strats(self, laps_to_go):
        for car in self.cars:
            if isinstance(car, AiCar):
                car.strategy = car.choose_strat(laps_to_go)

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
                    odds_no_pass = abs(int((60 - odds_of_pass) * 100))
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

    def update_AI_push(self):
        #meant to go before lap is run [avg_lap_time_for_strat, stops, laps_per_stint, push_avalible, init_push_level]
        sorted_cars = sorted(self.cars, key=lambda car: car.total_race_time)
        for slot in range(len(sorted_cars)):
            if isinstance(sorted_cars[slot], AiCar) and sorted_cars[slot].strategy[4] != 5:
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


    def go_racing(self):
        if self.lap <= 267:
            self.update_AI_push()
            self.advance_lap()
            self.calc_dirty_air()
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
car22 = AiCar("LOG", 22, 30.5, 20, -20)

race = Race()
race.add_car(car1)
race.add_car(car5)
race.add_car(car11)
race.add_car(car22)
race.set_Ai_strats(267)
race.go_racing()