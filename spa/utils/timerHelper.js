/**
 * 指定された終了時間までの残り時間を計算する関数
 *
 * @param {number} endTime - 終了時刻
 * @returns {number} 現在時刻から `endTime` までの残り時間（秒単位、0以上）
 */
export const calcRemaingTime = (endTime) => {
  const now = Date.now(); // 現在時刻（ミリ秒）
  const re = Math.max(0, Math.floor((endTime - now) / 1000)); // 残り時間（秒単位）
  return re;
};
