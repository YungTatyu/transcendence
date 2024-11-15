import { fetchData } from "./api.js";

let usersCache = {}

/**
 * @brief Returns user data If not found, fetches users data.
 * @returns object|null
 */
export async function fetchUsers() {
  if (Object.keys(usersCache).length > 0) {
    return usersCache
  }
  try {
    const users = await fetchData("http://127.0.0.1:8000/users/")
    console.log("fetch users", users)
    users.results.forEach(user => {
      usersCache[user.id] = user
    });
    return usersCache
  } catch (error) {
    console.error("Failed to fetch users:", error);
    return null
  }
}


/**
 * @brief Returns user data by id. If not found, fetches users data.
 * @param id: int
 * @returns object|null
 */
export async function fetchUserById(id) {
  if (usersCache[id]) {
    return usersCache[id]
  }
  try {
    const users = await fetchData("http://127.0.0.1:8000/users/")
    usersCache = {} // delete cache
    users.forEach(user => {
      usersCache[user.id] = user
    });
    const user = usersCache[id] ? usersCache[id] : null
    return user
  } catch (error) {
    console.error("Failed to fetch users:", error);
    return null
  }
}
