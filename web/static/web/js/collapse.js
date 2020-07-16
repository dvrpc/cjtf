const toggleButtons = document.querySelectorAll(".toggleDisplay");

function toggleDisplay(e) {
    const rowsToToggle = document.querySelectorAll("."+e.target.value)
    rowsToToggle.forEach(function(row) {
        e.target.classList.toggle("minus")
        if (row.style.display === "block") {
            row.style.display = "none";
        } else {
            row.style.display = "block";
        }
    })
}

toggleButtons.forEach(function(toggleButton) {
    toggleButton.addEventListener('click', toggleDisplay);
})
