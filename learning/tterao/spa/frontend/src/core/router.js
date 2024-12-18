/**
 * @class Router
 * @description 
 * シングルページアプリケーション (SPA) のルーティングを管理するクラス。
 * 現在のURLに基づいて適切なコンポーネントを表示し、動的な画面遷移を可能にする。
 */
export class Router {
  constructor(routes, rootEle) {
    this.routes = routes
    this.rootEle = rootEle
    this.initialize();
  }

  /**
   * @method route
   * @description
   * 現在のURLパスを解析し、対応するコンポーネントを描画する。
   * 404エラーページを表示する場合も含む。
   * @returns {Promise<void>}
   * @example
   * URLが '/login/' の場合、Loginコンポーネントを表示
   * router.route();
   */
  async route() {
    const uri = window.location.pathname;
    const component = this.routes[uri] || this.routes["/404"];
    const rootComp = new component();
    this.rootEle.innerHTML = rootComp.render();
    await rootComp.initializeEvents();
  }

  // イベントリスナーでURL変更時にrouteを実行
  initialize() {
    window.addEventListener("popstate", () => this.route()); // 戻る/進むボタン対応
    document.addEventListener("DOMContentLoaded", () => this.route());
  }
}
