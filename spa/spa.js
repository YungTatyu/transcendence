const SPA = (function() {
    const routes = {};
    let container = null;
  
    const init = ({ containerId }) => {
      container = document.getElementById(containerId);
      renderRoute();
    };
  
    const route = (path, view, setup) => {
      routes[path] = { view, setup };
    };
  
    const navigate = (path) => {
      history.pushState({}, "", path);
      renderRoute();
    };
  
    const renderRoute = () => {
      const path = window.location.pathname;
      const route = routes[path] || routes["/404"];
      if (route && container) {
        container.innerHTML = route.view();
        if (route.setup) {
          route.setup();
        }
      }
    };
  
    return { init, route, navigate };
  })();
  
  export default SPA;
  