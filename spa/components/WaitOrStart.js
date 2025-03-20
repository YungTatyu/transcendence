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
	waitOrStart.style.textShadow = '0 0 10px #FFFFFF, 0 0 20px #FFFFFF, 0 0 30px #FFFFFF';
}
