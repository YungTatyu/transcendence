import { decodeJwt, scheduleTokenRefresh } from "./jwt.js";
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
  pages.forEach((page) => page.classList.add("d-none"));
  document.getElementById(`${pageName}-page`).classList.remove("d-none");
  const pageEvent = pageEvents[pageName]
  pageEvent()
}

document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("authtoken")
  if (token === null) {
    showPage("login");
    return
  }
  const tokens = JSON.parse(token)
  const re = await scheduleTokenRefresh(tokens.refresh)
  if (!re) {
    showPage("login")
    return
  }
  showPage("home")
});
