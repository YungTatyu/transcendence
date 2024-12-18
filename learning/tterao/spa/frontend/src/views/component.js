/**
 * interface
 */
export class Component {
  constructor() {
    if (this.constructor === Component) {
      throw new Error("Component interface needs to be inherited.")
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
