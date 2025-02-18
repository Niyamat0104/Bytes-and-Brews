document.addEventListener("DOMContentLoaded", () => {
    const paymentOptions = document.querySelectorAll(".payment-option");
    const payBtn = document.getElementById("payBtn");
    const priceElement = document.getElementById("price");
  
    
  
    paymentOptions.forEach(option => {
      option.addEventListener("click", () => {
        // Remove selected class from other options
        document.querySelector(".payment-option.selected")?.classList.remove("selected");
  
        // Add selected class to clicked option
        option.classList.add("selected");
  
        // Update button text based on selected method
        const selectedMethod = option.dataset.method;
        payBtn.textContent = `Pay ₹${totalAmount} with ${selectedMethod}`;
      });
    });
  
    payBtn.addEventListener("click", () => {
      const selectedMethod = document.querySelector(".payment-option.selected")?.dataset.method;
      if (selectedMethod) {
        alert(`Payment made using ${selectedMethod}`);
      }  
    });
  });
  
  