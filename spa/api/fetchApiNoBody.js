/**
 * データをリクエストボディに含めないAPIリクエスト関数
 * @param {string} method - HTTPメソッド (例: "POST", "PUT")
 * @param {string} baseUrl - URL (例: "http://localhost:8080")
 * @param {string} endpoint - APIエンドポイント (例: "/auth/otp/login")
 * @returns {Promise<{status: number | null, data: any}>} - ステータスとデータ
 */
export default async function fetchApiNoBody(method, baseUrl, endpoint) {
  try {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method,
      credentials: "include",
    });

    const status = response.status;
    const data = await response.json();
    return { status, data };
  } catch (error) {
    console.error(`API fetch error at ${endpoint}:`, error);
    return { status: null, data: null };
  }
}
