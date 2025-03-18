const SPA = (() => {
  const routes = {};
  let container = null;

  const init = ({ containerId }) => {
    container = document.getElementById(containerId);
    window.addEventListener("popstate", renderRoute);
    window.addEventListener("DOMContentLoaded", renderRoute);
    renderRoute();
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
    const path = window.location.pathname;
    const route = routes[path] || routes["/404"];
    if (route && container) {
      container.innerHTML = route.view(params);
      if (route.setup) {
        await route.setup();
      }
      if (route.cleanup) {
        route.cleanup();
      }
    }
  };

  return { init, route, navigate };
})();

export default SPA;
