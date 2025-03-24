export default function WaitOrStart() {
  return `
      <p id="wait-or-start" class="d-flex justify-content-center align-items-center">
      </p>
	`;
}

export function changeWaitIntoStart() {
  const waitOrStart = document.getElementById("wait-or-start");
  waitOrStart.innerHTML = "START";
  waitOrStart.style.color = "#ffffff";
  waitOrStart.style.textShadow = "#ffffff 1px 0 10px";
  waitOrStart.style.fontSize = "4rem";
  waitOrStart.style.fontWeight = "bold";
  waitOrStart.style.filter = "blur(1px)";
}

export function changeStartIntoWait() {
  const waitOrStart = document.getElementById("wait-or-start");
  waitOrStart.innerHTML = "WAIT...";
  waitOrStart.style.color = "#0ca5bf";
  waitOrStart.style.textShadow = "#0ca5bf 1px 0 10px";
  waitOrStart.style.fontSize = "4rem";
  waitOrStart.style.fontWeight = "bold";
  waitOrStart.style.filter = "blur(1px)";
}
