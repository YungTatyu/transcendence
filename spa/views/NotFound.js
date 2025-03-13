export default function NotFound() {
  return `
        <h1 class="number">404</h1>
        <p class="text">Not Found</p>
        <button onclick="SPA.navigate('/')">ホームへ戻る</button>
    `;
}
