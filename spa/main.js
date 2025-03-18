import SPA from "./spa.js";
window.SPA = SPA;

import Game, { setupGame } from "./views/Game.js";
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
import ChangeUsername from "./views/ChangeUsername.js";
import ChangeMail from "./views/ChangeMail.js";
import ChangePassword from "./views/ChangePassword.js";
import ChangeAvatar from "./views/ChangeAvatar.js";

SPA.route("/", Home);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);
SPA.route("/signup", SignUp, setupSignUp);
SPA.route("/signup/verify", SignUpVerify, setupSignUpVerify);
SPA.route("/login", Login, setupLogin);
SPA.route("/login/verify", LoginVerify, setupLoginVerify);
SPA.route("/game", Game, setupGame);
SPA.route("/game/result", GameResult);
SPA.route("/profile", Profile);
SPA.route("/profile/username", ChangeUsername);
SPA.route("/profile/mail", ChangeMail);
SPA.route("/profile/password", ChangePassword);
SPA.route("/profile/avatar", ChangeAvatar);
SPA.route("/history/match", MatchHistory);


SPA.init({ containerId: "app" });
