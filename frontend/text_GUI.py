def print_lap(race_state):
    """
    Prints the current lap number and the number of laps remaining in the race.

    Args:
        race_state (Race): The current state of the race.
    """

    lap = race_state.lap
    lap_count = race_state.lap_count
    print(f'Lap {lap}/{lap_count} --- {1+lap_count-lap} to go')

def car_standing(car, first_time, next_time, rank):
    """
    Returns a formatted string representing a car's standing in the race, including its rank, 
    time to the leader, time to the next car, tire life, and fuel level.

    Args:
        car (Car): The car whose standing is being printed.
        first_time (float): The total race time of the car in the lead.
        next_time (float or None): The total race time of the next car behind.
        rank (int): The rank of the car.

    Returns:
        str: A formatted string displaying the car's rank, name, time to the leader and next car, tire life, and fuel level.
    """

    if next_time != None:
        time_to_first = f'{first_time - car.total_race_time:.2f}'
        time_to_next = f'{next_time - car.total_race_time:.2f}'
    else:
        time_to_first = "---"
        time_to_next = "---"
    return f'{rank}\t{car}\t{time_to_first}\t{time_to_next}\t{car.tire_life:.2f}\t{car.fuel_level:.2f}'

def print_standings(race_state):
    """
    Prints the current race standings, displaying each car's rank, name, time to the leader, time to the next car, tire life, and fuel level.

    Args:
        race_state (Race): The current state of the race, used to get the standings.
    """

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
    """
    Displays a list of cars with their current push level and allows the user to pick one for editing.

    Args:
        car_list (list): A list of cars available for selection.

    Returns:
        int: The index of the car selected by the user.
    """

    car_num = 0
    for car in car_list:
        print(f'{car_num}\t{car}\tPush: {car.push_tire}')
        car_num += 1
    return int(input("Car number to edit: "))

def update_strategy(race_state):
    """
    Prompts the user to update the push level of a car in the race.

    Args:
        race_state (Race): The current state of the race.

    Returns:
        Race: The updated race state with the modified car strategy.
    """

    car_to_edit = pick_list(race_state.cars)
    push_level_update = int(input("Set push level 1/2/3/4/5 Conservative -> aggressive: "))
    race_state.cars[car_to_edit].edit_push(push_level_update)
    return race_state

def update_pit(race_state):
    """
    Prompts the user to send a car into the pit for a pit stop.

    Args:
        race_state (Race): The current state of the race.

    Returns:
        Race: The updated race state after the selected car performs a pit stop.
    """

    car_to_pit = pick_list(race_state.cars)
    race_state.cars[car_to_pit].pit_stop()
    return race_state

def update(race_state):
    """
    Updates the race state by printing the current lap, standings, and allowing the user to advance the race, 
    adjust car strategy, or initiate pit stops.

    Args:
        race_state (Race): The current state of the race.

    Returns:
        Race: The updated race state after user inputs and race progression.
    """

    print_lap(race_state)
    print_standings(race_state)
    user_input = None
    while user_input != "":
        user_input = input('Advance[ENTER], Stratagy[s], Pit[p], Quit[q]: ')
        match user_input:
            case 's': race_state = update_strategy(race_state)
            case 'p': race_state = update_pit(race_state)
            case 'q': exit(1)
            case '' : pass
            case _: print("Invalid Input")
    return race_state