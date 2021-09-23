const socket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/'
);

function pull_search_data() {
    var input = document.getElementById('myInput');
    send({
        "type": "search",
        "input": input.value,
    });
    u1_selector = document.querySelector('.contacts');
    console.log(u1_selector)
    // console.log(input.value);
};

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)

};

socket.onopen = function (e) {
    send({
        "type": "on_open",
        "message": "connection established"
    })
    console.log("connection is opened");
};

socket.onclose = function (e) {
    console.log("WebSocket is closed now.");
};

function send(data) {
    socket.send(
        JSON.stringify(data)
    );
};

function users_constructor(users_data) {
    for (let i = 0; i < users_data.length; i++) {
        console.log(i)
    };
};