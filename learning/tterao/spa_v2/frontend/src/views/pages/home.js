import { Component } from "../../core/Component.js";

export class Home extends Component {
  constructor() { super() }

  render() {
    const content = `
    <div class="container mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>Welcome</h2>
        <ul class="list-unstyled js-user-status"></ul>
      </div>
      <button type="submit" class="btn btn-primary logout mb-3">Logout</button>
      <div class="content">
        <p>Here is your homepage content!</p>
      </div>
    </div>
`
    const template = document.createElement("template");
    template.innerHTML = content.trim(); // 空白をトリムしておく
    this.appendChildComponent(template)
  }
}

customElements.define('home-component', Home);
