const config = {
  development: {
    userService: "http://localhost:9000",
    matchService: "http://localhost:8003",
    gameService: "http://localhost:8001",
    realtimeGameService: "ws://localhost:8001",
    authService: "http://localhost:8000",
    friendService: "http://localhost:7500",
  },
  production: {
    userService: "https://user-proxy.transcen.com:8009",
    matchService: "https://match-proxy.transcen.com:8008",
    matchMatchingService: "wss://match-proxy.transcen.com:8008",
    gameService: "https://game-proxy.transcen.com:8004",
    realtimeGameService: "wss://game-proxy.transcen.com:8004",
    authService: "https://auth-proxy.transcen.com:8005",
    friendService: "https://friends-proxy.transcen.com:8007",
  },
};

const currentEnv =
  window.location.hostname === "localhost" ? "development" : "production";

export default config[currentEnv];
