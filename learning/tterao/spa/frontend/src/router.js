export class Router {
  constructor(routes) {
    this.routes = routes
    this.root = document.getElementById("root")
    this.initialize();
  }

  // 現在のURLに対応するコンポーネントを表示
  async route() {
    const uri = window.location.pathname;
    const component = this.routes[uri] || this.routes["/404"];
    const rootComp = new component();
    this.root.innerHTML = rootComp.render();
    await rootComp.initializeEvents();
  }

  // イベントリスナーでURL変更時にrouteを実行
  initialize() {
    window.addEventListener("popstate", () => this.route()); // 戻る/進むボタン対応
    document.addEventListener("DOMContentLoaded", () => this.route());
  }
}
