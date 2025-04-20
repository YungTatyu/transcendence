import { handleLoading } from "./utils/jwtHelper.js";

const SPA = (() => {
  const routes = {};
  let currentRoute = null;
  let container = null;

  const init = ({ containerId }) => {
    container = document.getElementById(containerId);
    window.addEventListener("popstate", renderRoute);
    window.addEventListener("DOMContentLoaded", async () => {
      await handleLoading();
      await renderRoute();
    });
  };

  const route = (path, view, setup, cleanup) => {
    routes[path] = { view, setup, cleanup };
  };

  const navigate = async (path, params = null, replace = false) => {
    if (replace) {
      history.replaceState({}, "", path);
    } else {
      history.pushState({}, "", path);
    }
    await renderRoute(params);
  };

  const renderRoute = async (params) => {
    //前回のルートのcleanupを実行
    if (currentRoute?.cleanup) {
      currentRoute.cleanup();
    }

    const path = window.location.pathname;
    const route = routes[path] || routes["/404"];
    if (route && container) {
      // INFO setupよりも先にcurrentRouteを更新する必要有り
      currentRoute = route;
      container.innerHTML = route.view(params);
      applyAutofocus();
      if (route.setup) {
        await route.setup();
      }
    }
  };

  const applyAutofocus = () => {
    // INFO input要素があれば1つ目のinputにfocusする
    const inputs = document.querySelectorAll("input");
    if (inputs.length > 0) {
      inputs[0].focus();
    }
  };

  return { init, route, navigate };
})();

export default SPA;
