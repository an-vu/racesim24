# Roadmap for NASCAR Manager '24

## v1.0 - **Public Release** ✅
- Initial release with core gameplay functionality.

---

## v1.1 - **JavaScript Cleanup** ✅
- Consolidate and organize JavaScript into `main.js`.
  - Move inline scripts from:
    - `setup.html`
    - `end.html`

---

## v1.2 - **Frontend Cleanup**
- Improve and finalize UI for:
  - `404.html`
  - `about.html`
  - `end.html`

---

## v1.3 - **Backend Cleanup**
- Reintroduce the **Player Car Number** feature for better customization.

---

## v1.4 - **Lap Controls**
- Add advanced lap-switching options:
  - **Go Back** to previous laps.
  - **Skip to Final Lap** button.
  - **Advance Lap x10** button for faster progression.

---

## v1.5 - **Stability Update**
- Refactor and optimize CI/CD pipelines.
- Finalize Docker configurations for seamless deployment.

---

## v1.6 - **Map Redesign**
- Revamp the race map to improve visuals and functionality.

---

## v1.7 - **Save/Load Feature**
- Introduce game save and load functionality to preserve player progress.

---

## v1.7 - **(QoL) and Miscellaneous Improvements**
- Code Organization and Optimization:
  - Refactor and modularize JavaScript:
    - Split main.js into smaller, page-specific files (home.js, setup.js, etc.).
    - Implement a build system (e.g., Webpack, Rollup) to compile and bundle files for improved performance in production.
  - Optimize CSS for consistency and maintainability.
- Enhanced Debugging:
  - Add detailed console logs for easier troubleshooting.
  - Include error-handling mechanisms for smoother user experience when API calls fail.
  - Display user-friendly error messages for common issues (e.g., missing inputs, connection errors).
- UI/UX Polish:
  - Improve mobile responsiveness across all pages.
- General Cleanup:
  - Remove unused assets, dead code, and redundant comments.
  - Streamline project structure.

---
