import { fetchData } from "../api.js";
import stateManager from "../stateManager.js";

const ApiData = () => {
  const state = stateManager.state;
  return `
        <div>
            <h1>APIData Page</h1>
            <button id="fetch-data">データ取得</button>
            <button id="delete-data">データ消去</button>
            <ul id="data-list">
                ${state.items ? state.items.map((item) => `<li>${item.title}</li>`).join("") : "no data"}
            </ul>
        </div>
    `;
};

export function setupApiData() {
  document.getElementById("fetch-data").addEventListener("click", async () => {
    const data = await fetchData("/posts"); // 仮のエンドポイント
    if (data) {
      stateManager.setState({ items: data.slice(0, 5) });
    }
  });

  document.getElementById("delete-data").addEventListener("click", async () => {
    stateManager.setState({ items: [] });
  });

  stateManager.subscribe(() => {
    const list = document.getElementById("data-list");
    if (list) {
      list.innerHTML = stateManager.state.items
        ? stateManager.state.items
            .map((item) => `<li>${item.title}</li>`)
            .join("")
        : "";
    }
  });
}

export default ApiData;
