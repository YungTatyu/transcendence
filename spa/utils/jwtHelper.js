import config from "../config.js";
import stateManager from "../stateManager.js";
import WsFriendActivityManager from "../services/friend_activity/WsFriendActivityManager.js";

export const parseJwt = (token) => {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");

  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map((c) => `%${`00${c.charCodeAt(0).toString(16)}`.slice(-2)}`)
      .join(""),
  );
  return JSON.parse(jsonPayload);
};

const fetchAccessToken = async () => {
  const res = await fetch(`${config.authService}/auth/token/refresh`, {
    method: "POST",
    credentials: "include",
  });
  if (res.status >= 400) {
    location.replace("/");
    return null;
  }
  const data = await res.json();
  const accessToken = data.accessToken;
  const payload = parseJwt(accessToken);
  const userId = payload.user_id;
  stateManager.setState({ userId: Number.parseInt(userId) });
  sessionStorage.setItem("access_token", accessToken);
  return payload;
};

/**
 * JWTの有効期限に基づいて、期限の10分前にトークンを自動更新する処理をスケジュールします。
 * accessToken を取得（または更新）したタイミングで呼び出す必要があります。
 *
 * @param {Object} payload - JWTのデコード済みペイロード
 */
export const scheduleRefresh = (payload) => {
  const now = Date.now(); // ミリ秒
  const exp = payload.exp * 1000; // expは秒なのでミリ秒に変換
  const tenMins = 10 * 60 * 1000;
  // WARN: jwtの有効期限は10分以下ではないこと
  const delayUntilRefresh = exp - tenMins - now;
  // JWTの更新タイミング：期限の10分前
  setInterval(fetchAccessToken, delayUntilRefresh);
};

export const handleLoading = async () => {
  const skipPaths = ["/login", "/signup"];
  const currentPath = location.pathname;
  if (
    currentPath === "/" ||
    skipPaths.some((path) => currentPath.startsWith(path))
  ) {
    return;
  }
  const payload = await fetchAccessToken();
  if (payload === null) {
    return;
  }
  WsFriendActivityManager.disconnect();
  WsFriendActivityManager.connect(sessionStorage.getItem("access_token"));
  scheduleRefresh(payload);
};
