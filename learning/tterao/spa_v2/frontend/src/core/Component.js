export default class Component extends HTMLElement {
  #props = {}
  #state = {}
  #events = []

  constructor(props = {}) {
    super()
    this.#props = props
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
  addChildComponent(component) {
    this.appendChild(component)
  }

  removeAllEvents() {
    this.#events.forEach(({ event, handler }) => {
      this.removeEventListener(event, handler);
    });
    this.#events = [];
  }
}
