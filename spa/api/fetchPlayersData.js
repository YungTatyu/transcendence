import config from "../config.js";
import fetchApiNoBody from "./fetchApiNoBody.js";

export default async function fetchPlayersData(userIdList) {
  try {
    const promises = userIdList.map((id) =>
      fetchApiNoBody("GET", config.userService, `/users?userid=${id}`),
    );
    const results = await Promise.all(promises);
    const playersData = results.map((item) => ({
      avatarPath: `${config.userService}/${item.data.avatarPath}`,
      name: item.data.username,
    }));
    return playersData;
  } catch (error) {
    console.error(error);
    return null;
  }
}
