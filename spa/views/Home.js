import Footer from "../components/Footer.js";
import Header from "../components/Header.js";
import stateManager from "../stateManager.js";

export default function Home() {
  return `
        ${Header({ title: "ホーム" })}
        <p>これはホームページです。</p>
        <img src="./assets/42.png" alt="ロゴ">
        <button onclick="SPA.navigate('/store')">storeへ</button>
        <button onclick="SPA.navigate('/api')">APIへ</button>
        <button onclick="SPA.navigate('/404')">404へ</button>
        <button onclick="SPA.navigate('/profile')">profileへ</button>
        <button onclick="SPA.navigate('/history/match')">Match Historyへ</button>
        <button onclick="SPA.navigate('/signup')">signupへ</button>
        <button onclick="SPA.navigate('/login')">loginへ</button>
        <button onclick="SPA.navigate('/profile/username')">changeUsernameへ</button>
        <button onclick="SPA.navigate('/profile/mail')">changeMailへ</button>
        <button onclick="SPA.navigate('/profile/password')">changePasswordへ</button>
        <button onclick="SPA.navigate('/profile/avatar')">changeAvatarへ</button>

        <button onclick="SPA.navigate('/game')">gameへ</button>
        <button onclick="SPA.navigate('/game/setup')">setupgameへ</button>
        <button onclick="SPA.navigate('/game/result')">gameresultへ</button>
        ${Footer({ text: "© 2025 My Company" })}
        <div> store sample</div>
        ${stateManager.state.count}
    `;
}
