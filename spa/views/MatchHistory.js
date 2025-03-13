import TitileAndHomeButton from "../components/titleAndHomeButton.js";

export default function MatchHistory() {
  return `

    ${TitileAndHomeButton("MATCH HISTORY")}

    <div class="container text-center history-container">
      <div class="row row-cols-5 header-row">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div id="content-row"">
      <!-- ここにAPIから取得したデータが挿入される -->
        <div class="row row-cols-5 mt-2">
          <div class="col">Quick Play</div>
          <div class="col text-center">
            <img src="./assets/42.png" alt="ロゴ" class="square-img rounded-circle me-2" >
            <span>username</span>
          </div>
          <div class="col">WIN</div>
          <div class="col">11-3</div>
          <div class="col">2025/01/01</div>
        </div>
        <!-- ここまでAPIから取得したデータが挿入される -->
      </div>
    </div>  

  `;
}
