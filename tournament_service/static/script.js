const loc = window.location;
const wsProtocol = (loc.protocol === 'https:') ? "wss:" : "ws:";
const tournamentMatchingUrl = `${wsProtocol}//${loc.host}${loc.pathname}tournaments/ws/enter-room`;

const tournamentStartTimeElement = document.getElementById('tournamentStartTime');
const tournamentMatchingWsHandler = new TournamentMatchingWsHandler(tournamentMatchingUrl, tournamentStartTimeElement);
tournamentMatchingWsHandler.connect();
