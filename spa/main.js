import SPA from "./spa.js";
window.SPA = SPA;

import Game, { setupGame } from "./views/Game.js";
import Home from "./views/Home.js";
import NotFound from "./views/NotFound.js";
import Store, { setupStore } from "./views/Store.js";
import ApiData, { setupApiData } from "./views/apiPage.js";
import MatchHistory from "./views/match-history.js";
import Profile from "./views/profile.js";

SPA.route("/", Home);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);
SPA.route("/profile", Profile);
SPA.route("/match-history", MatchHistory);
SPA.route("/game", Game, setupGame);

SPA.init({ containerId: "app" });
