import fetchApiNoBody from "../api/fetchApiNoBody.js";
import config from "../config.js";
import TitileAndHomeButton from "../components/titleAndHomeButton.js";
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
  ],
  total: 100,
};

export const setupFriendRequestList = async () => {
  const friendsList = document.querySelector(".js-friend-request-list");
  friendsList.innerHTML = "";
  async function fetchFriendUserList() {
    // friend_apiを叩く
    // const requestResponse = await fetchApiNoBody("GET", config.friendService, '/friends?status=pending');

    // エラー処理を入れる
    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    // let userId = stateManager.state?.userId;

    //テスト用
    // userId = 1;
    const useridList = data.friends.map((friend) => friend.fromUserId);

    // const useridList = requestResponse.data.friends.map((friend) => friend.fromUserId);
    return useridList;
  }

  // 取得したしたユーザIDからUser
  async function fetchUserNameAndAvatar(userId) {
    //return userInfo = await fetchApiNoBody("GET", config.userService,  `/users?userId=${userId}`);

    //テスト用
    return {
      status: 200, // 成功ステータス
      data: {
        userId: userId, // 固定のユーザーID
        avatarPath: "/assets/42.png", // 固定のアバターパス
        username: "akazukin", // 仮のユーザー名
      },
    };
  }

  const friendRequestList = await fetchFriendUserList();

  await Promise.all(
    friendRequestList.map(async (requestId) => {
      const friendRequestItem = document.createElement("div");
      const friend = await fetchUserNameAndAvatar(requestId);
      if (friend.status == null)
      {
        friendRequestItem.textContent = "Error Occured!";
        return ;
      }
      if (friend.status >= 400)
      {
        friendRequestItem.textContent =  JSON.stringify(friend.data.error, null, "\n");
        return ;
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
          const approved = await fetchApiNoBody("PATCH", config.friendService, `/friends/requests/${requestId}`);
          if (approved.status == null)
          {
            // friendRequestItem.innerHTML = "";
            // friendRequestItem.textContent = "Error Occured";
            return ;
          }
          if (approved.status >= 400)
          {
            // friendRequestItem.innerHTML = "";
            // friendRequestItem.textContent = "Error Occured";
            return ;
          }
          friendRequestItem.remove(); // 承認後、要素を削除
        });

      // 拒否ボタン
      friendRequestItem
        .querySelector(".reject-button")
        .addEventListener("click", async () => {
          const rejected = await fetchApiNoBody("DELETE", config.friendService, `/friends/requests/${requestId}`);
          if (rejected.status == null)
          {
            return ;
          }
          if (rejected >= 400)
          {
            return ;
          }
          friendRequestItem.remove(); // 拒否後、要素を削除
        });
      friendsList.appendChild(friendRequestItem);
    }),
  );
};

// jwtの関係上テストできない？
// const approved = await fetchApiNoBody("PATCH", config.friendService, `/friends/requests/${requestId}`);および
// const rejected = await fetchApiNoBody("DELETE", config.friendService, `/friends/requests/${requestId}`);
//　のエラー処理はどうするか？　エラー文は必要ない？