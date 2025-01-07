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
      message: this.message_
    }
  }
  copyObj(obj) {
    if (obj.timer) {
      this.timer_ = obj.timer;
      //timer evetnの時は、messageをupdateしない
      return
    }
    if (obj.message) {
      this.message_ = obj.message;
    }

  }
}

const gameState = new Game()
const ws = new WebSocket(`ws://127.0.0.1:8000/ws/game`)

async function send() {
  gameState.message = document.querySelector(".js-input").value
  await ws.send(JSON.stringify(gameState.toObj()))
}

function main() {
  ws.onopen = function(e) {
    console.log("ws connection established")
  }

  ws.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const timerEle = document.querySelector(".js-timer")
    const inputEle = document.querySelector(".js-input")
    const gameEle = document.querySelector(".js-game")
    gameState.copyObj(data)
    timerEle.innerText = gameState.timer
    inputEle.value = gameState.message
    gameEle.textContent = gameState.message
    if (data.timer === 0) {
      alert("game over")
    }
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
