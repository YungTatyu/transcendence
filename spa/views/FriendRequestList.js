import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendRequestList() {
	return `
	<div class="container">
		<h1 class="title text-light ">FRIENDS REQUEST</h1>
		<a href="#" class="home_bottan position-absolute top-0 end-0">
			<img src="/assets/home.png" alt="home" width="90" height="80">
		</a>
		<div class="botton_position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find_bottan btn btn-primary">+ Find Friend</button>
			<button type="button" class="request_bottan btn btn-primary">+ Request Friend</button>
		</div>
		<div class="js-friend_request_list">
			
		</div>
	</div>
	`;
}

const data = {
	"friends": [
	  {
		"fromUserId": 0,
		"toUserId": 1,
		"status": "approved",
		"requestSentAt": "2025-03-18T10:58:38.293Z",
		"approvedAt": "2025-03-18T10:58:38.293Z"
	  },
	  {
		"fromUserId": 2,
		"toUserId": 1,
		"status": "approved",
		"requestSentAt": "2025-03-17T12:00:00.000Z",
		"approvedAt": "2025-03-18T13:00:00.000Z"
	  },
	  {
		"fromUserId": 3,
		"toUserId": 1,
		"status": "approved",
		"requestSentAt": "2025-03-17T12:00:00.000Z",
		"approvedAt": "2025-03-18T13:00:00.000Z"
	  }
	],
	"total": 100
};

export const setupFriendRequestList = async() => {
	const friendsList = document.querySelector(".js-friend_request_list");
	friendsList.innerHTML = '';
	async function get_friend_user_list() {
		// friend_apiを叩く
		// const response = await fetch("/friend?status=pending");
		// const data = awit response.json();


		// responseの中のユーザのうち自身以外のuserIdを取ってくる
		var user_id = stateManager.state?.userId;
		//テストのためuser_idを1にする
		user_id = 1;

		//arrayまたはmap
		var userid_list = data.friends.map(friend => friend.fromUserId);
		return (userid_list)
	}

	// 取得したしたユーザIDからUser
	async function  get_user_name_and_avatar(userid) {
		// const response = await fetch("/users");
    	// const data = await response.json();
		// return {
		// 	username: data.username,
		// 	avatarPath: data.avatarPath
		// };
		return {
			username: "player",
			avatarPath: "/assets/42.png"
		};	
	}

	var friend_list = await get_friend_user_list();

	var friend_info = await Promise.all(friend_list.map(async (userid) => {
		const user = await get_user_name_and_avatar(userid);
		return { ...user};
	}));


	friend_info.forEach(function(friend, index){
		const friendRequestItem = document.createElement("div");
		friendRequestItem.classList.add("js-friend_list_item");
		friendRequestItem.innerHTML = `
		<div class="gap-wrap d-flex align-items-center mt-4">
			<img src=${friend.avatarPath}>
			<div class="text-white">${friend.username}</div>
			<button type="button" class="approved_bottan btn btn-primary">approved</button>
			<button type="button" class="reject_bottan btn btn-primary">reject</button>
		</div>
		`;
		friendsList.appendChild(friendRequestItem);
	})
}