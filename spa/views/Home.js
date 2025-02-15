import Header from "../components/Header.js";
import Footer from "../components/Footer.js";
import stateManager from "../stateManager.js";

export default function Home() {
    return `
        ${Header({ title: "ホーム" })}
        <p>これはホームページです。</p>
        <button onclick="SPA.navigate('/store')">storeへ</button>
        <button onclick="SPA.navigate('/404')">404へ</button>
        ${Footer({ text: "© 2025 My Company" })}
        <div> store sample</div>
        ${stateManager.state.count}
    `;
}
