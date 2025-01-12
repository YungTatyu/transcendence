var loc = window.location;
var uri = (loc.protocol === 'https:') ? "wss:" : "ws:";
uri += '//' + window.location.host + loc.pathname + 'tournaments/ws/enter-room';
const ws = new WebSocket(uri);

ws.onmessage = function(event) {
	console.log("DEBUGDESU!")
	const sentData = JSON.parse(event.data);
	console.log(sentData);
};

ws.onerror = function(error) { console.error("WebSocket error:", error); };
ws.onclose = function() { console.log("WebSocket connection closed."); };
