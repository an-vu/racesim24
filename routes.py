""" Module to run the flask api """

import csv, random
from flask import Flask, render_template, jsonify, request, send_from_directory
from backend.car import Car
from backend.car_ai import AI
from backend.race import Race, restart

app = Flask(__name__,  template_folder="frontend/templates", static_folder="frontend/static" )


# Initialize the actual race instance
race = Race()
list_car_numbers = [] # Define global variable to store non-AI car numbers

@app.route('/favicon.ico')
def favicon():
    """Created to get rid of the favicon load error"""
    return send_from_directory(f"{app.static_folder}/images", 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/initialize_race', methods=['POST'])
def initialize_race():
    """ Function to start the race by adding AI cars and player cars """

    cars = []
    # Load AI cars from CSV
    with open("ai_car_info.csv", mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # Map row values to specific variables based on expected column order
            name = row[0]
            number = int(row[1])
            random_adjustment =  random.randint(1,30)/1000
            fast_lap_time = float(row[2]) + random_adjustment
            passing = float(row[3])
            defending = float(row[4])

            # Create AI car and add it to the list
            ai_car = AI(name, number, fast_lap_time, passing, defending, race, 3)
            cars.append(ai_car)

    data = request.json
    player1_name = data.get("player1_name")
    car1_number = data.get("car1_number")
    player2_name = data.get("player2_name")
    car2_number = data.get("car2_number")
    
    # Create Car instances based on input
    player_car_1 = Car(player1_name, car1_number, 30.5, 22.45, -10.65, race, 1)
    player_car_2 = Car(player2_name, car2_number, 30.5, 22.45, -10.65, race, 2)
    cars.append(player_car_1)
    cars.append(player_car_2)

    # Add all cars to the race
    for car in cars:
        race.add_car(car)
    global list_car_numbers
    list_car_numbers = [car.number for car in race.cars if not isinstance(car, AI)]

    return jsonify({"status": "success"}), 200

@app.route('/')
def setup():
    """
    Function to bring user to setup.html when navigating to the root directory webpage
    """
    return render_template('setup.html')

@app.route('/home')
def home():
    """
    Function to bring user to home.html when navigating to the home subdirectory webpage
    """
    restart_race()
    return render_template('home.html')

@app.route('/about')
def about():
    """
    Function to bring user to about.html when navigating to the about subdirectory webpage
    """
    return render_template('about.html')



# API route to get the current race state using the actual race object
@app.route('/api/race', methods=['GET'])
def get_race_state():
    """Return the current state of the race using the actual race object."""
    cars_data = []
    for car in race.cars:
        cars_data.append({
            "name": car.name,
            "number": car.number,
            "to_leader": car.to_leader,
            "total_race_time": car.total_race_time,
            "tire_life": car.tire_life,
            "fuel_level": car.fuel_level,
            "ai_or_player": car.ai_or_player,
            "push_tire": car.push_tire if not isinstance(car, AI) else None
        })

    # Sort cars_data by 'total_race_time'
    cars_data = sorted(cars_data, key=lambda car: car["total_race_time"])
    player_cars_data = sorted(cars_data, key=lambda car: car["ai_or_player"])

    return jsonify({
        "lap": race.lap,
        "lap_count": race.lap_count,
        "cars": cars_data,
        "player_cars_data": player_cars_data
    })

# API route to advance the race by one lap
@app.route('/api/race/lap', methods=['POST'])
def advance_lap():
    """Advance the race by one lap using the actual race object."""
    try:
        race.race_end()
        race.next_lap()  # This will trigger all cars to advance their race time
        return jsonify({"message": "Lap advanced", "lap": race.lap})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to update the push level of non-AI cars
@app.route('/api/race/strategy', methods=['POST'])
def update_push_level():
    """Update the push level (aggressiveness) of a non-AI car."""
    data = request.get_json()
    car_number = int(data.get('number'))
    push_level = int(data.get('push_level'))

    if not 1 <= push_level <= 5:
        return jsonify({"error": "Push level must be between 1 and 5"}), 400

    # Find the car by number and ensure it is not an AI car
    for carnum in list_car_numbers:
        if carnum == car_number and not isinstance(carnum, AI):
            try:
                car_to_push = next(carnum for carnum in race.cars if carnum.number == car_number)
                car_to_push.edit_push(push_level)
                return jsonify({"message": f"Car {car_number} push level updated to {push_level}"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return jsonify({"error": f"Car {car_number} not found or is an AI car"}), 404

# API route to simulate a pit stop for non-AI cars
@app.route('/api/race/pit', methods=['POST'])
def pit_stop():
    """Simulate a pit stop for a non-AI car."""
    data = request.get_json()
    car_number = int(data.get('number'))

    # Find the car by number and ensure it is not an AI car
    for carnum in list_car_numbers:
        if carnum == car_number and not isinstance(carnum, AI):
            try:
                # Find the car with this number
                car_to_pit = next(carnum for carnum in race.cars if carnum.number == car_number)

                # Call pit_stop() for the correct car
                car_to_pit.pit_stop()
                return jsonify({"message": f"Car {car_number} pitted successfully"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return jsonify({"error": f"Car {car_number} not found or is an AI car"}), 404

@app.route('/api/race/reset', methods=['POST'])
def restart_race():
    """
    API route to restart the race. This will call the restart function with the race instance.
    
    Returns:
        JSON response indicating success or failure of the restart operation.
    """
    try:
        # Call the standalone restart function and pass the race_state instance
        restart(race)
        return jsonify({"status": "success", "message": "Race restarted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/map', methods=['GET'])
def get_map():
    """
    API Route to pull the map data
    """
    try:
        return jsonify(race.lap_data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(404)
def page_not_found():
    """
    Function to display 404 error
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    