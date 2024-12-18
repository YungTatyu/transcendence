/**
 * @class Component
 * @description
 * 全てのコンポーネントクラスが継承すべきベースクラス（インターフェース）。
 * このクラス自体は直接インスタンス化できず、必ず継承して `render` と `initializeEvents` メソッドを実装する必要がある。
 * コンポーネント設計の一貫性を保つための基盤を提供する。
 * 
 * @example
 * // 継承して新しいコンポーネントを作成
 * class MyComponent extends Component {
 *   render() {
 *     return "<h1>Hello World</h1>";
 *   }
 * 
 *   async initializeEvents() {
 *     console.log("Event Initialized");
 *   }
 * }
 */
export class Component {
  constructor() {
    if (this.constructor === Component) {
      throw new Error("Component interface needs to be inherited.")
    }
  }

  render() {
    throw new Error("Method 'render()' must be implemented")
  }

  async initializeEvents() {
    throw new Error("Method 'initializeEvents()' must be implemented")
  }
}
