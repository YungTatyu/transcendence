import { addLoginEvent } from "./login/login.js";
import { addVerifyOtpEvent } from "./login/otp.js";

const pageEvents = {
  login: addLoginEvent,
  otp: addVerifyOtpEvent,
}

export function showPage(pageName) {
  const pages = document.querySelectorAll("div[id$='-page']");
  console.log(pages)
  pages.forEach((page) => page.classList.add("d-none"));
  document.getElementById(`${pageName}-page`).classList.remove("d-none");
  const pageEvent = pageEvents[pageName]
  pageEvent()
}

document.addEventListener("DOMContentLoaded", () => {
  showPage("login");
  // showPage("otp");
});
