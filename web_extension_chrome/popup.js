$(document).ready(function(){

    // Get the currently active tab
    async function getActiveTab(){
        const tabs = await chrome.tabs.query({currentWindow: true, active: true});
        return tabs[0];
    }

    const container = $('#popup-main');
    let activePromptId;

    // async: Load the main content of the popup by using the user's search query to interact with the web API
    (async () => {
        const activeTab = await getActiveTab();
        const queryParameters = activeTab.url.split('?')[1];
        const urlParameters = new URLSearchParams(queryParameters);
        const userSearchQuery = urlParameters.get('q');

        // If on a valid Google search results page
        if (activeTab.url.includes('google.com/search') && userSearchQuery) {
            container.html(`<div id="searchquery">You searched for:<br><strong>${userSearchQuery}</strong></div>`);

            // Get the prompt via AJAX based on user's search query
            $.get(`${apiUrlPromptGet}?user_search_query=${userSearchQuery}`, function(data){
                // Define prompt object
                let prompt = data.prompt;
                // If a valid prompt was found then display it
                if (prompt){
                    activePromptId = prompt.id;
                    // Build HTML
                    let htmlToInject = `
                    <div id="prompt">
                        <div id="prompt-topic">
                            Your search appears to be related to a research topic that we're interested in:
                            <strong>${prompt.topic}</strong>
                        </div>
                        <div id="prompt-content">
                            ${prompt.prompt_content}
                        </div>
                    </div>`;
                    // Add response
                    if (prompt.response_required){
                        htmlToInject += `
                        <div id="response">
                            <textarea id="response-content" placeholder="Type your response here..." required></textarea>
                            <button id="response-post-button">Submit response</button>
                        </div>`;
                    }
                    // Inject HTML
                    container.append(htmlToInject);
                }
                // If a valid prompt was NOT found then show helpful message to user
                else {
                    container.append(`
                        <p>Your search doesn't appear to be related to our current research interests.</p>
                        <p>Please try adjusting your search or contact us for further support.</p>
                    `);
                }
            }).fail(function(){
                // If the get request fails, display an appropriate message to user
                container.append(`
                    <p>There's been an error when trying to connect to the server.</p>
                    <p>Please try again or contact us for support if the problem persists.</p>
                `);
            });

        }
        // If not on a valid Google search results page
        else {
            container.html(`
                <p>You're not currently on a Google search results page.</p>
                <p>To use this extension please perform a <a href="https://www.google.com" target="_blank">Google search</a> and then load this extension again.</p>`
            );
        }
    })();

    // User clicks the response post button: sends response to API
    $('body').on('click', '#response-post-button', function(){
        let responseContent = $('#response-content').val();
        if (responseContent.length > 0){
            // Post the response
            $.post(apiUrlPromptPost, {user_response_content: responseContent, active_prompt_id: activePromptId}, function(data, status){
                if (data.response_saved == 1){
                    container.html('<div id="response-post-success">Your response has been successfully posted!</div><button id="response-post-finished-button">Finished</button>');
                }
                else {
                    container.html('<div id="response-post-failed">Error: Your post was not saved successfully. Please try again or contact us for further support.');
                }
            }).fail(function(){
                // If the post request fails, display an appropriate message to user
                container.append(`
                    <p>There's been an error when trying to send your response to the server.</p>
                    <p>Please try again or contact us for support if the problem persists.</p>
                `);
            });
        }
    });

    // User clicks the finished button: close pop up
    $('body').on('click', '#response-post-finished-button', function(){
        window.close();
    });
});