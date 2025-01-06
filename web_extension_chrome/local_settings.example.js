/*
local_settings.js is ignored from git, so will need to be created.

Actions:
1. Make a copy of local_settings.example.js
2. Call the copied file local_settings.js
3. Customise the values according to your environment (e.g. dev, live).

Don't change the const names as these are used elsewhere in the extension.
*/

// Provide the URLs for the API request (used in popup.js to get/post data from/to the API)
const apiUrl = 'http://localhost:8001';
const apiUrlPromptGet = `${apiUrl}/data/prompt/get/`;
const apiUrlResponsePost = `${apiUrl}/data/response/post/`;
const apiUrlNotRelevantReportPost = `${apiUrl}/data/notrelevantreport/post/`;
