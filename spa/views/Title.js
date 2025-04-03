export default function Title() {
  return `
        <div class="d-flex justify-content-center align-items-center flex-column vh-100 position-relative">
            <p class="title-text">Ping <br />Pong</p>
            <div class="d-flex title-custom-gap">
                <button class="btn btn-primary btn-signup js-btn-signup" type="button">SignUp</button>
                <button class="btn btn-primary btn-login js-btn-login" type="button">Login</button>
            </div>
        </div>
    `;
}

export function setupTitile() {
  const btnSinup = document.querySelector(".js-btn-signup");
  const btnLogin = document.querySelector(".js-btn-login");

  btnSinup.addEventListener("click", () => {
    SPA.navigate("/signup");
  });

  btnLogin.addEventListener("click", () => {
    SPA.navigate("/login");
  });
}
