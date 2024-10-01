// function togglePrediction(element) {
//     const toggleShow = element.nextElementSibling;
//     // const icon = element.querySelector('.toggle i');
//     if (toggleShow.style.display === "block") {
//         toggleShow.style.display = "none";
//         rotation += 45; // Increase rotation by 45 degrees
//         box.style.transform = `rotate(${rotation}deg)`;
//     } else {
//         toggleShow.style.display = "block";
//     }
// }
let rotation = 0; // Initialize rotation angle

function togglePrediction(element) {
    const toggleShow = element.nextElementSibling;
    const icon = element.querySelector('.faq-icon');

    if (toggleShow.style.display === "block") {
        toggleShow.style.display = "none";
        icon.classList.remove('toggle-roted');

    } else {
        icon.classList.add('toggle-roted');
        toggleShow.style.display = "block";
    }
}
