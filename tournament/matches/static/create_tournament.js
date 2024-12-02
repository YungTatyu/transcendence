$(document).ready(function() {
  $('#tournamentForm').on('submit', function(e) {
    e.preventDefault();

    let players = [];
    for (let i = 1; i <= 8; i++) {
      let playerName = $(`#player${i}`).val().trim();
      if (playerName) {
        players.push(playerName);
      }
    }
    let ownerUser = $('#ownerUser').val().trim();

    let tournamentData = {
      players: players,
      owner_user: ownerUser
    };

    $.ajax({
	  url: 'http://localhost:8000/api/tournament/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(tournamentData),
      success: function(response) {
		const tournamentData = generateTournamentData(response.players);
		console.log(JSON.stringify(tournamentData, null, 2));

		$("#bracket").bracket({
			init: tournamentData,
			skipConsolationRound: true, // 敗者復活戦をスキップ
			teamWidth: 150, // チーム名の表示幅調整
			matchWidth: 70 // 試合間の幅調整
		});
		$('.team .label').filter(function() {
			return $(this).text() === 'bye';
		}).closest('.team').css('visibility', 'hidden');
      },
      error: function(xhr, status, error) {
        alert('エラーが発生しました: ' + error);
        console.error(error);
      }
    });
  });
});
