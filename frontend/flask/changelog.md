# Nov 7 Changelog:

### New Files and Features:
- **setup.html**: Created a new player setup page with fields for profile picture, player name, and car number.
  - **Profile Picture Selection**: Added 6 images in `/static/images/profiles`. Clicking the profile picture circle will shuffle through these images.
  - **Player Info Input**: Added fields for Player Name and Car Number.
  - **Start the Race Button**: Navigates to `home.html` when clicked.

### File Updates:
- **routes.py**: 
  - Updated routes: the root (`/`) now points to `setup.html`, and `home.html` is accessed at `/home` (lines 46-52).
  
- **style.css**: 
  - Cleaned up and sorted out styling for a more consistent look across pages.
  
- **home.html**: 
  - Added JavaScript to retrieve and display player info from `setup.html`.
  - (Consider moving the growing script to `main.js` to keep `home.html` short and just html...)
  
- **base.html**: 
  - Minor adjustments to header and footer for improved alignment and uniformity.

---

## What's Next:
- Ensure player name and car number display correctly in `home.html`.
- Enable the "About" button functionality in `home.html`.
- Highlight Player 1 and Player 2 on the standings board for visibility.
- General cleanup to improve layout and visual consistency across pages.

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

footer for base.html

    <footer id="footer-sections" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; width: 100%; box-sizing: border-box;">
        <button id="nav-button" class="start-button" style="flex-shrink: 0;">About</button>
        <div class="footer-text" style="flex-grow: 1; text-align: center;">© NASCAR Manager '24</div>
        <button id="clock-button" class="clock" style="flex-shrink: 0;">⏳</button>
    </footer>