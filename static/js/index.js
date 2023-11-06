console.log("Sanity check from index.js.");

const userName = JSON.parse(document.getElementById('userName').textContent);

// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

document.querySelector("#logout").onclick = function() {
    window.location.pathname = "login/login/";
}

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        document.querySelector("#roomConnect").click();
    }
};

// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function() {
    let roomName = document.querySelector("#roomInput").value;
    window.localStorage.setItem("userName", userName);
    window.location.pathname = "room/" + roomName + "/" + userName + "/";
}

// redirect to '/room/<roomSelect>/'
document.querySelector("#roomSelect").onchange = function() {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "room/" + roomName + "/" + userName +  "/";
}
