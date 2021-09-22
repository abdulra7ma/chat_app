const user_username = JSON.parse(document.getElementById('user_username').textContent);
const reciever_username = JSON.parse(document.getElementById('reciever').textContent);
const sender_avatar_url = JSON.parse(document.getElementById('sender_avatar_url').textContent);
const reciever_avatar_url = JSON.parse(document.getElementById('reciever_avatar_url').textContent);

var num = 0;


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
    if (message.length > 0) {
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'username': user_username,
            'message': message,
        }));
    };  
    messageInputDom.value = '';
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
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
        }
        document.getElementById('card-body').innerHTML += generatedHTML
    } else if (data['command'] === 'messages') {

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
    if (message_class === 'start'){
        var generatedHTML = '<div class="d-flex justify-content-' + message_class + ' mb-4"> <div class="img_cont_msg"> <img src="'+ sender_avatar_url +'" class="rounded-circle user_img_msg"> </div> <div class="msg_cotainer">' + message + ' </div> </div>';
    } else {
        var generatedHTML = '<div class="d-flex justify-content-end mb-4"> <div class="msg_cotainer_send"> '+ message + '</div> <div class="img_cont_msg"> <img src="'+ reciever_avatar_url +'" class="rounded-circle user_img_msg"></div></div>'
    }
    return generatedHTML;
}
