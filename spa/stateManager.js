const stateManager = {
    state: {
        count: 0,
        items: [],
    },
    listeners: [],
    setState(newState) {
      this.state = { ...this.state, ...newState };
      this.listeners.forEach((listener) => listener(this.state));
    },
    subscribe(listener) {
      this.listeners.push(listener);
    },
  };
  
  export default stateManager;
  