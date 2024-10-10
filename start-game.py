from backend import race
from frontend import text_GUI as GUI

def main():
    race_state = race.start()
    while not race_state.race_end():
        race_state = GUI.update(race_state) 
        race_state.next_lap()

    return True

if __name__ == "__main__":
    main()
