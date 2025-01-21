export default class Component extends HTMLElement {
  #props = {}
  #state = {}
  #events = {}

  constructor(props = {}) {
    super()
    this.#props = props
  }

  render() { }

  getState() { return this.#state }

  setState(state) { this.#state = state }

  addEvent(event, handler) {
    document.addEventListener(event, handler)
    if (!this.#events[event]) {
      // 一つのイベントに複数のハンドラを登録できるように配列にする
      this.#events[event] = [];
    }
    this.#events[event].push(handler);
  }

  /**
   * @brief render()の中でeventListnerを追加する際に使用する
   *
   * @param events {Object<string, Array<Function>>} イベント名をキーとして、対応するイベントハンドラの配列を保持するオブジェクト
   * @example
   * const events = {
   *   "onclick": [handler1, handler2],
   *   "hover": [handler3]
   * };
   *
   */
  addEvents(events) {
    for (const event in events) {
      for (const handler of events[event]) {
        this.addEvent(event, handler)
      }
    }
  }

  removeEvent(event, handler) {
    if (!this.#events[event]) {
      return
    }
    this.#events[event] = this.#events[event].filter(target => target !== handler);
    document.removeEventListener(event, handler);
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
    for (const event in this.#events) {
      for (const handler of this.#events[event]) {
        document.removeEventListener(event, handler);
      }
      delete this.#events[event];
    }
  }
}
