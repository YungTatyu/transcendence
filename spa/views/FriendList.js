import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";
import WsFriendActivityManager from "../services/friend_activity/WsFriendActivityManager.js";
import stateManager from "../stateManager.js";

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

const scrollHandler = {
  loading: false,
  currentPage: 0,
  limit: 10,
  async fetchFriendUserList() {
    const offset = this.currentPage * this.limit;
    const response = await fetchApiNoBody(
      "GET",
      config.friendService,
      `/friends?status=approved&offset=${offset}&limit=${this.limit}`,
    );
    if (response.status === null) {
      console.error("Error Occured");
      return [];
    }
    if (response.status >= 400) {
      console.error(response.data.error);
      return [];
    }
    // if (response.data.total <= offset + this.limit)
    //   return [];
    const userId = Number(stateManager.state?.userId);
    const useridList = response.data.friends.map((friend) =>
      friend.fromUserId === userId ? friend.toUserId : friend.fromUserId,
    );
    return useridList;
  },
  async loadFriendList() {
    if (this.loading) return;
    this.loading = true;
    const friendsList = document.querySelector(".js-friend-list");
    const friendList = await this.fetchFriendUserList(); //ここはthisでいいのか
    if (friendList.length === 0) {
      window.removeEventListener("scroll", this.handleScroll); // スクロールイベントを削除
    }
    // console.log(friendList);
    await Promise.all(
      friendList.map(async (friendId) => {
        const friendItem = document.createElement("div");
        const friend = await fetchApiNoBody(
          "GET",
          config.userService,
          `/users?userid=${friendId}`,
        );
        let status = "offline";
        console.log(stateManager.state.onlineUsers);
        if (stateManager.state?.onlineUsers.includes(String(friendId))) {
          status = "online";
          console.log(stateManager.state.onlineUsers);
        }
        const statusColor = status === "online" ? "#0CC0DF" : "#929090";
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
          <div data-userid="${friendId}" class="user-status" style="color: ${statusColor}">${status}</div>
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
    this.currentPage++;
    this.loading = false;
  },
  async handleScroll() {
    const scrollTop = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const windowHeight = window.innerHeight;

    if (scrollTop + windowHeight >= documentHeight - 10) {
      // 誤差を考慮
      await scrollHandler.loadFriendList(); //スクロールした時のapiを叩く関数
    }
  },
  destructor() {
    this.currentPage = 0;
    this.loading = false;
  },
};

export const setupFriendList = async () => {
  const friendsList = document.querySelector(".js-friend-list");
  friendsList.innerHTML = "";
  await scrollHandler.loadFriendList();
  window.addEventListener("scroll", scrollHandler.handleScroll);
  const findButton = document.querySelector(".find-button");
  const requestButton = document.querySelector(".request-button");

  findButton.addEventListener("click", () => {
    SPA.navigate("/friend/friend-request-form");
  });

  requestButton.addEventListener("click", () => {
    SPA.navigate("/friend/request");
  });
};

export const cleanupFriendList = () => {
  window.removeEventListener("scroll", scrollHandler.handleScroll);
  scrollHandler.destructor();
  console.log("Scroll event removed");
};
