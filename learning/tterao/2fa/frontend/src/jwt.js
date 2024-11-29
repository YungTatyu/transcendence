export function decodeJwt(token) {
  const payload = token.split('.')[1];
  return JSON.parse(atob(payload));
}
