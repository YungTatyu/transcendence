var loc = window.location;
var uri = (loc.protocol === 'https:') ? "wss:" : "ws:";
uri += '//' + window.location.host + loc.pathname + 'tournaments/ws/enter-room';
const ws = new WebSocket(uri);

const tournamentStartTime = document.getElementById('tournamentStartTime');

ws.onmessage = function(event) {
	const sentData = JSON.parse(event.data);
	if (sentData.tournament_id) {
		console.log(sentData.tournament_id);
		ws.close();
	} else if (sentData.tournament_start_time) {
		if (sentData.tournament_start_time === "None") {
			tournamentStartTime.style.display = "none";
		} else {
			tournamentStartTime.style.display = "block";
			tournamentStartTime.textContent = calcRemainingTime(sentData.tournament_start_time);
		}
		console.log(sentData.tournament_start_time);
	} else {
		console.log("Error");
	}
};

function calcRemainingTime(tournamentStartTimeString) {
	const start_time = parseFloat(tournamentStartTimeString);
	const currentUnixTime = Date.now() / 1000;
	const remainingTime = Math.round(start_time - currentUnixTime);
	return remainingTime;
}

ws.onerror = function(error) { console.error("WebSocket error:", error); };
ws.onclose = function() { console.log("WebSocket connection closed."); };
