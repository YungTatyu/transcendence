import { Component } from "../../core/Component.js";

export class Error404 extends Component {
  constructor() { super() }

  render() {
    const header = document.createElement("h1")
    header.innerText = "404 Error"
    this.appendChildComponent(header)

    const message = document.createElement("h2")
    header.innerText = "page not found"
    this.appendChildComponent(header)
  }
}

customElements.define('error404-component', Error404);
