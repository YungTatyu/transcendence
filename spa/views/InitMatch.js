import stateManager from "../stateManager.js";

// TODO 一旦開発用に仮に作った
export default function InitMatch() {
  alert(`your userid: ${stateManager?.userId}`);
  return `
    <div class="container mt-5">
      <h2 class="mb-4">試合情報入力フォーム</h2>
      <form class="js-match-form">
          <div class="mb-3">
              <label for="matchId" class="form-label">Match ID</label>
              <input type="text" class="form-control" id="matchId" name="matchId" placeholder="試合IDを入力">
          </div>
          <div class="mb-3">
              <label for="leftPlayerId" class="form-label">Left Player ID</label>
              <input type="text" class="form-control" id="leftPlayerId" name="leftPlayerId" placeholder="左プレイヤーIDを入力">
          </div>
          <div class="mb-3">
              <label for="rightPlayerId" class="form-label">Right Player ID</label>
              <input type="text" class="form-control" id="rightPlayerId" name="rightPlayerId" placeholder="右プレイヤーIDを入力">
          </div>
          <button type="submit" class="btn btn-primary">送信</button>
      </form>
    </div>
  `
};

export function setupInitMatch() {
  const formEle = document.querySelector(".js-match-form");
  formEle.addEventListener("submit", (event) => {
    const matchId = event.target.matchId;
    const leftPlayerId = event.target.leftPlayerId;
    const rightPlayerId = event.target.rightPlayerId;
    if (!matchId || !leftPlayerId || !rightPlayerId) {
      alert("全てのフィールドを入力してください。");
      return;
    }
    stateManager.setState({ matchId: matchId });
    stateManager.setState({ players: [leftPlayerId, rightPlayerId] });
  });
}
