export default class Component extends HTMLElement {
  #props = {}
  #state = {}
  #events = {}

  constructor(props = {}) {
    super()
    this.#props = props
  }

  /**
   * HTMLElementを描画して、event listenerを登録
   */
  update(events) {
    this.render()
    for (const event in events) {
      for (const handler of events[event]) {
        this.addEvent(event, handler)
      }
    }
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

  removeEvent(event, handler) {
    if (!this.#events[event]) {
      return
    }
    this.#events[event] = this.#events[event].filter(target => target !== handler);
    document.removeEventListener(event, handler);
  }

  /**
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
