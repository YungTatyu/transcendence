const config = {
  development: {
    userService: "http://localhost:9000",
    matchService: "http://localhost:8003",
    gameService: "http://localhost:8001",
    realtimeGameService: "wss://game:8001",
    authService: "https://auth:8000",
  },
  production: {
    userService: "",
    matchService: "",
    gameService: "",
    realtimeGameService: "",
    authService: "",
  },
};

const currentEnv =
  window.location.hostname === "localhost" ? "development" : "production";

export default config[currentEnv];
