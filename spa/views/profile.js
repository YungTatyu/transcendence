import stateManager from "../stateManager.js";

export default function Profile() {
  return `

    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <p class="title text-start">PROFILE</p>
        </div>
        <div class="col align-self-end">
          <div class="position-relative">
            <img src="./assets/home.png" class="home-icon position-absolute top-0 end-0">
          </div>
        </div>
      </div>
    </div>

    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img id="user-avatar" src="./assets/42.png" alt="ロゴ" class="square-img rounded-circle me-2 pencil-icon" >
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>


      <div class="d-inline-flex align-items-center mt-5">
          <p id="username" class="text me-2">UserName</p>
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>


      <div class="d-inline-flex align-items-center">
          <p class="text me-2">Password</p>
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>

      <div class="d-inline-flex align-items-center">
          <p class="text me-2">Mail</p>
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>
    </div>


    <div class="container text-center mt-4 match-record">
      <div id="row-content" class="row row-cols-3">
        <div class="col">Number1</div>
        <div class="col">Number2</div>
        <div class="col">Number3</div>
      </div>
      <div id="row-label" class="row row-cols-3">
        <div class="col">Wins</div>
        <div class="col">Losses</div>
        <div class="col">Tournament Wins</div>
      </div>
    </div>

    <div class="d-grid gap-2 col-6 mx-auto mt-5">
      <button class="btn btn-primary rounded-pill" type="button">Match History</button>
    </div>

  `;
}
