import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestList() {
  return `
	<div class="container">
		${TitleAndHomeButton("FRIEND REQUEST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="list-button btn btn-primary">+ Friends List</button>
		</div>
		<div class="js-friend-request-list">
		</div>
	</div>
	`;
}

export const setupFriendRequestList = async () => {
  let currentPage = 0;
  const limit = 10;
  const friendsList = document.querySelector(".js-friend-request-list");
  friendsList.innerHTML = "";

  async function fetchFriendUserList(offset, limit) {
    // friend_apiを叩く
    const requestResponse = await fetchApiNoBody(
      "GET",
      config.friendService,
      `/friends?status=pending&offset=${offset}&limit=${limit}`,
    );
    if (requestResponse.status === null) {
      console.error("Error Occured!");
      return [];
    }
    if (requestResponse.status >= 400) {
      console.error(requestResponse.data.error);
      return [];
    }
    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    const useridList = requestResponse.data.friends.map(
      (friend) => friend.fromUserId,
    );
    return useridList;
  }

  async function loadFriendRequestList() {
    const friendRequestList = await fetchFriendUserList(
      currentPage * limit,
      limit,
    );
    if (friendRequestList.length === 0) {
      window.removeEventListener("scroll", handleScroll); // スクロールイベントを削除
      return;
    }

    await Promise.all(
      friendRequestList.map(async (requestId) => {
        const friendRequestItem = document.createElement("div");
        const friend = await fetchApiNoBody(
          "Get",
          config.userService,
          `/users?userid=${requestId}`,
        );
        if (friend.status == null) {
          console.error("Error Occured!")
        }
        if (friend.status >= 400) {
          console.error(friend.data.error);
          return;
        }
        const totalLength = 10;
        const name = friend.data.username.padEnd(totalLength, " ");
        friendRequestItem.classList.add("js-friend-request-item");
        friendRequestItem.innerHTML = `
      <div class="gap-wrap d-flex align-items-center mt-4">
        <img src=${friend.data.avatarPath}>
        <div class="text-white">${name}</div>
        <button type="button" class="approved-button btn btn-primary">approved</button>
        <button type="button" class="reject-button btn btn-primary">reject</button>
      </div>
      `;
        friendRequestItem
          .querySelector(".approved-button")
          .addEventListener("click", async () => {
            //テスト用
            // console.log(requestId);
            const approved = await fetchApiNoBody(
              "PATCH",
              config.friendService,
              `/friends/requests/${requestId}`,
            );
            if (approved.status == null) {
              // friendRequestItem.innerHTML = "";
              // friendRequestItem.textContent = "Error Occured";
              return;
            }
            if (approved.status >= 400) {
              // friendRequestItem.innerHTML = "";
              // friendRequestItem.textContent = "Error Occured";
              return;
            }
            friendRequestItem.remove(); // 承認後、要素を削除
          });

        // 拒否ボタン
        friendRequestItem
          .querySelector(".reject-button")
          .addEventListener("click", async () => {
            const rejected = await fetchApiNoBody(
              "DELETE",
              config.friendService,
              `/friends/requests/${requestId}`,
            );
            if (rejected.status == null) {
              return;
            }
            if (rejected >= 400) {
              return;
            }
            friendRequestItem.remove(); // 拒否後、要素を削除
          });
        friendsList.appendChild(friendRequestItem);
      }),
    );
    currentPage++;
  }
  async function handleScroll() {
    if (loading) return;

    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
      // 誤差を考慮
      loading = true;
      await loadFriendRequestList(); //スクロールした時のapiを叩く関数
      loading = false;
    }
  }
  // スクロールイベントを登録
  let loading = false;

  loadFriendRequestList();

  window.addEventListener("scroll", handleScroll);

  const findButton = document.querySelector(".find-button");
  const listButton = document.querySelector(".list-button");

  findButton.addEventListener("click", () => {
    SPA.navigate("/friend/friend-request-form");
  });

  listButton.addEventListener("click", () => {
    SPA.navigate("/friend");
  });
};
