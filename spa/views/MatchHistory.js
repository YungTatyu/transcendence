import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function MatchHistory() {
  // function MatchHistoryData() {
  //   const playerAvatar = "/assets/user.png";
  //   //APIから取得した値で上書する
  //   return `
  // <div class="row row-cols-5 mt-2">
  //   <div class="col">loading...</div>
  //   <div class="col text-center">
  //     <img src="${playerAvatar}" alt="ロゴ" class="square-img rounded-circle me-2" >
  //     <span>loading...</span>
  //   </div>
  //   <div class="col">loading...</div>
  //   <div class="col">loading...</div>
  //   <div class="col">loading...</div>
  // </div>
  //     `;
  // }
  return `

    ${TitleAndHomeButton("MATCH HISTORY")}

    <div class="container text-center match-history-container">
      <div class="row row-cols-5 match-history-table-header">
        <div class="col">MODE</div>
        <div class="col">PLAYER</div>
        <div class="col">RESULT</div>
        <div class="col">SCORE</div>
        <div class="col">DATE</div>
      </div>

      <div class="match-history-table">
      </div>
    </div>  

  `;
}

export const setupMatchHistory = async () => {
  const matchHistoryTable = document.querySelector(".match-history-table");
  matchHistoryTable.innerHTML = "";
  let currentPage = 0;
  const limit = 10;
  myUserId = stateManager.state?.userId;

  async function loadHistory(offset, limit) {
    userHistory = fetchApiNoBody(
      "GET",
      config.matchService,
      `/matches/statistics/${myUserId}?offset=${offset}&limit=${limit}`,
    );
    if (userHistory.status === null) {
      console.error("Error Occured");
      return;
    }
    if (userHistory.status >= 400) {
      console.error(userHistory.data.error);
      return;
    }
    if (userHistory.length === 0) {
      window.removeEventListener("scroll", handleScroll); // スクロールイベントを削除
      return;
    }
    await Promise.all(
      userHistory.data.map(async (matchResult) => {
        const matchItem = document.createElement("div");
        const opponent = await fetchUserNameAndAvatar(
          "Get",
          config.friendService,
          `/users?userid=${matchResult.opponents.id}`,
        );
        if (opponent.status === null) {
          console.error("Error Occured");
          return;
        }
        if (opponent.status >= 400) {
          console.error(opponent.data.error);
          return;
        }
        const avatarImg = `${config.userService}${friend.data.avatarPath}`;
        const score = `${matchResult.userScore}-${matchResult.opponent.score}`;
        matchItem.innerHTML = `
        <div class="row row-cols-5 mt-2">
          <div class="col">${matchResult.mode}</div>
          <div class="col text-center">
            <img src=${avatarImg} alt="ロゴ" class="square-img rounded-circle me-2" >
            <span>${opponent.username}</span>
          </div>
          <div class="col">${matchResult.result}</div>
          <div class="col">${score}</div>
          <div class="col">${matchResult.date}</div>
          </div>
        `;
        matchHistoryTable.appendChild(matchItem);
      }),
    );
    currentPage++;
  }

  async function handleScroll() {
    if (loading) return;

    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
      // 誤差を考慮
      loading = true;
      await loadHistory(currentPage * limit, limit);
      loading = false;
    }
  }

  let loading = false;
  loadHistory(currentPage * limit, limit);
  window.addEventListener("scroll", handleScroll);
};
