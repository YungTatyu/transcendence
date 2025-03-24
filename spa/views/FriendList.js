import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import stateManager from "../stateManager.js";

export default function FriendList() {
  return `
	<div class="container">
    ${TitileAndHomeButton("FRIEND LIST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="request-button btn btn-primary">+ Request Friend</button>
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
  async function getFriendUserList() {
    // friend_apiを叩く
    // const response = await fetch("/friend?status=approved");
    // const data = awit response.json();

    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    let userId = stateManager.state?.userId;
    //テストのためuser_idを1にする
    userId = 1;

    //arrayまたはmap
    const useridList = data.friends.map((friend) =>
      friend.fromUserId === 1 ? friend.toUserId : friend.fromUserId,
    );
    return useridList;
  }

  // 取得したしたユーザIDからUser
  async function getUserNameAndAvatar(userid) {
    // const response = await fetch("/users");
    // const data = await response.json();
    // return {
    // 	username: data.username,
    // 	avatarPath: data.avatarPath
    // };
    return {
      username: "player",
      avatarPath: "/assets/42.png",
    };
  }

  async function getUserStatus(userId) {
    // statusを得るapiを叩く
    return {
      status: "online",
    };
  }

  const friendList = await getFriendUserList();

  await Promise.all(
    friendList.map(async (friendId) => {
      const friendItem = document.createElement("div");
      const friend = await getUserNameAndAvatar(friendId);
      const status = await getUserStatus(friendId);
      friendItem.classList.add("js-friend-list-item");
      friendItem.innerHTML = `
		<div class="gap-wrap d-flex align-items-center mt-4">
			<img src=${friend.avatarPath} alt="avotor">
			<div class="text-white fs-2">${friend.username}</div>
			<div class="user-status">${status.status}</div>
			<button type="button" class="remove-button btn btn-primary">remove</button>
		</div>
		`;
      friendItem
        .querySelector(".remove-button")
        .addEventListener("click", async () => {
          // await fetch(`/friend/approve/${request_id}`, { method: "POST" }); // APIを叩く
          friendItem.remove(); // 要素を削除
        });
      friendsList.appendChild(friendItem);
    }),
  );
};
