export default function MatchingInfo() {
  return `
    <p id="matching-info" class="d-flex justify-content-center align-items-center"></p>
  `;
}

export function renderMatchingInfo(text, color) {
  const matchingInfo = document.getElementById("matching-info");
  matchingInfo.innerHTML = text;
  matchingInfo.style.color = color;
}
