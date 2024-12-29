const gameState = {
  message: "",
  timer: 60
}

const ws = new WebSocket(`ws://127.0.0.1:8000/ws/game`)

function startTimer() {
  gameState.timer = 60;
  const timerInterval = setInterval(() => {
    if (gameState.timer > 0) {
      gameState.timer -= 1;
      send();
    } else {
      clearInterval(timerInterval);
      alert("Game Over!");
    }
  }, 1000);
}

async function send() {
  gameState.message = document.querySelector(".js-input").value
  await ws.send(JSON.stringify(gameState))
}

function main() {
  ws.onopen = function(e) {
    console.log("ws connection established")
  }

  ws.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const gameEle = document.querySelector(".js-game")
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
