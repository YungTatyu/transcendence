const SPA = (() => {
  const routes = {};
  let container = null;

  const init = ({ containerId }) => {
    container = document.getElementById(containerId);
    window.addEventListener("popstate", renderRoute);
    window.addEventListener("DOMContentLoaded", renderRoute);
    renderRoute();
  };

  const route = (path, view, setup) => {
    routes[path] = { view, setup };
  };

  const navigate = (path, params = null, replace = false) => {
    if (replace) {
      history.replaceState({}, "", path);
    } else {
      history.pushState({}, "", path);
    }
    renderRoute(params);
  };

  const renderRoute = (params) => {
    const path = window.location.pathname;
    const route = routes[path] || routes["/404"];
    if (route && container) {
      container.innerHTML = route.view(params);
      if (route.setup) {
        route.setup();
      }
    }
  };

  return { init, route, navigate };
})();

export default SPA;
