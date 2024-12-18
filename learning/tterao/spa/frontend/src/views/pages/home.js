import { Component } from "../component.js";

export class Home extends Component {
  constructor() { super() }

  render() {
    this.root.innerHTML = `
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
  }

  async initializeEvents() {
    // document.querySelector(".logout").addEventListener("click", logoutEvent)
  }
}

