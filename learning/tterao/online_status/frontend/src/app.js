import { REFRESH_TOKEN } from "./config/constants.js";
import { error404 } from "./views/pages/error404.js";
import { home } from "./views/pages/home.js";
import { login } from "./views/pages/login.js";


const routes = {
  '/': home,
  '/login/': login
};

async function router() {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN)
  const uri = window.location.pathname;
  const page = refreshToken === null && login || (routes[uri] ? routes[uri] : error404)
  const root = document.getElementById("root")
  root.innerHTML = page.render()
  await page.initializeEvents()
}

document.addEventListener('load', router);
document.addEventListener("DOMContentLoaded", router)
