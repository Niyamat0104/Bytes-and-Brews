document.addEventListener("DOMContentLoaded", () => {
    const agreeBtn = document.getElementById("agree-btn");
    const declineBtn = document.getElementById("decline-btn");

    agreeBtn.addEventListener("click", () => {
        alert("Thank you for accepting our terms! Enjoy Bytes and Brew.");
        window.location.assign(); // Redirect to homepage
    });

    declineBtn.addEventListener("click", () => {
        alert("You must accept the terms to proceed.");
    });
});