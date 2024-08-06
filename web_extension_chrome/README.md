# README - Ethical Interface: Web Browser Extension (Chrome)

This document provides information for technical staff working on the Ethical Interface web browser extension (for Google Chrome).

To learn about developing Chrome web extensions see: <https://developer.chrome.com/docs/extensions>

## Getting Started

+ See local_settings.example.js for instructions about creating a local_settings.js file, which is critical to the extension operating properly.
+ Running the extension:
    + Development:
        + Go to <chrome://extensions/> in your Chrome web browser
        + Enable 'Developer Mode'
        + Click 'Load unpacked' button and select this web extension directory
    + Live: find the extension the Chrome Web Store: <https://chromewebstore.google.com/>


## Code Structure

This extension follows a conventional structure, e.g.:

+ manifest.json - the core of the project
+ popup.html - the HTML content that appears in the popup box when user clicks on extension icon
+ popup.css - the styling for the popup box content
+ popup.js - the functionality within the popup, e.g. interacting with the web API
+ icon.png - the 

Additionally to above conventional files, this extension also has:

+ jquery-[version].min.js - used within popup.js
+ local_settings.js - values that are specific to the local environment and must be customised in each environment
+ local_settings.example.js - used to help developer create local_settings.js (as it's ignored from git)
