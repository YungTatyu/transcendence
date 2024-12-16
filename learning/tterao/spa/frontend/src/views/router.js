/**
 * interface
 */
export class Router {
  constructor() {
    if (this.constructor === Router) {
      throw new Error("Router interface needs to be inherited.")
    }
    this.root = document.getElementById("root")
  }

  render() {
    throw new Error("Method 'render()' must be implemented")
  }

  async initializeEvents() {
    throw new Error("Method 'initializeEvents()' must be implemented")
  }
}
