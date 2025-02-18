function increaseQuantity(button) {
    let input = button.previousElementSibling;
    let currentValue = parseInt(input.value, 10);
    input.value = currentValue + 1;
}

function decreaseQuantity(button) {
    let input = button.nextElementSibling;
    let currentValue = parseInt(input.value, 10);
    if (currentValue > 1) {
        input.value = currentValue - 1;
    }
}