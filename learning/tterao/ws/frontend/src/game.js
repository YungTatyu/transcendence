function main() {
  const gameEle = document.querySelector((".js-game"))
  const ws = new WebSocket(`ws://127.0.0.1:8000/ws/game`)

  ws.onmessage = function(e) {
    console.log("ws connection established")
  }

  ws.onmessage = function(e) {
    const data = JSON.parse(e.data)
    gameEle.value += data.message
    console.log("onmessage", data)
  }

  ws.onclose = function(e) {
    console.error("error: ", e)
  }

  document.querySelector(".js-input")?.addEventListener("input", (e) => {
    console.log("input event")
    ws.send(JSON.stringify({ "message": e.value }))
  })
}

main()
