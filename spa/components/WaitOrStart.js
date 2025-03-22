export default function WaitOrStart() {
  return `
      <p id="wait-or-start" class="d-flex justify-content-center align-items-center">
        WAIT...
      </p>
	`;
}

export function changeWaitIntoStart() {
  const waitOrStart = document.getElementById("wait-or-start");
  waitOrStart.innerHTML = "START";
  waitOrStart.style.color = "white";
  waitOrStart.style.textShadow = "#FFFFFF 1px 0 10px";
}
