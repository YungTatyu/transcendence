const config = {
  development: {
    userService: "http://localhost:9000",
    matchService: "http://localhost:8003",
    gameService: "http://localhost:8001",
    realtimeGameService: "ws://localhost:8001",
    authService: "http://localhost:8000",
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
