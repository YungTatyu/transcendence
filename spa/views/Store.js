import Footer from "../components/Footer.js";
import Header from "../components/Header.js";
import stateManager from "../stateManager.js";

export default function Store() {
  return `
    ${Header({ title: "store" })}
    <p>カウント: <span id="count">${stateManager.state.count}</span></p>
    <button id="incrementButton">カウントを増やす</button>
    <button onclick="SPA.navigate('/')">homeへ</button>
    ${Footer({ text: "© 2025 My Company" })}
  `;
}

export function setupStore() {
  const incrementButton = document.getElementById("incrementButton");
  const countDisplay = document.getElementById("count");

  incrementButton.addEventListener("click", () => {
    stateManager.setState({ count: stateManager.state.count + 1 });
  });

  stateManager.subscribe((newState) => {
    countDisplay.textContent = newState.count;
  });
}
