var dropdown = document.getElementsByClassName("dropdown-btn");
var modal = document.getElementById('id01');
var i;

for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    });
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}