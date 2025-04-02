import SPA from "./spa.js";
window.SPA = SPA;

import ChangeAvatar from "./views/ChangeAvatar.js";
import ChangeMail from "./views/ChangeMail.js";
import ChangePassword from "./views/ChangePassword.js";
import ChangeUsername, { setupChageUsername } from "./views/ChangeUsername.js";
import FriendRequestForm, {
  setupFriendRequestForm,
} from "./views/FriendRequestForm.js";
import Game, { cleanupGame, setupGame } from "./views/Game.js";
import GameResult, { setupGameResult } from "./views/GameResult.js";
import Home, { setupHome } from "./views/Home.js";
import InitMatch, { setupInitMatch } from "./views/InitMatch.js";
import Login, { setupLogin } from "./views/Login.js";
import LoginVerify, { setupLoginVerify } from "./views/LoginVerify.js";
import MatchHistory from "./views/MatchHistory.js";
import NotFound from "./views/NotFound.js";
import Profile, { setupProfile } from "./views/Profile.js";
import QuickPlayMatching, {
  setupQuickPlayMatching,
} from "./views/QuickPlayMatching.js";
import SignUp, { setupSignUp } from "./views/SignUp.js";
import SignUpVerify, { setupSignUpVerify } from "./views/SignUpVerify.js";
import Store, { setupStore } from "./views/Store.js";
import TmpHome from "./views/TmpHome.js";
import Tournament, { setupTournament } from "./views/Tournament.js";
import TournamentMatching, {
  setupTournamentMatching,
} from "./views/TournamentMatching.js";
import ApiData, { setupApiData } from "./views/apiPage.js";

import FriendList, { setupFriendList } from "./views/FriendList.js";
import FriendRequestList, {
  setupFriendRequestList,
} from "./views/FriendRequestList.js";

SPA.route("/", TmpHome);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);
SPA.route("/signup", SignUp, setupSignUp);
SPA.route("/signup/verify", SignUpVerify, setupSignUpVerify);
SPA.route("/login", Login, setupLogin);
SPA.route("/login/verify", LoginVerify, setupLoginVerify);
SPA.route("/friend", FriendList, setupFriendList);
SPA.route("/friend/request", FriendRequestList, setupFriendRequestList);
SPA.route("/game", Game, setupGame, cleanupGame);
SPA.route("/game/result", GameResult, setupGameResult);
SPA.route("/home", Home, setupHome);
SPA.route("/game/setup", InitMatch, setupInitMatch);
SPA.route("/tournament", Tournament, setupTournament);
SPA.route("/profile", Profile, setupProfile);
SPA.route("/profile/username", ChangeUsername, setupChageUsername);
SPA.route("/profile/mail", ChangeMail);
SPA.route("/profile/password", ChangePassword);
SPA.route("/profile/avatar", ChangeAvatar);
SPA.route("/history/match", MatchHistory);
SPA.route("/matching/quick-play", QuickPlayMatching, setupQuickPlayMatching);
SPA.route("/matching/tournament", TournamentMatching, setupTournamentMatching);

SPA.route(
  "/friend/friend-request-form",
  FriendRequestForm,
  setupFriendRequestForm,
);
SPA.init({ containerId: "app" });
