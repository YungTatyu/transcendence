export default function Tournament() {
  return `<div id="bracket"></div>`;
}

export function setupTournament() {
  const tournamentData = {
    teams: [
      ["Team 1", "Team 2"],
      ["Team 3", null],
      ["Team 4", null],
      ["Team 5", null],
    ],
    results: [
      [
        [
          [1, 0],
          [null, null],
          [null, null],
          [null, null],
        ],
        [
          [null, null],
          [1, 4],
        ],
        [
          [null, null],
          [null, null],
        ],
      ],
    ],
  };
  renderTournament(tournamentData);
}

function renderTournament(data) {
  $("#bracket").bracket({
    init: data,
    skipConsolationRound: true, // 敗者復活戦をスキップ
    teamWidth: 150, // チーム名の表示幅調整
    matchWidth: 70, // 試合間の幅調整
  });
}
