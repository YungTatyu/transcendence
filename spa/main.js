import SPA from "./spa.js";
window.SPA = SPA;

import ApiData, { setupApiData } from "./views/APIView.js";
import Home from "./views/Home.js";
import NotFound from "./views/NotFound.js";
import Store, { setupStore } from "./views/Store.js";

SPA.route("/", Home);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);

SPA.init({ containerId: "app" });
