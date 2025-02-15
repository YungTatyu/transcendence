import SPA from "./spa.js";
window.SPA = SPA;

import Home from "./views/Home.js";
import NotFound from "./views/NotFound.js";


SPA.route("/", Home);
SPA.route("/404", NotFound);

SPA.init({ containerId: "app" });
