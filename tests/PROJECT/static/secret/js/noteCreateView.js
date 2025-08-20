window.addEventListener("DOMContentLoaded", function () {
  const title = document.getElementById("id_title");
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
    slug_field.value = slugifyText(title.value);
  }

  title.addEventListener("change", populateSlug);
  title.addEventListener("focus", populateSlug);
  title.addEventListener("keyup", populateSlug);
});
