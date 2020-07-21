const toggleButtons = document.querySelectorAll(".toggleDisplay");

function toggleDisplay(e) {
    const tbody = document.querySelector("."+e.target.value)
    e.target.classList.toggle("minus")
    if (tbody.style.display === "table-row-group") {
        tbody.style.display = "none";
    } else {
        tbody.style.display = "table-row-group";
    }
}

toggleButtons.forEach(function(toggleButton) {
    toggleButton.addEventListener('click', toggleDisplay);
})
