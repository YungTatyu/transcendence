import stateManager from "../stateManager.js";

export default function MatchHistory() {
  return `

    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <p class="title text-start">MATCH HISTORY</p>
        </div>
        
        <div class="col align-self-end">
          <div class="position-relative">
            <svg class="home-icon bi bi-house-door-fill position-absolute top-0 end-0"
              xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor">
              <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
            </svg>
          </div>
        </div>
      </div>
    </div>



    <div class="container text-center history-container">
      <div class="row row-cols-5 header-row">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div class="row row-cols-5 content-row mt-2">
        <div class="col">Quick Play</div>
        <div class="col text-center">
          <img src="./assets/42.png" alt="ロゴ" class="square-img rounded-circle me-2" >
          <span>username</span>
        </div>
        <div class="col">WIN</div>
        <div class="col">11-3</div>
        <div class="col">2025/01/01</div>
      </div>
    </div>

    

  `;
}
