import { Error404 } from "./views/pages/error404.js";
import { Home } from "./views/pages/home.js";
import { Login } from "./views/pages/login.js";
import { Router } from "./core/router.js";

async function main() {
  const routes = {
    '/': Home,
    '/login': Login,
    '/404': Error404,
  };
  const router = new Router(routes, document.getElementById("root"))
  router.route()
}

document.addEventListener('load', main);
document.addEventListener("DOMContentLoaded", main)
