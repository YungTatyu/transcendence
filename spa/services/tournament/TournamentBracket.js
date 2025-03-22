export default function TournamentBracket() {
  return `<div id="bracket"></div>`;
}

export function renderTournamentBracket(data) {
  $("#bracket").bracket({
    init: data,
    skipConsolationRound: true, // 敗者復活戦をスキップ
    teamWidth: 150, // チーム名の表示幅調整
    matchWidth: 70, // 試合間の幅調整
  });
}
