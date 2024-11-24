# Nov 24 Changelog

### File Updates:
- Moved `favicon.ico` to /frontend/static/images/
- Added 2 new profile pictures

**`main.js`**:

**`home.html`**:


**`routes.py`**:
- Cleaned up and moved some functions around for better readability.
- Added a shebang line.

**`style.css`**:
- Cleaned up a bunch:
  - class `.box` is now `.card`


---

### Known Issues:
- **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

---

### Next Updates:
- Get map added and working
- Highlight Player 1 and Player 2 on the standings board for better visibility.
- Continue general layout and visual cleanup for consistency across pages.
- Finalize designs for `about.html` and `404.html`.
- Add support for dark mode/theme options.

---

# Nov 21 Changelog
### File Updates:
 **main.js**: Fixed player pit functions and stat updates


# Nov 19 Changelog

- TLDR: Small update resizing the home screen layout to 80% and moving the "Advance Lap" and "Reset" buttons to the Player Control Center column.

### File Updates:
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

---

### Known Issues:
- **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

---

### Next Updates:
- Get map added and working
- Highlight Player 1 and Player 2 on the standings board for better visibility.
- Continue general layout and visual cleanup for consistency across pages.
- Finalize designs for `about.html` and `404.html`.
- Add support for dark mode/theme options.

---

# Nov 13 Changelog

### New Files and Features
- **.gitignore**: Re-added and will ignore all future cache files to clean repo

### File Updates:
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

---

### Known Issues:
- **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).

---

### Next Updates:
- Highlight Player 1 and Player 2 on the standings board for better visibility.
- Continue general layout and visual cleanup for consistency across pages.
- Finalize designs for `about.html` and `404.html`.
- Add support for dark mode/theme options.

---

# Nov 10 Changelog

### New Files and Features:
- **setup.html**: Introduced a new player setup page with fields for selecting a profile picture, entering player name, and specifying car number.
  - **Profile Picture Selection**: Added six images in `/static/images/profiles` for player selection. Clicking the profile picture cycles through these images.
  - **Player Info Input**: Added input fields for **Player Name** and **Car Number**.
  - **Start the Race Button**: Navigates to `home.html` upon clicking, launching the main game interface.

### File Updates:
- **routes.py**: 
  - Updated route mappings: the root path (`/`) now serves `setup.html`, and `home.html` is accessible at `/home` (see lines 46-52 for reference).

- **style.css**: 
  - Cleaned up and organized styles for a more consistent look across all pages.

- **home.html**: 
  - Integrated JavaScript to retrieve and display player data from `setup.html`.
  - Moved JavaScript functions from `home.html` to `main.js` for better code management.

- **base.html**: 
  - Refined header and footer for improved alignment and uniformity.
  - The "About" button is now functional, linking to `about.html`.

---

### Known Issues:
- **Display Issue on Smaller Screens**: `home.html` layout issues on smaller display devices (e.g., 13" MacBook).
- **Profile Sync Issue**: Player profile pictures and information fail to sync correctly between `setup.html` and `home.html`: Player 1’s profile picture appearing in Player 2’s control center.

---

### Next Updates:
- Make sure player name and car number display accurately in `home.html`.
- Highlight Player 1 and Player 2 on the standings board for better visibility.
- Continue general layout and visual cleanup for consistency across pages.
- Finalize designs for `about.html` and `404.html`.
- Add support for dark mode/theme options.

---


# Approach for player setup

## Phase 1: Build the visual layout and input fields in setup.html (no back-end changes needed yet).

## Phase 2: Plan data flow and set up a form submission that passes data to the back end.

## Phase 3: Add basic backend logic in routes.py to handle and store player info, then update home.html to display this data.


# Planned Universal Classes and Their Placement

## Headers & Subheaders:
.main-title (for primary headers, like page titles): Replace inline header styles in setup.html, home.html, and base.html.
.sub-title (for subtitles): Use in areas like the update message in home.html and player titles in setup.html.

## Containers:
.content: Central container that centers content, used across pages. Ensures vertical and horizontal alignment.
.box: Core styling for any container (background color, padding, border radius, shadow). Use for player setup boxes, standings, and control centers.
.box-large and .box-small can be subclasses of .box for resizing.
.centered-container: Apply in base.html and .content divs to centralize content across the entire viewport.

## Buttons:
.button: Base button style for uniform padding, border-radius.
.button-primary, .button-danger for different actions (e.g., start race, reset).
Replace inline button styles for the "Start Race" and pit/reset buttons in home.html and setup.html.

## Profile Picture Placeholder:
.profile-picture: Standardize for the circular image placeholder. This ensures it’s easy to customize if you change image sizes or colors across themes.

## Table:
.standings-table: For tables in home.html, using .standings-table ensures a consistent look.
Add header and cell styles for alignment, border-bottom, padding, etc., so each page with tables will follow the same setup.

## Input Fields:
.input-field: Standardize for text and number input styling in setup.html. It replaces the inline input styles with a class for consistent padding, border, and radius.