window.addEventListener("DOMContentLoaded", function () {
  const bank = document.getElementById("id_bank");
  const name = document.getElementById("id_name");
  const slug_field = document.getElementById("id_slug");

  slug_field.readOnly = true;

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
    slug_field.value = bank.value + slugifyText(name.value);
  }

  bank.addEventListener("change", populateSlug);
  bank.addEventListener("focus", populateSlug);
  bank.addEventListener("keyup", populateSlug);
  name.addEventListener("change", populateSlug);
  name.addEventListener("focus", populateSlug);
  name.addEventListener("keyup", populateSlug);
});
