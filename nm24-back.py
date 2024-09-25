class Car:
    def __init__(self, name, number, fast_lap_time):
        self.name = name
        self.number = number
        self.total_race_time = 0
        self.fast_lap_time = fast_lap_time
        self.current_laptime_standing = fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.push_tire = 3

    def drive(self):
        if self.push_tire == 1:
             self.current_laptime_standing += 0.02
             self.tire_life -= 1
             self.fuel_level -= 1.6
             self.total_race_time += self.current_laptime_standing + 0.5
        if self.push_tire == 2:
             self.current_laptime_standing += 0.03
             self.tire_life -= 1.5
             self.fuel_level -= 1.6
             self.total_race_time += self.current_laptime_standing + 0.25
        if self.push_tire == 3:
             self.current_laptime_standing += 0.04
             self.tire_life -= 2
             self.fuel_level -= 1.6
             self.total_race_time += self.current_laptime_standing
        if self.push_tire == 4:
             self.current_laptime_standing += 0.05
             self.tire_life -= 2.5
             self.fuel_level -= 1.6
             self.total_race_time += self.current_laptime_standing - 0.25
        if self.push_tire == 5:
             self.current_laptime_standing += 0.06
             self.tire_life -= 3
             self.fuel_level -= 1.6
             self.total_race_time += self.current_laptime_standing - 0.5

    def pit_stop(self):
        self.current_laptime_standing = self.fast_lap_time
        self.tire_life = 100
        self.fuel_level = 100
        self.total_race_time += 70

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




car1 = Car("CHA", 1, 30.5)
car5 = Car("LAR", 5, 30.5)
car11 = Car("HAM", 11, 30.5)

race = Race()
race.add_car(car1)
race.add_car(car5)
race.add_car(car11)
race.go_racing()