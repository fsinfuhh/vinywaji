"use strict";

document.querySelector("form#purchase").addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = new FormData(event.target)
    await fetch(event.target.action, {
        method: "POST",
        body: data
    })

    location.reload()
});
