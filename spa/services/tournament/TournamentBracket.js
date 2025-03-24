export default function TournamentBracket() {
  return `
      <div class="d-flex justify-content-center">
        <div id="bracket"></div>
      </div>
	`;
}

export function renderTournamentBracket(data) {
  $("#bracket").bracket({
    init: data,
    skipConsolationRound: true, // 敗者復活戦をスキップ
    teamWidth: 150, // チーム名の表示幅調整
    scoreWidth: 50, // スコアの横幅の表示幅調整
    matchMargin: 100, // 試合間隔を調整
    roundMargin: 100, // ラウンドの間隔調整
  });
}
