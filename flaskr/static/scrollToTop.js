    // When the user scrolls down 20px from the top of the document, show the button    
function scrollFunction() {
    if (document.body.scrollTop > 49 || document.documentElement.scrollTop > 49) {
        document.getElementById("top").style.display = "block";
    } else {
        document.getElementById("top").style.display = "none";
    }
}

window.onscroll = function () { scrollFunction(); };

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
        document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}