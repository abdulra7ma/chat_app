const user_username = JSON.parse(document.getElementById('user_username').textContent);
const reciever_username = JSON.parse(document.getElementById('reciever').textContent);
var num = 0


const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/messanger/' +
    reciever_username +
    '/'
);

var input = document.getElementById("input");
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("submit").click();
    }
});

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'username': user_username,
        'message': message,
    }));
    messageInputDom.value = '';
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data['visit'])
    createMessage(data);

}

chatSocket.onopen = function (e) {
    chatSocket.send(JSON.stringify({
        'command': 'fetch_messages',
        'user_live': true,
        'username': user_username
    }));
}

chatSocket.onclose = function (e) {
    console.log("WebSocket is closed now.");
}

function createMessage(data) {
    if (data['command'] === 'new_message') {
        message = data['message']['content']
        if (data.message.author === user_username) {
            var generatedHTML = htmlConstractor(message, 'start')
        } else {
            var generatedHTML = htmlConstractor(message, 'end')
            // var generatedHTML = '<div class="d-flex justify-content-end mb-4"> <div class="msg_cotainer_send"> '+ data.message + '<span class="msg_time_send">8:55 AM, Today</span></div> <div class="img_cont_msg"> <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg"></div></div>'
        }
        document.getElementById('card-body').innerHTML += generatedHTML
    } else if (data['command'] === 'messages') {
        console.log(data)
        if (data['sender'] === user_username){
            messages = data['messages']
            for (let i = 0; i<messages.length; i++){
                if (messages[i].author === user_username) {
                    var generatedHTML = htmlConstractor(messages[i].content, 'start')
                } else {
                    var generatedHTML = htmlConstractor(messages[i].content, 'end')
                }
                document.getElementById('card-body').innerHTML += generatedHTML
            }
        }
        
    }
}

function htmlConstractor(message, message_class) {
    var generatedHTML = '<div class="d-flex justify-content-' + message_class + ' mb-4"> <div class="img_cont_msg"> <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg"> </div> <div class="msg_cotainer">' + message + ' </div> </div>';
    return generatedHTML;
}
