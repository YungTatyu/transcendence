import config from "../config.js";
import stateManager from "../stateManager.js";

export default function FriendList() {
	return `
	<div class="container">
		<h1 class="title text-light ">FRIENDS LIST</h1>
		<a href="#" class="home_bottan position-absolute top-0 end-0">
			<img src="assets/home.png" alt="home" width="90" height="80">
		</a>
		<div class="botton_position d-flex flex-column justify-content-center align-items-end gap-3">
			<button type="button" class="find_bottan btn btn-primary">+ Find Friend</button>
			<button type="button" class="request_bottan btn btn-primary">+ Request Friend</button>
		</div>
		<div class="friend_list ml-4">
			
		</div>
	</div>
	`;
}

export const setupFriendList = async() {
	// friend_apiを叩く
	async function get_friend_user_list() {
		// const response = await fetch("/friend");
		// const data = awit response.json();
		// responseの中のユーザのうち
		// 
		
		return (userid_list)
	}

	// 取得したしたユーザIDからUser
	async function  get_user_name_and_avator(userid) {
		// const response = await fetch("/users");
    	// const data = await response.json();
		// return {
		// 	username: data.username,
		// 	avatarPath: data.avatarPath
		// };
		return {
			username: "player",
			avatarPath: "../asssets/42.png"
		};	
	} 

	friend_list = 
}