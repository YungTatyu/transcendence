class Game {
  constructor() {
    /** @private */
    this.message_ = ""
    /** @private */
    this.timer_ = 60
  }

  get message() { return this.message_ }
  set message(message) { this.message_ = message }
  get timer() { return this.timer_ }
  set timer(timer) { this.timer_ = timer }
  toObj() {
    return {
      message: this.message_,
      timer: this.timer_
    }
  }
  copyObj(obj) {
    this.message_ = obj.message
    this.timer_ = obj.timer
  }
}

const gameState = new Game()
const ws = new WebSocket(`ws://127.0.0.1:8000/ws/game`)

function startTimer() {
  gameState.timer = 60
  const timerEle = document.querySelector(".js-timer").innerText = gameState.timer
  const timerInterval = setInterval(() => {
    if (gameState.timer > 0) {
      gameState.timer = gameState.timer - 1
      send();
    } else {
      clearInterval(timerInterval);
      alert("Game Over!");
    }
  }, 1000);
}

async function send() {
  gameState.message = document.querySelector(".js-input").value
  await ws.send(JSON.stringify(gameState.toObj()))
}

function main() {
  startTimer()
  ws.onopen = function(e) {
    console.log("ws connection established")
  }

  ws.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const timerEle = document.querySelector(".js-timer")
    const gameEle = document.querySelector(".js-game")
    gameState.copyObj(data)
    timerEle.innerText = data.timer
    gameEle.textContent += data.message
    console.log("onmessage", data)
  }

  ws.onclose = function(e) {
    console.error("error: ", e)
  }

  document.querySelector(".js-input")?.addEventListener("input", (e) => {
    send()
  })
}

main()
