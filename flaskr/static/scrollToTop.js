    // When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () { scrollFunction();};
    
function scrollFunction() {
    if (document.body.scrollTop > 49 || document.documentElement.scrollTop > 49) {
        document.getElementById("top").style.display = "block";
    } else {
        document.getElementById("top").style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
        document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}