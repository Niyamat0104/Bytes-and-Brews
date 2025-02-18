function validateForm() {
  let isValid = true;

  // Clear previous error messages
  document.getElementById("usernameError").textContent = "";
  document.getElementById("emailError").textContent = "";
  document.getElementById("phoneError").textContent = "";
  document.getElementById("queryError").textContent = "";

  // Username validation
  const username = document.getElementById("username").value.trim();
  if (username === "") {
    document.getElementById("usernameError").textContent =
      "Username is required.";
    isValid = false;
  }

  // Email validation
  const email = document.getElementById("email").value.trim();
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (email === "" || !emailPattern.test(email)) {
    document.getElementById("emailError").textContent =
      "Please enter a valid email.";
    isValid = false;
  }

  // Phone number validation
  const phone = document.getElementById("phone").value.trim();
  const phonePattern = /^[0-9]{10}$/;
  if (phone === "" || !phonePattern.test(phone)) {
    document.getElementById("phoneError").textContent =
      "Please enter a valid 10-digit phone number.";
    isValid = false;
  }

  // Query validation
  const query = document.getElementById("query").value.trim();
  if (query === "") {
    document.getElementById("queryError").textContent =
      "Query cannot be empty.";
    isValid = false;
  }

  if (isValid) {
    alert("Form submitted successfully!");
    document.getElementById("contactForm").reset();
  }
}
