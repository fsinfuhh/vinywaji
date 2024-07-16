"use strict";

// auto-initialize materialize components
document.onload = function () {
    M.AutoInit();
};

// submit all forms via JavaScript to prevent the browser from navigating to the api endpoint
document.querySelectorAll("form.js-submit")
    .forEach(form => form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const data = new FormData(event.target)
        await fetch(event.target.action, {
            method: event.target.method,
            body: data
        })

        form.reset()
        location.reload()
    }));

let mode = localStorage.theme ?? 'system';

function updateMode() {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }

    document.querySelector('#modeSwitch > [data-icon]').dataset.icon = mode;
}

updateMode();

function switchMode() {
    switch (mode) {
        case 'light':
            localStorage.theme = 'dark';
            mode = 'dark';
            break;
        case 'dark':
            localStorage.removeItem('theme')
            mode = 'system';
            break;
        case 'system':
            localStorage.theme = 'light';
            mode = 'light';
            break;
    }
    updateMode();
}

document.querySelector('#modeSwitch').addEventListener('click', (e) => {
    switchMode();
})
