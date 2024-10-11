from backend.car import Car
from backend.car_AI import AI
import random

class Race:
    def __init__(self):
        self.lap = 1
        self.cars = []
        self.lap_count = 267
        self.standings = [] # sorted list of cars

    def add_car(self, car):
        self.cars.append(car)

    def advance_lap(self):
        self.lap += 1
        for car in self.cars:
            car.drive()

    def calc_dirty_air(self): # needs work
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
        self.standings = sorted(self.cars, key=lambda car: car.total_race_time)
        return self.standings

    def update_AI_push(self): # needs work
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
        self.update_AI_push()
        self.advance_lap()
        self.calc_dirty_air()

    def race_end(self):
        return self.lap >= self.lap_count
    

def start():
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
    return state.race_end()
