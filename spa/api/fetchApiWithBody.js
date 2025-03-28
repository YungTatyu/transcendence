/**
 * データをリクエストボディに含めるAPIリクエスト関数
 * WARN レスポンスはJSON形式である必要がある
 * @param {string} method - HTTPメソッド (例: "POST", "PUT")
 * @param {string} baseUrl - URL (例: "http://localhost:8080")
 * @param {string} endpoint - APIエンドポイント (例: "/auth/otp/login")
 * @param {object} requestBody - リクエストボディ (JSON)
 * @returns {Promise<{status: number | null, data: any}>} - ステータスとデータ
 */
export default async function fetchApiWithBody(
  method,
  baseUrl,
  endpoint,
  requestBody,
) {
  try {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method,
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    const status = response.status;
    const data = await response.json();
    return { status, data };
  } catch (error) {
    console.error(`API fetch error at ${endpoint}:`, error);
    return { status: null, data: null };
  }
}
