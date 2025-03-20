export default function MatchingRoom() {
	return `
      <div class="container" id="matching-room-container">
        <div id="matching-room" class="row"></div>
      </div>
	`;
}

export function renderMatchingRoom(users) {
	const room = document.getElementById("matching-room");
	room.innerHTML = "";
	room.style.display = "grid"; // Grid レイアウトを適用

	users.forEach(user => {
		const div = document.createElement("div");
		div.classList.add("matching-room-user");

		const avatarImg = document.createElement("img");
		avatarImg.src = user.avatarPath;
		avatarImg.alt = "";
		div.appendChild(avatarImg);

		const nameText = document.createElement("p");
		nameText.textContent = user.name;
		div.appendChild(nameText);

		room.appendChild(div);
	});
	updateSizes();
}

function updateSizes() {
	const container = document.getElementById("matching-room");
	if (!container) return;

	const items = container.children;
	const count = items.length;
	if (count === 0) return;

	const cols = Math.ceil(Math.sqrt(count));
	const rows = Math.ceil(count / cols);

	// グリッドの列と行の数を設定
	container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
	container.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
}
