import config from "../config"
import SPA from "../spa";

const handleReload = async () => {
  const skipPaths = ["/login", "/signup"];
  const currentPath = location.pathname;
  if (currentPath === "/" || skipPaths.some(path => currentPath.startsWith(path))) {
    return;
  }
  const res = await fetch(`${config.authService}/auth/token/refresh`, {
    method: "POST",
  })
  if (res.status >= 400) {
    SPA.navigate("/title")
    return
  }
  const data = await res.json();

}
