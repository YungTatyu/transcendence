import SPA from "./spa.js";

export default function GameHome() {
  return `
        <img src="./assets/user.png" class="profile-icon js-btn-profile">
        <img src="./assets/friend.png" class="friend-icon js-btn-friend">
        <div class="d-flex vh-100 align-items-center justify-content-center text-center">
            <div class="d-grid gap-4 col-4 mx-auto">
                <button class="btn btn-primary btn-quickplay js-btn-quickplay" type="button">Quick Play</button>
                <button class="btn btn-primary btn-tournament js-btn-tournament" type="button">Tournament</button>
            </div>
        </div>
    `;
}

export function setupGameHome() {
  const profileButton = document.querySelector(".js-btn-profile");
  const friendButton = document.querySelector(".js-btn-friend");

  const quickplayButton = document.querySelector(".js-btn-quickplay");
  const tournamentButton = document.querySelector(".js-btn-tournament");

  profileButton.addEventListener("click", () => {
    SPA.navigate("/profile");
  });
  friendButton.addEventListener("click", () => {
    SPA.navigate("/friend");
  });
  quickplayButton.addEventListener("click", () => {
    SPA.navigate("/matching/quick-play");
  });
  tournamentButton.addEventListener("click", () => {
    SPA.navigate("/matching/tournament");
  });
}
