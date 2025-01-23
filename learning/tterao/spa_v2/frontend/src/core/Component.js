export class Component extends HTMLElement {
  #props = {}
  #state = {}
  #events = []
  #childComponents = []

  constructor(props = {}) {
    super()
    this.#props = props
  }

  connectedCallback() {
    this.render()
    console.log("カスタム要素がページに追加されました。");
  }

  disconnectedCallback() {
    console.log("カスタム要素がページから除去されました。");
    this.removeAllEvents()
  }

  adoptedCallback() {
    console.log("カスタム要素が新しいページへ移動されました。");
  }

  attributeChangedCallback(name, oldValue, newValue) {
    console.log(`属性 ${name} が変更されました。`);
  }

  render() { }

  getState() { return this.#state }

  setState(state) { this.#state = state }

  addEvent(event, handler) {
    this.addEventListener(event, handler)
    this.#events.push({ event, handler });
  }

  /**
   * @brief render()の中でeventListnerを追加する際に使用する
   *
   * @param events Array<string, Function> イベント名をキーとして、対応するイベントハンドラの配列
   * @example
   * const events = {
   *   "onclick": [handler1, handler2],
   *   "hover": [handler3]
   * };
   *
   */
  addEvents(events) {
    events.forEach(({ event, handler }) => {
      this.addEvent(event, handler)
    });
  }

  /**
   * 主にrender()の中で要素を追加する際に使用する
   *
   * @param Component | HTMLElement
   */
  appendChildComponent(component) {
    this.appendChild(component)
    this.#childComponents.push(component)
  }

  removeAllChildren() {
    this.#childComponents.forEach((component) => {

    });
  }

  removeAllEvents() {
    this.#events.forEach(({ event, handler }) => {
      this.removeEventListener(event, handler);
    });
    this.#events = [];
  }
}

customElements.define('custom-component', Component);
