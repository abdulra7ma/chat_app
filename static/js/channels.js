const user_username = JSON.parse(document.getElementById('user_username').textContent);
const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

var input = document.getElementById("input");
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        document.querySelector('#submit').click();
    };
});

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': user_username,
    }));
    messageInputDom.value = '';
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    document.querySelector('#chat-text').value += (data.username + ': ' + data.message + '\n')
};

function closeConnection() {
    console.log("user is disconnected");
    chatSocket.onclose = function (event) {
        console.log("user is disconnected");
        const message = 'have disconnected.'
        chatSocket.send(JSON.stringify({
            'message': message,
            'username': user_username
        }));
    }
};

