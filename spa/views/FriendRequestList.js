import fetchApiNoBody from "../api/fetchApiNoBody.js";
import TitleAndHomeButton from "../components/TitleAndHomeButton.js";
import config from "../config.js";

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

const scrollHandler = {
  loading: false,
  currentPage: 0,
  limit: 10,
  total: null,
  async fetchFriendUserList() {
    // friend_apiを叩く
    const offset = this.currentPage * this.limit;
    const requestResponse = await fetchApiNoBody(
      "GET",
      config.friendService,
      `/friends?status=pending&offset=${offset}&limit=${this.limit}`,
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
    this.total = requestResponse.data.total;
    const useridList = requestResponse.data.friends.map(
      (friend) => friend.fromUserId,
    );
    return useridList;
  },
  async loadFriendRequestList() {
    if (this.loading) return;
    this.loading = true;
    const friendsList = document.querySelector(".js-friend-request-list");
    if (!friendsList) {
      return;
    }
    const friendRequestList = await this.fetchFriendUserList();
    const offset = this.currentPage * this.limit;
    if (this.total !== null && this.total <= offset + this.limit) {
      window.removeEventListener("scroll", this.handleScroll);
    }
    if (friendRequestList.length === 0) return;
    await Promise.all(
      friendRequestList.map(async (requestId) => {
        const friendRequestItem = document.createElement("div");
        const friend = await fetchApiNoBody(
          "GET",
          config.userService,
          `/users?userid=${requestId}`,
        );
        if (friend.status == null) {
          console.error("Error Occured!");
        }
        if (friend.status >= 400) {
          console.error(friend.data.error);
          return;
        }
        const totalLength = 10;
        const name = friend.data.username.padEnd(totalLength, " ");
        const avatarImg = `${config.userService}${friend.data.avatarPath}`;
        friendRequestItem.classList.add("js-friend-request-item");
        friendRequestItem.innerHTML = `
      <div class="gap-wrap d-flex align-items-center mt-4">
        <img src=${avatarImg}>
        <div class="text-white">${name}</div>
        <button type="button" class="approved-button btn btn-primary">Approve</button>
        <button type="button" class="reject-button btn btn-primary">Reject</button>
      </div>
      `;
        friendRequestItem
          .querySelector(".approved-button")
          .addEventListener("click", async () => {
            const approved = await fetchApiNoBody(
              "PATCH",
              config.friendService,
              `/friends/requests/${requestId}`,
            );
            if (approved.status == null) {
              console.error("Error Occured!");
              return;
            }
            if (approved.status >= 400) {
              console.error(approved.data.error);
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
        try {
          friendsList.appendChild(friendRequestItem);
        } catch (error) {
          console.log(error);
        }
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
      await scrollHandler.loadFriendRequestList(); //スクロールした時のapiを叩く関数
    }
  },
  destructor() {
    this.currentPage = 0;
    this.loading = false;
  },
};

export const setupFriendRequestList = async () => {
  const friendsList = document.querySelector(".js-friend-request-list");
  if (!friendsList) {
    return;
  }
  friendsList.innerHTML = "";

  // スクロールイベントを登録
  await scrollHandler.loadFriendRequestList();

  window.addEventListener("scroll", scrollHandler.handleScroll);

  const findButton = document.querySelector(".find-button");
  const listButton = document.querySelector(".list-button");

  if (!(findButton && listButton)) {
    return;
  }

  findButton.addEventListener("click", () => {
    SPA.navigate("/friend/friend-request-form");
  });

  listButton.addEventListener("click", () => {
    SPA.navigate("/friend");
  });
};

export const cleanupFriendRequestList = () => {
  window.removeEventListener("scroll", scrollHandler.handleScroll);
  scrollHandler.destructor();
  console.log("Scroll event removed");
};
