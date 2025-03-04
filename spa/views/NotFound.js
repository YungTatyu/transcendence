export default function NotFound() {
  return `
        <h1>404 Not Found</h1>
        <p>ページが見つかりません。</p>
        <button onclick="SPA.navigate('/')">ホームへ戻る</button>
    `;
}
