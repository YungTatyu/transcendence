const SPA = (function() {
    const routes = {};
    let container = null;

    const init = ({ containerId }) => {
        container = document.getElementById(containerId);
        renderRoute();
    };

    const route = (path, view) => {
        routes[path] = view;
    };

    const navigate = (path) => {
        history.pushState({}, "", path);
        renderRoute();
    };

    const renderRoute = () => {
        const path = window.location.pathname;
        const view = routes[path] || routes["/404"];

        if (view && container) {
            container.innerHTML = view();
        }
    };

    return { init, route, navigate };
})();

export default SPA;
