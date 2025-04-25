// このパラメータのみ、sessionStorageに保存する
const PERSIST_KEYS = ["tournamentId", "matchId", "players"];

const stateManager = {
  state: {
    userId: null,
    username: null,
    avatarUrl: null,
    tournamentId: null,
    matchId: null,
    players: null,
    onlineUsers: null,
  },
  listeners: [],

  // 初期化で sessionStorage から復元
  init() {
    for (const key of PERSIST_KEYS) {
      const stored = sessionStorage.getItem(key);
      if (stored !== null) {
        try {
          this.state[key] = JSON.parse(stored);
        } catch {
          this.state[key] = stored;
        }
      }
    }
  },

  setState(newState) {
    for (const key in newState) {
      // 特定のパラメータのみsessionStorageに保存する
      if (PERSIST_KEYS.includes(key)) {
        sessionStorage.setItem(key, JSON.stringify(newState[key]));
      }
      this.state[key] = newState[key];
    }

    for (const listener of this.listeners) {
      listener(this.state);
    }
  },

  subscribe(listener) {
    this.listeners.push(listener);
  },
};

stateManager.init();

export default stateManager;
