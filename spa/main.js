import SPA from "./spa.js";
window.SPA = SPA;

import Game, { setupGame } from "./views/Game.js";
import GameHome from "./views/GameHome.js";
import GameResult from "./views/GameResult.js";
import Home from "./views/Home.js";
import Login, { setupLogin } from "./views/Login.js";
import LoginVerify, { setupLoginVerify } from "./views/LoginVerify.js";
import MatchHistory from "./views/MatchHistory.js";
import NotFound from "./views/NotFound.js";
import Profile from "./views/Profile.js";
import SignUp, { setupSignUp } from "./views/SignUp.js";
import SignUpVerify, { setupSignUpVerify } from "./views/SignUpVerify.js";
import Store, { setupStore } from "./views/Store.js";
import ApiData, { setupApiData } from "./views/apiPage.js";

SPA.route("/", Home);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);
SPA.route("/profile", Profile);
SPA.route("/match-history", MatchHistory);
SPA.route("/signup", SignUp, setupSignUp);
SPA.route("/signup/verify", SignUpVerify, setupSignUpVerify);
SPA.route("/login", Login, setupLogin);
SPA.route("/login/verify", LoginVerify, setupLoginVerify);
SPA.route("/game", Game, setupGame);
SPA.route("/game/result", GameResult);
SPA.route("/home", GameHome);

SPA.init({ containerId: "app" });
