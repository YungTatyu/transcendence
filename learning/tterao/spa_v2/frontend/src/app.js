import { Error404 } from "./views/pages/error404.js";
import { Home } from "./views/pages/home.js";
import { Login } from "./views/pages/login.js";
import { Router } from "./core/Router.js";

async function main() {
  const routes = {
    '/': new Home,
    '/login': new Login,
    '/404': new Error404,
  };
  const router = new Router(routes, document.getElementById("root"))
  router.initialize()
  router.render()
}

document.addEventListener('load', main);
document.addEventListener("DOMContentLoaded", main)
