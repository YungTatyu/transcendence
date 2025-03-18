const stateManager = {
  state: {
    count: 0,
    items: [],
    userId: null,
    username: null,
    avatar_path: null,
  },
  listeners: [],
  setState(newState) {
    this.state = { ...this.state, ...newState };
    for (const listener of this.listeners) {
      listener(this.state);
    }
  },
  subscribe(listener) {
    this.listeners.push(listener);
  },
};

export default stateManager;
