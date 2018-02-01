function updateReaction() {
    var request = new XMLHttpRequest();
    request.addEventListener('load', displayEmotion);
    request.open('GET', '/ask?post=' + postInput.value);
    request.send();
}

function displayDefaultIcon() {
    loadingAnimationIsDisplayed = false;
    reactionOutput.innerHTML = '❔';
}

function displayLoadingAnimation() {
    if (loadingAnimationIsDisplayed) return;

    reactionOutput.innerHTML = `
        <div class="spinner">
            <div class="rect1"></div>
            <div class="rect2"></div>
            <div class="rect3"></div>
            <div class="rect4"></div>
            <div class="rect5"></div>
        </div>`;
    loadingAnimationIsDisplayed = true;
}

function displayEmotion() {
    loadingAnimationIsDisplayed = false;
    const response = JSON.parse(this.responseText)
    if (response == 'joy') {
        reactionOutput.innerHTML = '😊';
    } else if (response == 'surprise') {
        reactionOutput.innerHTML = '😯';
    } else if (response == 'sadness') {
        reactionOutput.innerHTML = '😢';
    } else if (response == 'anger') {
        reactionOutput.innerHTML = '😡';
    } else {
        reactionOutput.innerHTML = '❓';
    }
}

function handleKeyEvent() {
    // Avoid requesting the same value multiple times
    if (postInput.value == lastEnteredText) return;

    // Clear the timeout if it was set
    clearTimeout(timeout);

    if(postInput.value == '') {
        // Display default icon at the end of the post
        // input if no text was entered
        displayDefaultIcon();
        return;
    }
    
    lastEnteredText = postInput.value;
    // Display a loading animation while the 
    // user is typing
    displayLoadingAnimation();
    // Register a new timeout to detect whether the
    // user stopped typing
    timeout = setTimeout(updateReaction, 800);
}

// Get the input and output elements
var postInput = document.getElementById('post');
var reactionOutput = document.getElementById('reaction');

// Initialize a variable to save the value on which
// the last timeout was registered
var lastEnteredText = '';

var loadingAnimationIsDisplayed = false;

// Initialize a timeout variable
var timeout = null;

// Listen for keystroke events
postInput.onkeyup = handleKeyEvent;