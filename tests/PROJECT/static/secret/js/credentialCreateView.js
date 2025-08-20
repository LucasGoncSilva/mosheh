window.addEventListener("DOMContentLoaded", function () {
  const thirdPartyLogin = document.getElementById("id_third_party_login_name");
  const thirdPartyLoginDiv = thirdPartyLogin.parentElement;
  const login = document.getElementById("id_login");
  const loginDiv = login.parentElement;
  const password = document.getElementById("id_password");
  const passwordDiv = password.parentElement;
  const thirdPartyCheck = document.getElementById("id_third_party_login");
  const form = document.querySelector("form");
  const service = document.getElementById("id_service");
  const name = document.getElementById("id_name");
  const slug_field = document.getElementById("id_slug");

  slug_field.readOnly = true;

  function initPage() {
    loginDiv.classList.remove("hidden-zero");
    passwordDiv.classList.remove("hidden-zero");
    thirdPartyLoginDiv.classList.remove("hidden-zero");

    if (thirdPartyCheck.checked) {
      login.value = "-----";
      password.value = "-----";
      loginDiv.classList.add("hidden-zero");
      passwordDiv.classList.add("hidden-zero");
    } else {
      thirdPartyLogin.value = "-----";
      thirdPartyLoginDiv.classList.add("hidden-zero");
    }
  }
  initPage();

  function toggleFields() {
    thirdPartyLoginDiv.classList.toggle("hidden-zero");
    loginDiv.classList.toggle("hidden-zero");
    passwordDiv.classList.toggle("hidden-zero");
  }

  function slugifyText(text) {
    return text
      .toString() // Cast to string (optional)
      .normalize("NFKD") // The normalize() using NFKD method returns the Unicode Normalization Form of a given string.
      .toLowerCase() // Convert the string to lowercase letters
      .trim() // Remove whitespace from both sides of a string (optional)
      .replace(/\s+/g, "-") // Replace spaces with -
      .replace(/[^\w\-]+/g, ""); // Remove all non-word chars
  }

  function populateSlug() {
    slug_field.value = service.value + slugifyText(name.value);
  }

  thirdPartyCheck.onclick = function () {
    if (this.checked) {
      login.value = "-----";
      password.value = "-----";
      toggleFields();
      thirdPartyLogin.value = "";
    } else {
      thirdPartyLogin.value = "-----";
      toggleFields();
      login.value = "";
      password.value = "";
    }
  };

  form.addEventListener("submit", function () {
    if (!thirdPartyCheck.checked) {
      thirdPartyLogin.value = "-----";
    } else {
      login.value = "-----";
      password.value = "-----";
    }
  });
  form.addEventListener("reset", function () {
    setTimeout(function () {
      initPage();
    }, 0);
  });

  service.addEventListener("change", populateSlug);
  service.addEventListener("focus", populateSlug);
  service.addEventListener("keyup", populateSlug);
  name.addEventListener("change", populateSlug);
  name.addEventListener("focus", populateSlug);
  name.addEventListener("keyup", populateSlug);
});
