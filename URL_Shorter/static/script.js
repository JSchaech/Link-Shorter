function redirectToCustomURL() {
    var customURL = document.getElementsByName('uC_URL')[0].value;
    if (customURL.trim() !== "") {
        window.location.href = "/INFO/" + customURL;
        return false; // Prevent the form from submitting
    }
    return true; // Allow the form to submit if uC_URL is empty
}