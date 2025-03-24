import stateManager from "../stateManager.js";
import TitileAndHomeButton from "../components/titleAndHomeButton.js";

export default function FriendRequestList() {
  return `
	<div class="container">
    ${TitileAndHomeButton("FRIEND REQUEST")}
		<div class="button-position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find-button btn btn-primary">+ Find Friend</button>
			<button type="button" class="request-button btn btn-primary">+ Request Friend</button>
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
  async function getFriendUserList() {
    // friend_apiを叩く
    // const response = await fetch("/friend?status=pending");
    // const data = awit response.json();

    // responseの中のユーザのうち自身以外のuserIdを取ってくる
    let userId = stateManager.state?.userId;
    //テストのためuser_idを1にする
    userId = 1;

    //arrayまたはmap
    const useridList = data.friends.map((friend) => friend.fromUserId);
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

  const friendRequestList = await getFriendUserList();

  // const friendInfo = await Promise.all(
  //   friendList.map(async (userid) => {
  //     const user = await getUserNameAndAvatar(userid);
  //     return { ...user };
  //   }),
  // );

  // friendInfo.forEach((friend, index) => {
  //   const friendRequestItem = document.createElement("div");
  //   friendRequestItem.classList.add("js-friend-request-item");
  //   friendRequestItem.innerHTML = `
	// 	<div class="gap-wrap d-flex align-items-center mt-4">
	// 		<img src=${friend.avatarPath}>
	// 		<div class="text-white">${friend.username}</div>
	// 		<button type="button" class="approved-button btn btn-primary">approved</button>
	// 		<button type="button" class="reject-button btn btn-primary">reject</button>
	// 	</div>
	// 	`;
  //   friendsList.appendChild(friendRequestItem);
  // });

  await Promise.all(friendRequestList.map(async (request_id) => {
    const friendRequestItem = document.createElement("div");
    const friend = await getUserNameAndAvatar(request_id);
    friendRequestItem.classList.add("js-friend-request-item");
    friendRequestItem.innerHTML = `
		<div class="gap-wrap d-flex align-items-center mt-4">
			<img src=${friend.avatarPath}>
			<div class="text-white">${friend.username}</div>
			<button type="button" class="approved-button btn btn-primary">approved</button>
			<button type="button" class="reject-button btn btn-primary">reject</button>
		</div>
		`;
    friendsList.appendChild(friendRequestItem);
  }));
};
