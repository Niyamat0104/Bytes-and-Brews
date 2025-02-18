const scrollContainer = document.getElementById("recommendScroll");
const leftButton = document.querySelector(".scroll-left");
const rightButton = document.querySelector(".scroll-right");

function scrollLeft() {
    scrollContainer.scrollBy({ left: -320, behavior: 'smooth' });
    setTimeout(updateScrollButtons, 500); // Small delay to update visibility
}

function scrollRight() {
    scrollContainer.scrollBy({ left: 320, behavior: 'smooth' });
    setTimeout(updateScrollButtons, 500); // Small delay to update visibility
}

function updateScrollButtons() {
    if (scrollContainer.scrollLeft <= 0) {
        leftButton.style.display = "none"; // Hide left button at the start
    } else {
        leftButton.style.display = "block"; // Show left button if not at the start
    }

    if (scrollContainer.scrollLeft + scrollContainer.clientWidth >= scrollContainer.scrollWidth - 10) {
        rightButton.style.display = "none"; // Hide right button if at the end
    } else {
        rightButton.style.display = "block"; // Show right button if not at the end
    }
}

scrollContainer.addEventListener("scroll", updateScrollButtons);
window.onload = updateScrollButtons;