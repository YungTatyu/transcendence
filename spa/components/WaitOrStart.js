export default function WaitOrStart() {
  return `
      <p id="wait-or-start" class="d-flex justify-content-center align-items-center">
      </p>
	`;
}

export function renderWaitOrStart(text, color) {
  const waitOrStart = document.getElementById("wait-or-start");
  waitOrStart.innerHTML = text;
  waitOrStart.style.color = color;
  waitOrStart.style.textShadow = "${color} 1px 0 10px";
  waitOrStart.style.fontSize = "4rem";
  waitOrStart.style.fontWeight = "bold";
  waitOrStart.style.filter = "blur(1px)";
}
