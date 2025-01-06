$(document).ready(function(){

    // Get the currently active tab
    async function getActiveTab(){
        const tabs = await chrome.tabs.query({currentWindow: true, active: true});
        return tabs[0];
    }

    const container = $('#popup-main');
    let activePromptId;
    let userSearchQuery;
    let searchExact = 0;
    let topicsExclude = '';

    // async: Load the main content of the popup by using the user's search query to interact with the web API
    function loadMainContent(){
        (async () => {
            const activeTab = await getActiveTab();
            const queryParameters = activeTab.url.split('?')[1];
            const urlParameters = new URLSearchParams(queryParameters);
            userSearchQuery = urlParameters.get('q');

            // If on a valid Google search results page
            if (activeTab.url.includes('google.com/search') && userSearchQuery) {
                container.html(`<div id="searchquery">You searched for:<br><strong>${userSearchQuery}</strong></div>`);

                // Get the prompt via AJAX based on user's search query
                $.get(`${apiUrlPromptGet}?user_search_query=${userSearchQuery}&search_exact=${searchExact}&topics_exclude=${topicsExclude}`, function(data){
                    let prompt = data.prompt;
                    let htmlToInject = '';
                    // If a valid prompt was found then display it
                    if (prompt){
                        activePromptId = prompt.id;
                        // Build HTML
                        htmlToInject += `
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
                    }
                    // If a valid prompt was NOT found then show helpful message to user
                    else {
                        htmlToInject += `
                            <p>Your search doesn't appear to be related to our current research interests.</p>
                            <p>Please try adjusting your search or contact us for further support.</p>
                        `;
                    }
                    // Add content for allowing user to take action if search isn't relevant
                    // User can try again by doing an exact search or create a report
                    htmlToInject += `
                    <div id="notrelevanttoggle">Result not relevant?</div>
                    <div id="notrelevant">
                        <p>
                            If this information shown above isn't relevant to your search, please try <span id="notrelevant-exactsearch">reloading with an exact search match</span>.
                        </p>
                        <p>
                            You can also try limiting which topics are included. Untick a topic and click Reload to try again without these topics:`;
                            for (var i = 0; i < data.topics.length; i++){
                                let topic = data.topics[i];
                                let checked = ' checked';
                                if (topic['excluded'] == 1) checked = ''
                                htmlToInject += `<div class="notrelevant-topic">
                                    <input type="checkbox" id="topic-${topic['id']}" name="includetopic" value="${topic['id']}"${checked}>
                                    <label for="topic-${topic['id']}"> ${topic['name']}</label>
                                </div>`;
                            }
                            htmlToInject += `
                            <button id="notrelevant-topic-reload">Reload</button>
                        </p>
                        <p>
                            If the information shown still isn't relevant to your search, please <span id="notrelevant-report">report this to us</span> so that we can work to improve the accuracy of this tool.
                        </p>
                    </div>`;
                    // Inject HTML
                    container.append(htmlToInject);
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
    }
    // Load content on popup start
    loadMainContent();

    // User clicks "not relevant" exact search button:
    // Reloads search using 'exact search' that will only match the entire search term, not words within it
    $('body').on('click', '#notrelevanttoggle', function(){
        $('#notrelevant').toggle();
    });

    // User clicks "not relevant" exact search button:
    // Reloads search using 'exact search' that will only match the entire search term, not words within it
    $('body').on('click', '#notrelevant-exactsearch', function(){
        searchExact = 1;
        loadMainContent();
    });

    // User clicks the "not relevant" topic reload button:
    // Reloads search and excludes any unticked topics
    $('body').on('click', '#notrelevant-topic-reload', function(){
        topicsExclude = $(".notrelevant-topic input:checkbox:not(:checked)").map(function(){return $(this).val();}).get().join(',');
        loadMainContent();
    });

    // User clicks the "not relevant" report post button:
    // Sends report to API
    $('body').on('click', '#notrelevant-report', function(){
        $.post(apiUrlNotRelevantReportPost, {user_search_query: userSearchQuery, active_prompt_id: activePromptId}, function(data, status){
            if (data.report_saved == 1){
                container.html('<div id="report-post-success">Thank you, your report has been successfully sent to us and will be used to improve the product.<br>Please contact us if you would like to provide further feedback</div><button class="btn-close">Finished</button>');
            }
            else {
                container.html('<div id="report-post-failed">Error: Your report was not sent successfully. Please try again or contact us for further support.');
            }
        }).fail(function(){
            // If the post request fails, display an appropriate message to user
            container.append(`
                <p>There's been an error when trying to send your report to the server.</p>
                <p>Please try again or contact us for support if the problem persists.</p>
            `);
        });
    });

    // User clicks the response post button:
    // Sends response to API
    $('body').on('click', '#response-post-button', function(){
        let responseContent = $('#response-content').val();
        if (responseContent.length > 0){
            // Post the response
            $.post(apiUrlResponsePost, {user_response_content: responseContent, active_prompt_id: activePromptId}, function(data, status){
                if (data.response_saved == 1){
                    container.html('<div id="response-post-success">Your response has been successfully posted!</div><button class="btn-close">Finished</button>');
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

    // User clicks the finished button:
    // Closes pop up
    $('body').on('click', '.btn-close', function(){
        window.close();
    });
});