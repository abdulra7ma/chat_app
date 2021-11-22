document.getElementById('video-button').addEventListener("click", function() {
    hide_card();
});

function hide_card() {
    document.getElementsByClassName('card-header')[1].style.display = "none";
    document.getElementsByClassName('card-body')[1].style.display = "none";
    document.getElementsByClassName('card-footer')[1].style.display = "none";
};