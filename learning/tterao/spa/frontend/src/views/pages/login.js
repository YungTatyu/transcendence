import { Router } from "../router.js";

export class Login extends Router {
  constructor() { super() }

  render() {
    this.root.innerHTML = `
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
    </div >
  `
  }

  initializeEvents() { }
}

