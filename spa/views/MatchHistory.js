import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function MatchHistory() {
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

const scrollHandler = {
  loading: false,
  currentPage: 0,
  limit: 15,
  async loadHistory() {
    if (this.loading) return;
    this.loading = true;
    const matchHistoryTable = document.querySelector(".match-history-table");
    if (!matchHistoryTable) {
      return;
    }
    const offset = this.currentPage * this.limit;
    const myUserId = stateManager.state?.userId;
    const userHistory = await fetchApiNoBody(
      "GET",
      config.matchService,
      `/matches/histories/${myUserId}?offset=${offset}&limit=${this.limit}`,
    );
    if (userHistory.status === null) {
      console.error("Error Occured");
      return;
    }
    if (userHistory.status >= 400) {
      console.error(userHistory.data.error);
      return;
    }
    if (userHistory.data.total <= offset + this.limit) {
      window.removeEventListener("scroll", this.handleScroll); // スクロールイベントを削除
    }
    await Promise.all(
      userHistory.data.results.map(async (matchResult) => {
        const matchItem = document.createElement("div");
        const opponent = await fetchApiNoBody(
          "GET",
          config.userService,
          `/users?userid=${matchResult.opponents[0].id}`,
        );
        if (opponent.status === null) {
          console.error("Error Occured");
          return;
        }
        if (opponent.status >= 400) {
          console.error(opponent.data.error);
          return;
        }
        const avatarImg = `${config.userService}${opponent.data.avatarPath}`;
        const score = `${matchResult.userScore} - ${matchResult.opponents[0].score}`;
        const resultColor =
          matchResult.result === "win" ? "#0CC0DF" : "#FF0004";
        matchItem.innerHTML = `
        <div class="row row-cols-5 mt-2">
          <div class="col">${matchResult.mode}</div>
          <div class="col text-center">
            <img src=${avatarImg} alt="ロゴ" class="square-img rounded-circle me-2" >
            <span>${opponent.data.username}</span>
          </div>
          <div class="col" style="color: ${resultColor}">${matchResult.result}</div>
          <div class="col">${score}</div>
          <div class="col">${matchResult.date}</div>
          </div>
        `;
        try {
          matchHistoryTable.appendChild(matchItem);
        } catch (error) {
          console.log("MatchHistory appendChild Error");
        }
      }),
    );
    this.currentPage++;
    this.loading = false;
  },
  async handleScroll() {
    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
      // 誤差を考慮
      await scrollHandler.loadHistory();
    }
  },
  destructor() {
    this.currentPage = 0;
    this.loading = false;
  },
};

export const setupMatchHistory = async () => {
  const matchHistoryTable = document.querySelector(".match-history-table");
  if (!matchHistoryTable) {
    return;
  }
  matchHistoryTable.innerHTML = "";

  await scrollHandler.loadHistory();
  window.addEventListener("scroll", scrollHandler.handleScroll);
};

export const cleanupMatchHistory = () => {
  window.removeEventListener("scroll", scrollHandler.handleScroll);
  scrollHandler.destructor();
  console.log("Scroll event removed");
};
