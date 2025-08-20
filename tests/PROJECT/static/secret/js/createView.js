window.addEventListener("DOMContentLoaded", function () {
  const userInfo = this.document.getElementById("userData");
  const user = userInfo.dataset.user;
  const userID = userInfo.dataset.userId;

  ownerField = document.getElementById("id_owner");
  ownerField.innerHTML = `<option value="${userID}">${user}</option>`;
  ownerField.parentElement.classList.add("none");
});
