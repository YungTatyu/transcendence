const config = {
  development: {
    userService: 'http://localhost:9000',
    matchService: 'http://localhost:8003',
    gameService: 'http://localhost:8001',
  },
  production: {
    userService: '',
    matchService: '',
    gameService: '',
  },
};

const currentEnv = window.location.hostname === 'localhost' ? 'development' : 'production';

export default config[currentEnv];
