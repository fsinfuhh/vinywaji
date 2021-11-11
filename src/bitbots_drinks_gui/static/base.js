"use strict";

// auto-initialize materialize components
document.onload = function () {
    M.AutoInit();
};

// submit all forms via JavaScript to prevent the browser from navigating to the api endpoint
document.querySelector("form.js-submit").addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = new FormData(event.target)
    await fetch(event.target.action, {
        method: event.target.method,
        body: data
    })

    location.reload()
});
