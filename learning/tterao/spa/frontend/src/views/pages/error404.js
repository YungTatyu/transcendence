import { Component } from "../component.js"

export class Error404 extends Component {
  constructor() { super() }

  render() {
    this.root.innerHTML = `
      <h1>404 Error</h1>
      <h2>page not found</h2>
`
  }

  initializeEvents() { }
}
