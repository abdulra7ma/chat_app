const socket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/'
);

var u1_selector = document.querySelector('.friends');
var wrapper_list_div = document.querySelector('.wrapper_list');
var hidden = "hidden";


socket.onopen = function (e) {
    send({
        "type": "on_open",
        "message": "connection established"
    })
    console.log("connection is opened");
};

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    users_constructor(data)

};

function pull_search_data() {
    var input = document.getElementById('myInput');
    // clean if the contracts panel if input is empty
    if (input.value === "") {
        var elms = document.querySelectorAll("[id='wrapper_id']");

        for (var i = 0; i < elms.length; i++){
            elms[i].remove()
        };

        if (u1_selector.classList.contains(hidden)) {
            u1_selector.classList.remove(hidden);
        };
    } else {
        wrapper_list_div.innerHTML = ""
        send({
            "type": "search",
            "input": input.value,
        });
    };
};

function send(data) {
    socket.send(
        JSON.stringify(data)
    );
};

function users_constructor(users_data) {
    if (!u1_selector.classList.contains(hidden)) {
        u1_selector.classList.add(hidden)
    };

    console.log(users_data)

    for (let i = 0; i < users_data.length; i++) {
        rapperHTML = user_constructor(users_data[i])
        wrapper_list_div.appendChild(rapperHTML)
    };
};

function user_constructor(user) {
    var wrapperHTML = document.createElement("div");
    var a_link = document.createElement("a");
    var li = document.createElement('li');
    var img = document.createElement('img');
    var div_main = document.createElement('div');
    var div_status = document.createElement('div');
    var div_info = document.createElement('div');
    var span = document.createElement('span');
    var special_id = user["id"]
    
    a_link.href = "/m/"+ user['username'] + "/";
    div_main.className = "d-flex bd-highlight";
    div_main.id = special_id
    
    div_status.classList.add("img_cont");
    img.src = "/media/" +  user['avatar_url'] + '/';
    img.className = "rounded-circle user_img";
    div_status.appendChild(img);
    div_main.appendChild(div_status);

    div_info.classList.add("user_info");
    span.innerText = user['username'];
    div_info.appendChild(span);
    div_main.appendChild(div_info);
    
    li.appendChild(div_main);
    a_link.appendChild(li);
    a_link.id = "wrapper_id"
    wrapperHTML.appendChild(a_link)
    
    return wrapperHTML;
};

socket.onclose = function (e) {
    console.log("WebSocket is closed now.");
};