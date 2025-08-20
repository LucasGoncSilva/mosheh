window.addEventListener("DOMContentLoaded", function () {
  const filterInput = document.getElementById("filter");
  const type = document.getElementById("type").innerText;

  filterInput.onkeyup = function () {
    const value = this.value.toLowerCase();
    const arr = document.getElementsByClassName("secret");

    if (!value.length) {
      for (const e of arr) {
        e.classList.remove("hide");
      }
      return;
    }

    switch (type) {
      case "Credenciais":
        for (const e of arr) {
          if (
            !e.dataset.name.includes(value) &&
            !e.dataset.service.includes(value)
          ) {
            e.classList.add("hide");
          } else {
            e.classList.remove("hide");
          }
        }
        break;

      case "Cartões":
        for (const e of arr) {
          if (
            !e.dataset.name.includes(value) &&
            !e.dataset.bank.includes(value)
          ) {
            e.classList.add("hide");
          } else {
            e.classList.remove("hide");
          }
        }
        break;

      case "Anotações":
        for (const e of arr) {
          if (!e.dataset.title.includes(value)) {
            e.classList.add("hide");
          } else {
            e.classList.remove("hide");
          }
        }
        break;
    }
  };
});
