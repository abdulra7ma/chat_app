document.getElementById('video-button').addEventListener("click", function() {
    hide_card();
    generate_HTML_call();
});

function hide_card() {
    document.getElementsByClassName('card-header')[1].style.display = "none";
    document.getElementsByClassName('card-body')[1].style.display = "none";
    document.getElementsByClassName('card-footer')[1].style.display = "none";
};

function generate_HTML_call(image_src) {
    if (!image_src) {
        image_src = 'https://placeimg.com/400/400/people'
    }

    card_class = document.getElementById("dfgchvbjnm")
    card_class.innerHTML += '<div class="call-animation"> <img class="img-circle" src="' + image_src + '" alt="" width="135"/> </div>'
    card_class.style.cssText = "display: flex; justify-content: center;align-items:center"
}