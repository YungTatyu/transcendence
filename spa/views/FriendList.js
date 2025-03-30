import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendList() {
  return `
	<div class="container">
		${TitileAndHomeButton("FRIENDS LIST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="request-button btn btn-primary">+ Friends Request</button>
		</div>
		<div class="friend-list js-friend-list ml-4">
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
  ],
  total: 100,
};

export const setupFriendList = async () => {
  const friendsList = document.querySelector(".js-friend-list");
  friendsList.innerHTML = "";
  async function fetchFriendUserList() {
    // friend_apiを叩く
    const response = await fetchApiNoBody(
      "GET",
      config.friendService,
      "/friends?status=approved",
    );

    const userId = stateManager.state?.userId;
    //テストのためuser_idを1にする
    // userId = 1;

    // テスト用
    // const useridList = data.friends.map((friend) =>
    //   friend.fromUserId === 1 ? friend.toUserId : friend.fromUserId,
    // );

    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    const useridList = response.data.friends.map((friend) =>
      friend.fromUserId === userId ? friend.toUserId : friend.fromUserId,
    );
    return useridList;
  }

  // 取得したしたユーザIDからUser
  async function fetchUserNameAndAvatar(userid) {
    const userInfo = await fetchApiNoBody(
      "GET",
      config.userService,
      `/users?userid=${userid}`,
    );
    // const userInfo = await fetchApiNoBody("GET", config.userService,  `/users?userId=${userId}`);
    return userInfo;

    // テスト用
    // return {
    //   status: 200, // 成功ステータス
    //   data: {
    //     userId: userid, // 固定のユーザーID
    //     avatarPath: "/assets/42.png", // 固定のアバターパス
    //     username: "akazukin", // 仮のユーザー名
    //   },
    // };

    // return {
    //   status: null, // 成功ステータス
    //   data: {
    //     userId: userid, // 固定のユーザーID
    //     avatarPath: "/assets/42.png", // 固定のアバターパス
    //     username: "akazukin", // 仮のユーザー名
    //   },
    // };
  }

  async function fetchUserStatus(userId) {
    // statusを得るapiを叩く
    return {
      status: 200, // 成功ステータス
      data: {
        status: "online",
      },
    };
  }

  const friendList = await fetchFriendUserList();

  await Promise.all(
    friendList.map(async (friendId) => {
      const friendItem = document.createElement("div");
      const friend = await fetchUserNameAndAvatar(friendId);
      const statusResponse = await fetchUserStatus(friendId);

      if (friend.status === null || statusResponse.status === null) {
        friendItem.textContent = "Error Occured!";
        friendsList.appendChild(friendItem);
        return;
      }
      if (friend.status >= 400) {
        friendItem.textContent = JSON.stringify(friend.data.error, null, "\n");
        return;
      }
      if (statusResponse.status >= 400) {
        friendItem.textContent = JSON.stringify(
          statusResponse.data.error,
          null,
          "\n",
        );
        return;
      }
      friendItem.classList.add("js-friend-list-item");
      friendItem.innerHTML = `
		<div class="gap-wrap d-flex align-items-center mt-4">
			<img src=${friend.data.avatarPath} alt="avotor">
			<div class="text-white fs-2">${friend.data.username}</div>
			<div class="user-status">${statusResponse.data.status}</div>
			<button type="button" class="remove-button btn btn-primary">remove</button>
		</div>
		`;
      friendItem
        .querySelector(".remove-button")
        .addEventListener("click", async () => {
          // テスト用
          console.log(friendId);
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
};
//error occuredが一度でも出たらmap文をbreakしたい

/// homebuttonのnavigate
