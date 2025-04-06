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

const testHistoryData = {
  total: 42,
  offset: 0,
  limit: 2,
  results: [
    {
      mode: "QuickPlay",
      result: "win",
      date: "2024-12-09",
      userScore: 11,
      opponents: [
        {
          id: 1,
          score: 5,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 10,
      opponents: [
        {
          id: 2,
          score: 12,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "lose",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 50,
        },
      ],
    },
    {
      mode: "Tournament",
      result: "win",
      date: "2024-12-01",
      userScore: 50,
      opponents: [
        {
          id: 2,
          score: 70,
        },
      ],
    },
  ],
};

const testUserData = {
  userId: 0,
  username: "player",
  avatarPath: "/assets/42.png",
};

export const setupMatchHistory = async () => {
  const matchHistoryTable = document.querySelector(".match-history-table");
  matchHistoryTable.innerHTML = "";
  let currentPage = 0;
  const limit = 15;
  const myUserId = stateManager.state?.userId;

  async function loadHistory(offset, limit) {
    // 本番用
    // userHistory = fetchApiNoBody(
    //   "GET",
    //   config.matchService,
    //   `/matches/histories/${myUserId}?offset=${offset}&limit=${limit}`,
    // );
    // if (userHistory.status === null) {
    //   console.error("Error Occured");
    //   return;
    // }
    // if (userHistory.status >= 400) {
    //   console.error(userHistory.data.error);
    //   return;
    // }
    // if (userHistory.length === 0) {
    //   window.removeEventListener("scroll", handleScroll); // スクロールイベントを削除
    //   return;
    // }
    // await Promise.all(
    //   userHistory.data.results.map(async (matchResult) => {
    //     const matchItem = document.createElement("div");
    //     const opponent = await fetchUserNameAndAvatar(
    //       "GET",
    //       config.friendService,
    //       `/users?userid=${matchResult.opponents[0].id}`,
    //     );
    //     if (opponent.status === null) {
    //       console.error("Error Occured");
    //       return;
    //     }
    //     if (opponent.status >= 400) {
    //       console.error(opponent.data.error);
    //       return;
    //     }
    //     const avatarImg = `${config.userService}${friend.data.avatarPath}`;
    //     const score = `${matchResult.userScore} - ${matchResult.opponent[0].score}`;
    //     matchItem.innerHTML = `
    //     <div class="row row-cols-5 mt-2">
    //       <div class="col">${matchResult.mode}</div>
    //       <div class="col text-center">
    //         <img src=${avatarImg} alt="ロゴ" class="square-img rounded-circle me-2" >
    //         <span>${opponent.username}</span>
    //       </div>
    //       <div class="col">${matchResult.result}</div>
    //       <div class="col">${score}</div>
    //       <div class="col">${matchResult.date}</div>
    //       </div>
    //     `;
    //     matchHistoryTable.appendChild(matchItem);
    //   }),
    // );

    // テスト用
    const userHistory = testHistoryData.results.slice(offset, offset + limit);
    await Promise.all(
      userHistory.map(async (matchResult) => {
        const matchItem = document.createElement("div");
        const opponent = testUserData;
        const avatarImg = testUserData.avatarPath;
        const score = `${matchResult.userScore} - ${matchResult.opponents[0].score}`;
        const resultColor =
          matchResult.result === "win" ? "#0CC0DF" : "#FF0004";
        matchItem.innerHTML = `
        <div class="row row-cols-5 mt-2">
          <div class="col">${matchResult.mode}</div>
          <div class="col text-center">
            <img src=${avatarImg} alt="ロゴ" class="square-img rounded-circle me-2" >
            <span>${opponent.username}</span>
          </div>
          <div class="col" style="color: ${resultColor}">${matchResult.result}</div>
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
