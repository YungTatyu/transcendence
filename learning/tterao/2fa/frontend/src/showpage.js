import { decodeJwt } from "./jwt.js";
import { addLoginEvent } from "./login/login.js";
import { addVerifyOtpEvent } from "./login/otp.js";
import { addLogoutEvent } from "./logout/logout.js";
import { addSignupEvent } from "./signup/signup.js";

const pageEvents = {
  login: addLoginEvent,
  otp: addVerifyOtpEvent,
  signup: addSignupEvent,
  home: addLogoutEvent,
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
  const token = localStorage.getItem("authtoken")
  if (token === null) {
    showPage("login");
    return
  }
  console.log(decodeJwt(JSON.parse(token).access))
  showPage("home")
});
