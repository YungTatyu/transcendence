function get_fill_size(players_size) {
	let fill_size = 1;
	for (let i = 2;; i *= 2) {
		if (players_size <= i) {
			return fill_size;
		}
		fill_size *= 2;
	}
}

function generateTournamentData(players) {
	let tournamentData = {
		teams: [],
		results: [],
	}
	const number_of_players = players.length;

	// Create teams
	tournamentData.teams = Array(get_fill_size(number_of_players)).fill().map(() => ["bye", "bye"]);
	const number_of_combinations = tournamentData.teams.length;
	for (let i = 0; i < number_of_players; i++) {
		tournamentData.teams[i % number_of_combinations][i >= number_of_combinations ? 1 : 0] = players[i];
	}

	// Create results
	for (let i = 1; i < number_of_players; i *= 2) {
		tournamentData.results.push(Array(i).fill().map(() => [0, 0]));
	}
	tournamentData.results.sort((a, b) => b.length - a.length);

	// Fill bye -1
	for (let i = 0; i < number_of_combinations; i++) {
		if (tournamentData.teams[i][1] === "bye") {
			tournamentData.results[0][i][1] = -1;
		}
	}
    return tournamentData;
}
