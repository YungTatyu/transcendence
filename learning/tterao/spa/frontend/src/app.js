import { Error404 } from "./views/pages/error404.js";
import { Home } from "./views/pages/home.js";
import { Login } from "./views/pages/login.js";


const routes = {
  '/': Home,
  '/login/': Login
};

async function router() {
  const uri = window.location.pathname;
  const pageClass = (routes[uri] ? routes[uri] : Error404)
  const page = new pageClass()
  page.render()
  await page.initializeEvents()
}

document.addEventListener('load', router);
document.addEventListener("DOMContentLoaded", router)
