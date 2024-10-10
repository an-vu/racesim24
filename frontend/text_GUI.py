def print_lap(race_state):
    lap = race_state.lap
    lap_count = race_state.lap_count
    print(f'Lap {lap}/{lap_count} --- {1+lap_count-lap} to go')

def car_standing(car, first_time, next_time, rank):
    if next_time != None:
        time_to_first = f'{first_time - car.total_race_time:.2f}'
        time_to_next = f'{next_time - car.total_race_time:.2f}'
    else:
        time_to_first = "---"
        time_to_next = "---"
    return f'{rank}\t{car}\t{time_to_first}\t{time_to_next}\t{car.tire_life:.2f}\t{car.fuel_level:.2f}'

def print_standings(race_state):
    print("Rank\tNumb\tName\tDis1\tDis+\tTire\tFuel")
    standings = race_state.get_standings()
    first_car_time = standings[0].total_race_time
    next_car_time = None
    rank = 1
    for car in standings:
        print(car_standing(car, first_car_time, next_car_time, rank))
        next_car_time = car.total_race_time
        rank += 1

def pick_list(car_list):
    car_num = 0
    for car in car_list:
        print(f'{car_num}\t{car}\tPush: {car.push_tire}')
        car_num += 1
    return int(input("Car number to edit: "))

def update_strategy(race_state):
    car_to_edit = pick_list(race_state.cars)
    push_level_update = int(input("Set push level 1/2/3/4/5 Conservative -> aggressive: "))
    race_state.cars[car_to_edit].edit_push(push_level_update)
    return race_state

def update_pit(race_state):
    car_to_pit = pick_list(race_state.cars)
    race_state.cars[car_to_pit].pit_stop()
    return race_state

def update(race_state):
    print_lap(race_state)
    print_standings(race_state)
    user_input = None
    while user_input != "":
        user_input = input('Advance[ENTER], Stratagy[s], Pit[p]:')
        match user_input:
            case 's': race_state = update_strategy(race_state)
            case 'p': race_state = update_pit(race_state)
            case '' : pass
            case _: print("Invalid Input")
    return race_state