import SPA from "./spa.js";
window.SPA = SPA;

import Game, { setupGame } from "./views/Game.js";
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

import FriendList, { setupFriendList } from "./views/FriendList.js";
import FriendRequestList, { setupFriendRequestList } from "./views/FriendRequestList.js";


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
SPA.route("/friend/friend-list", FriendList, setupFriendList)
SPA.route("/friend/friend-request-list", FriendRequestList, setupFriendRequestList)

SPA.init({ containerId: "app" });
