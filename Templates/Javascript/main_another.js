function togglePrediction(element) {
    const toggleShow = element.nextElementSibling;
    if (toggleShow.style.display === "block") {
        toggleShow.style.display = "none";
    } else {
        toggleShow.style.display = "block";
    }
}
