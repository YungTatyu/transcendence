import fetchApiNoBody from "../../api/fetchApiNoBody.js";
import config from "../../config.js";

export default function TournamentBracket() {
  return `
      <div class="d-flex justify-content-center">
        <div id="bracket"></div>
      </div>
	`;
}

export async function renderTournamentBracket(data) {
  data.teams = await convertIdToNameInTeams(data.teams);
  $("#bracket").bracket({
    init: data,
    skipConsolationRound: true, // 敗者復活戦をスキップ
    teamWidth: 150, // チーム名の表示幅調整
    scoreWidth: 50, // スコアの横幅の表示幅調整
    matchMargin: 100, // 試合間隔を調整
    roundMargin: 100, // ラウンドの間隔調整
  });
}

async function convertIdToNameInTeams(teams) {
  return Promise.all(
    teams.map(async (team) => {
      return Promise.all(team.map((id) => convertIdToName(id)));
    }),
  );

  async function convertIdToName(id) {
    const response = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?userid=${id}`,
    );

    // ErrorならuserIdで描画
    if (response.status === null || response.status >= 400) {
      return id;
    }
    return response.data.username;
  }
}
