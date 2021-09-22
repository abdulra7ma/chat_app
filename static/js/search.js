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
    console.log(input.value);
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

function myFunction() {
    console.log("inside the myFunction()")

}

function send(data) {
    socket.send(
        JSON.stringify(data)
    )
}