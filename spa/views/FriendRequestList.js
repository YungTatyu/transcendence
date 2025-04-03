import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestList() {
  return `
	<div class="container">
		${TitileAndHomeButton("FRIEND REQUEST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="list-button btn btn-primary">+ Friends List</button>
		</div>
		<div class="js-friend-request-list">
		</div>
	</div>
	`;
}

const data = {
  friends: [
    {
      fromUserId: 0,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-18T10:58:38.293Z",
      approvedAt: "2025-03-18T10:58:38.293Z",
    },
    {
      fromUserId: 2,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 3,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 4,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 5,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 6,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 7,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 8,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 9,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 10,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 11,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 12,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
    {
      fromUserId: 13,
      toUserId: 1,
      status: "approved",
      requestSentAt: "2025-03-17T12:00:00.000Z",
      approvedAt: "2025-03-18T13:00:00.000Z",
    },
  ],
  total: 100,
};

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
      console.log("Error Occured!");
      return [];
    }
    if (requestResponse.status >= 400) {
      console.log(requestResponse.data.error);
      return [];
    }
    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    const userId = stateManager.state?.userId;
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
          friendRequestItem.textContent = "Error Occured!";
          return;
        }
        if (friend.status >= 400) {
          friendRequestItem.textContent = JSON.stringify(
            friend.data.error,
            null,
            "\n",
          );
          return;
        }
        friendRequestItem.classList.add("js-friend-request-item");
        friendRequestItem.innerHTML = `
      <div class="gap-wrap d-flex align-items-center mt-4">
        <img src=${friend.data.avatarPath}>
        <div class="text-white">${friend.data.username}</div>
        <button type="button" class="approved-button btn btn-primary">approved</button>
        <button type="button" class="reject-button btn btn-primary">reject</button>
      </div>
      `;
        friendRequestItem
          .querySelector(".approved-button")
          .addEventListener("click", async () => {
            //テスト用
            console.log(requestId);
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
};
