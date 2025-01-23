import { Component } from "../../core/Component.js";

class ExampleButton extends Component {
  constructor() { super() }

  buttonHandler(event) {
    event.preventDefault()
    alert("example button clicked!")
  }

  buttonHandler2(event) {
    event.preventDefault()
    alert("buttonHandler2")
  }

  render() {
    // const button = document.createElement("button")
    // button.classList.add("btn", "btn-warning");
    // button.innerText = "Example Button";
    // this.appendChild(button);

    this.classList.add("btn", "btn-warning");
    this.innerText = "Example Button!";
    this.addEvents([
      { "click": this.buttonHandler },
      { "click": this.buttonHandler2 }
    ])
  }
}

customElements.define('example-button-component', ExampleButton);

export class Login extends Component {
  constructor() { super() }

  render() {
    const content = `
      <div id = "login-page" class="container mt-5 d-flex justify-content-center align-items-center text-center" >
        <div class="position-relative">
          <h2 class="mb-3">Login</h2>
          <form class="login-form">
            <div class="mb-3">
              <input type="text" class="form-control" name="username" placeholder="Username" required />
            </div>
            <div class="mb-3"> <input type="password" class="form-control" name="password" placeholder="Password"
              required />
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
          </form>
        </div>
    </div>
  `
    const template = document.createElement("template");
    template.innerHTML = content.trim(); // 空白をトリムしておく
    this.appendChildComponent(template.content)
    this.appendChildComponent(new ExampleButton)
  }
}

customElements.define('login-component', Login);
