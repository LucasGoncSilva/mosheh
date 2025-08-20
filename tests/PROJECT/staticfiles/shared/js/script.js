document.addEventListener("DOMContentLoaded", () => {
  const year = new Date().getFullYear();

  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80, // Navbar height
          behavior: "smooth",
        });
      }
    });
  });

  function setCurrentYear() {
    document.querySelectorAll(".current-year").forEach((e) => {
      e.textContent = year;
    });
  }
  setCurrentYear();

  // Toggle Inputs Visibility
  document.querySelectorAll(".toggle-input-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const input = document.getElementById(targetId);

      if (input.type === "password") {
        input.type = "text";
        this.textContent = "Hide";
      } else {
        input.type = "password";
        this.textContent = "View";
      }
    });
  });
});
