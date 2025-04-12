export default function NeonInfo() {
  return `
      <p id="neon-info" class="d-flex justify-content-center align-items-center">
      </p>
	`;
}

export function renderNeonInfo(text, color) {
  const neonInfo = document.getElementById("neon-info");
  neonInfo.innerHTML = text;
  neonInfo.style.color = color;
  neonInfo.style.textShadow = "${color} 1px 0 10px";
  neonInfo.style.fontSize = "4rem";
  neonInfo.style.fontWeight = "bold";
  neonInfo.style.filter = "blur(1px)";
}
