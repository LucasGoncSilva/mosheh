document.addEventListener("DOMContentLoaded", function () {
  const faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");
    const toggleBtn = item.querySelector(".toggle-btn");

    answer.style.display = "none";

    question.addEventListener("click", () => {
      item.classList.toggle("active");

      if (item.classList.contains("active")) {
        answer.style.display = "block";
        toggleBtn.classList.add("active");
      } else {
        answer.style.display = "none";
        toggleBtn.classList.remove("active");
      }
    });
  });
});
