import SPA from "./spa.js";
window.SPA = SPA;

import Home from "./views/Home.js";
import NotFound from "./views/NotFound.js";
import Store, { setupStore } from "./views/Store.js";
import ApiData, { setupApiData } from "./views/apiPage.js";
import SignUp, { setupSignUp } from "./views/signUp.js";
import SignUpVerify, { setupSignUpVerify } from "./views/signUpVerify.js";
import Login, { setupLogin } from "./views/login.js";

SPA.route("/", Home);
SPA.route("/404", NotFound);
SPA.route("/store", Store, setupStore);
SPA.route("/api", ApiData, setupApiData);
SPA.route("/signup", SignUp, setupSignUp);
SPA.route("/signup-verify", SignUpVerify, setupSignUpVerify);
SPA.route("/login", Login, setupLogin);

SPA.init({ containerId: "app" });
