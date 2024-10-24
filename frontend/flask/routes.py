from flask import Flask, render_template, jsonify, request
from backend.car import Car
from backend.car_AI import AI
from backend.race import *

app = Flask(__name__)


# Initialize the actual race instance
race = Race()
cars = [
    Car("CHA", 1, 30.5, 22.45, -10.65, race),
    Car("LAR", 5, 30.5, 24.68, -6.72, race),
    AI("HAM", 11, 30.5, 23.42, -13.02, race),
    AI("LOG", 22, 30.5, 20, -20, race)
]
for car in cars:
    race.add_car(car)

# Define global variable to store non-AI car numbers
list_car_numbers = [car.number for car in race.cars if not isinstance(car, AI)]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
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
            "push_tire": car.push_tire if not isinstance(car, AI) else None  # Only for non-AI cars
        })
    
    # Sort cars_data by 'total_race_time'
    cars_data = sorted(cars_data, key=lambda car: car["total_race_time"])
    
    return jsonify({
        "lap": race.lap,
        "lap_count": race.lap_count,
        "cars": cars_data
    })

# API route to advance the race by one lap
@app.route('/api/race/lap', methods=['POST'])
def advance_lap():
    """Advance the race by one lap using the actual race object."""
    try:
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

    if not (1 <= push_level <= 5):
        return jsonify({"error": "Push level must be between 1 and 5"}), 400

    # Find the car by number and ensure it is not an AI car
    for car in list_car_numbers:
        if car == car_number and not isinstance(car, AI):
            try:
                car_to_push = next(car for car in race.cars if car.number == car_number)
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
    for car in list_car_numbers:
        if car == car_number and not isinstance(car, AI):
            try:
                # Find the car with this number
                car_to_pit = next(car for car in race.cars if car.number == car_number)

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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    