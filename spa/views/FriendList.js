import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";
import WsFriendActivityManager from "../services/friend_activity/WsFriendActivityManager.js";

export default function FriendList() {
  return `
	<div class="container">
		${TitleAndHomeButton("FRIENDS LIST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="request-button btn btn-primary">+ Friends Request</button>
		</div>
		<div class="friend-list js-friend-list ml-4">
		</div>
	</div>
	`;
}


export const setupFriendList = async () => {
  let currentPage = 0;
  const limit = 10;
  const friendsList = document.querySelector(".js-friend-list");
  friendsList.innerHTML = "";

  async function fetchFriendUserList(offset, limit) {
    // friend_apiを叩く
    const response = await fetchApiNoBody(
      "GET",
      config.friendService,
      `/friends?status=approved&offset=${offset}&limit=${limit}`,
    );
    if (response.status === null) {
      console.error("Error Occured");
      return [];
    }
    if (response.status >= 400) {
      console.error(response.data.error);
      return [];
    }
    const userId = stateManager.state?.userId;
    const useridList = response.data.friends.map((friend) =>
      friend.fromUserId === userId ? friend.toUserId : friend.fromUserId,
    );
    return useridList;
  }

  async function loadFriendList() {
    // console.log(currentPage * limit);
    const friendList = await fetchFriendUserList(currentPage * limit, limit);
    if (friendList.length === 0) {
      window.removeEventListener("scroll", handleScroll); // スクロールイベントを削除
      return;
    }
    // const onlineUserlist = stateManager.onlineUsers;
    await Promise.all(
      friendList.map(async (friendId) => {
        const friendItem = document.createElement("div");
        const friend = await fetchApiNoBody(
          "GET",
          config.userService,
          `/users?userid=${friendId}`,
        );
        const status = "offline";
        // if (onlineUserlist?.includes(friendId))
        //   status = "online";
        if (friend.status === null) {
          console.error("Error Occured!");
          return;
        }
        if (friend.status >= 400) {
          console.error(friend.data.error);
          return;
        }
        const avatarImg = `${config.userService}${friend.data.avatarPath}`;
        friendItem.classList.add("js-friend-list-item");
        friendItem.innerHTML = `
        <div class="gap-wrap d-flex align-items-center mt-4">
          <img src=${avatarImg} alt="avotor">
          <div class="text-white fs-2">${friend.data.username}</div>
          <div data-userid="${friendId}" class="user-status" style="color: #929090;">${status}</div>
          <button type="button" class="remove-button btn btn-primary">Remove</button>
        </div>
        `;
        friendItem
          .querySelector(".remove-button")
          .addEventListener("click", async () => {
            // テスト用
            // console.log(friendId);
            const deleteResponse = await fetchApiNoBody(
              "DELETE",
              config.friendService,
              `/friends/${friendId}`,
            );
            if (deleteResponse.status == null) {
              return;
            }
            if (deleteResponse.status >= 400) {
              return;
            }
            friendItem.remove(); // 要素を削除
          });
        friendsList.appendChild(friendItem);
      }),
    );
    currentPage++;
  }

  // 無限スクロールの実装
  async function handleScroll() {
    if (loading) return;

    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
      // 誤差を考慮
      loading = true;
      await loadFriendList(); //スクロールした時のapiを叩く関数
      loading = false;
    }
  }
  // スクロールイベントを登録
  let loading = false;

  await loadFriendList();

  window.addEventListener("scroll", handleScroll);

  const accessToken = sessionStorage.getItem("access_token");
  if (!accessToken) {
    SPA.navigate("/");
    return;
  }

  WsFriendActivityManager.connect(accessToken);

  const findButton = document.querySelector(".find-button");
  const requestButton = document.querySelector(".request-button");

  findButton.addEventListener("click", () => {
    SPA.navigate("/friend/friend-request-form");
  });

  requestButton.addEventListener("click", () => {
    SPA.navigate("/friend/request");
  });
};
