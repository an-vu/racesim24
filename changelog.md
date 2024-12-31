# Dec 31 Changelog

- Ported to Github
- Added roadmap.md
- Added profile.psd to frontend/images/

---
# Dec 11 Changelog

**`setup.html`**:
- Added a hint line.

**`home.html`**:
- Added some new buttons.

---
# Dec 9 Changelog

**`race.py`**:
  - Added crash mechanics via two functions, 5% chance each lap a crash could happen.

**`test_race.py`**:
  - Added test for new crash mechanics

**`requirements.txt`**:
  - Added pytest-mock

---
# Dec 8 Changelog

## File Updates:

**`home.html`**:
  - Moved Map card to the middle
  - Edited About card
  - Gitlab Button in About card works now, will take to the project page of course
  - Aligned Pit button to the center of Player Control card

**`about.html`**:
  - Started on redesigning the whole thing...

---
# Dec 6 Changelog

## TLDR:
  - Public release for new UI.
  - Make sure new UI works properly with Dec 4 Update.
  - **New UI now works with big screen and small screen.** Fuck yea!

## File Updates:

**`end.html`**:
  - Updated to match with the new UI style.


## Known Issues:
  - Map doesn't work anymore...

---
# Dec 4 Changelog

**race.py**: Added starting_gaps to restart() function

**main.js**: Changed player car update functions to use player car numbers instead of index in list

**end.html**: Added base.html blocking to have the file use the same css

## Next Updates:
  - An's GUI update
  - End standings javascript

---
# Dec 1 Changelog

## File Updates:

**car.py**: Removed reset_for_race, unused.

**race.py**: 
  - Removed test print statements
  - adjusted restart() to set the race.cars to empty list
  - removed need for reset_for_race

**main.js**:
  - added logic to test for race_end
  - added endRace()
  - resetRace() now brings user back to '/'
  - added message for pit stop
  - removed testing console.log statements
  - removed unused resetStrategySelections
  - removed player car numbers

**end.html**: added file with basic info

**setup.html**: 
  - removed player car number inputs
  - added error handling for no names entered

**routes.py**: 
  - hard coded in player numbers as 2 and 3
  - removed race_reset on loading of home.html
  - added /end route

## Next Updates:
  - Get map added and working
  - Highlight Player 1 and Player 2 on the standings board for better visibility.
  - Continue general layout and visual cleanup for consistency across pages.
  - Finalize designs for `about.html` and `404.html`.
  - Add support for dark mode/theme options.

---
# Nov 27 Changelog

  - This big ass update brings a whole new look to the simulation: glassmorphism, 3d vision pro vibe,... you name it our project looks 3024 now.
  - It also fixes the display issue with smaller screen   - now it does work on my 13 inch macbook pro now fuck yeah!
  - It also comes with some new bugs... for sum reason html and javascript kinda glitchy right now... example if we got this element <bold>car</bold> it doesnt render as bold anymore... something happening and i dont know what is happening...

## File Updates:
**`/frontend/static/images/profiles`**:
  - Added 6 new profile pictures.

**`style.css`**:
  - Cleaned up, change classes names, this .css is now 90% new.

**`404.html`**:
  - Redesigned the whole page

## Known Issues:
  - yo why tf the js scripts in `setup.html` stop working when moved to `main.js`...
  - Returning to the setup page and changing input values does not update the displayed values in the game interface. This issue seems related to the recent changes in the `setup.html` structure, including the removal of the required attribute and the introduction of floating labels. The backend or JavaScript may be reusing previously stored values instead of capturing the updated inputs.

---
# Nov 24 Changelog

## File Updates:
  - Moved `favicon.ico` to /frontend/static/images/

**`home.html`**:
  - Updated the layout a bit...

**`setup.html`**:
  - Updated to follow `base.html` rules.

**`routes.py`**:
  - Cleaned up and moved some functions around for better readability.
  - Added shebang line.

**`style.css`**:
  - Cleaned up a bunch, removed unused classes, polished some elements etc etc...

## Known Issues:
  - **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

## Next Updates:
  - Get map added and working
  - Highlight Player 1 and Player 2 on the standings board for better visibility.
  - Continue general layout and visual cleanup for consistency across pages.
  - Finalize designs for `about.html` and `404.html`.
  - Add support for dark mode/theme options.
  - Update map?
  - Add race ending stuff

---
# Nov 21 Changelog

## File Updates:
**main.js**: Fixed player pit functions and stat updates

---
# Nov 19 Changelog

  - TLDR: Small update resizing the home screen layout to 80% and moving the "Advance Lap" and "Reset" buttons to the Player Control Center column.

## File Updates:
**car.py**: Added lap time calculations

**race.py**:
  - Fixed dirty air, swapped updates_needed from list to dictionary
  - Added map_helper method, creates dictionary for use for map building

**main.js**: created updateMap() function, updates elements on home.html

**home.html**:
  - Created rudimentary map elements
  - Moved Reset and Advance Lap buttons to the Control Center columns
  - Game Layout is now `.home-container` class

**routes.py**: /api/map route created, pulls race.lap_data

**style.css**:
  - Created .track_cars styling for track
  - Added `.home-container` class: scaled down to 80% for smaller screen

## Known Issues:
  - **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

## Next Updates:
  - Get map added and working
  - Highlight Player 1 and Player 2 on the standings board for better visibility.
  - Continue general layout and visual cleanup for consistency across pages.
  - Finalize designs for `about.html` and `404.html`.
  - Add support for dark mode/theme options.

---
# Nov 13 Changelog

## New Files and Features
**.gitignore**:
  - Re-added and will ignore all future cache files to clean repo

## File Updates:
**car_AI.py -> car_ai.py**: Renamed for valid snake_case and cleaned up via linter
**car.py**: Cleaned up via linter
**race.py**: Cleaned up via linter, removed unused import
**routes.py**:
  - Moved to root directory to clean imports, didn't make sense to have in the frontend
  - Cleanded via linter, 
  - added static and templates references
  - added favicon.ico route
  - removed static player names and numbers
  - added initialize_race route to get player names and numbers and start race
**test_race.py**: Cleaned up via linter
**Dockerfile**: Updated reference to routes.py
**setup.html**: Fixed script to update player names and numbers

## Known Issues:
  - **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

## Next Updates:
  - Highlight Player 1 and Player 2 on the standings board for better visibility.
  - Continue general layout and visual cleanup for consistency across pages.
  - Finalize designs for `about.html` and `404.html`.
  - Add support for dark mode/theme options.

---
# Nov 10 Changelog

## New Files and Features:
**setup.html**: Introduced a new player setup page with fields for selecting a profile picture, entering player name, and specifying car number.
**Profile Picture Selection**: Added six images in `/static/images/profiles` for player selection. Clicking the profile picture cycles through these images.
**Player Info Input**: Added input fields for **Player Name** and **Car Number**.
**Start the Race Button**: Navigates to `home.html` upon clicking, launching the main game interface.

## File Updates:
**routes.py**: 
  - Updated route mappings: the root path (`/`) now serves `setup.html`, and `home.html` is accessible at `/home` (see lines 46-52 for reference).

**style.css**: 
  - Cleaned up and organized styles for a more consistent look across all pages.

**home.html**: 
  - Integrated JavaScript to retrieve and display player data from `setup.html`.
  - Moved JavaScript functions from `home.html` to `main.js` for better code management.

**base.html**: 
  - Refined header and footer for improved alignment and uniformity.
  - The "About" button is now functional, linking to `about.html`.

## Known Issues:
**Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).
**Profile Sync Issue**: Player profile pictures and information fail to sync correctly between `setup.html` and `home.html`: Player 1’s profile picture appearing in Player 2’s control center.

## Next Updates:
  - Make sure player name and car number display accurately in `home.html`.
  - Highlight Player 1 and Player 2 on the standings board for better visibility.
  - Continue general layout and visual cleanup for consistency across pages.
  - Finalize designs for `about.html` and `404.html`.
  - Add support for dark mode/theme options.
