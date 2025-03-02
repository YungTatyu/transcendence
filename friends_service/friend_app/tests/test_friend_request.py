import jwt
import pytz
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from friend_app.models import Friend


class FriendRequestTestsPost(APITestCase):
    def setUp(self):
        # self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id):
        """
        フレンド申請をしている状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="pending"
        )

    def set_approved(self, from_user_id, to_user_id):
        """
        フレンド状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="approved"
        )

    def test_create_request(self):
        """
        フレンド申請をしていない場合
        """
        url = reverse("friend-request", kwargs={"user_id": 2})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Friend request sent successfully", response.data.get("message"))

    def test_same_account(self):
        """
        自分自身にフレンド申請をした場合
        """
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "You cannot send a request to yourself.", response.data.get("error")
        )

    def test_already_sent_request(self):
        """
        同じ相手にフレンド申請を二度した場合
        """
        url = reverse("friend-request", kwargs={"user_id": 3})

        # 1回目のリクエスト（成功することを期待）
        self.client.post(url)

        # 2回目のリクエスト（エラーが返ることを期待）
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Friend request already sent", response2.data.get("error"))

    def test_already_sent_request2(self):
        """
        相手からフレンド申請が来ている場合
        """
        self.set_pending(7, 1)
        url = reverse("friend-request", kwargs={"user_id": 7})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn(
            "Friend requests have already been received.",
            response.data.get("error", ""),
        )

    def test_already_friend(self):
        """
        すでにフレンドの相手にフレンド申請した場合
        """
        self.set_approved(4, 1)
        url = reverse("friend-request", kwargs={"user_id": 4})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))

    def test_already_friend2(self):
        """
        すでにフレンドの相手にフレンド申請した場合
        """
        self.set_approved(1, 5)
        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))


class FriendRequestTestsDelete(APITestCase):
    def setUp(self):
        # self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id):
        """
        フレンド申請をしている状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="pending"
        )

    def set_approved(self, from_user_id, to_user_id):
        """
        フレンド状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="approved"
        )

    def test_delete_request(self):
        """
        フレンド申請を削除した場合
        """
        self.set_pending(2, 1)
        url = reverse("friend-request", kwargs={"user_id": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_same_account(self):
        """
        自分自身にフレンド申請の削除をした場合
        """
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "You cannot send a request to yourself.", response.data.get("error")
        )

    def test_no_request(self):
        """
        フレンド申請されていないのに削除した場合
        """
        url = reverse("friend-request", kwargs={"user_id": 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            "No friend request exists from the specified user.",
            response.data.get("error"),
        )

    def test_already_friend(self):
        """
        すでにフレンドの相手を削除した場合
        """
        self.set_approved(4, 1)
        url = reverse("friend-request", kwargs={"user_id": 4})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))

    def test_already_sent_request(self):
        """
        2回削除しようとした場合
        """
        self.set_pending(5, 1)
        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            "No friend request exists from the specified user.",
            response.data.get("error"),
        )


class FriendTestDelete(APITestCase):
    def setUp(self):
        # self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id):
        """
        フレンド申請をしている状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="pending"
        )

    def set_approved(self, from_user_id, to_user_id):
        """
        フレンド状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="approved"
        )

    def test_delete_friend(self):
        """
        フレンドの削除
        """
        self.set_approved(1, 2)
        url = reverse("friend", kwargs={"friend_id": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_friend2(self):
        """
        フレンドの削除
        fromとtoを逆にした場合
        """
        self.set_approved(3, 1)
        url = reverse("friend", kwargs={"friend_id": 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_same_account(self):
        """
        自分自身にフレンドの削除をした場合
        """
        url = reverse("friend", kwargs={"friend_id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "You cannot send a request to yourself.", response.data.get("error")
        )

    def test_no_request(self):
        """
        フレンド申請していない場合
        """
        url = reverse("friend", kwargs={"friend_id": 4})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))

    def test_not_receive_request(self):
        """
        フレンド申請を受諾していない場合
        """
        self.set_pending(1, 5)
        url = reverse("friend", kwargs={"friend_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))

    def test_not_receive_request2(self):
        """
        フレンド申請を受諾していない場合
        fromとtoを逆にした場合
        """
        self.set_pending(6, 1)
        url = reverse("friend", kwargs={"friend_id": 6})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))


# add_functionのテスト


class FriendRequestTestsPatch(APITestCase):
    def setUp(self):
        # self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id):
        """
        フレンド申請をしている状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="pending"
        )

    def set_approved(self, from_user_id, to_user_id):
        """
        フレンド状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id, to_user_id=to_user_id, status="approved"
        )

    def test_approved_friend(self):
        """
        id=2からのフレンド申請の承認
        """
        from_user_id = 2
        self.set_pending(from_user_id, 1)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(from_user_id, response.data.get("userId"))

    def test_same_account(self):
        """
        自分自身にフレンド申請の削除をした場合
        """
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "You cannot send a request to yourself.", response.data.get("error")
        )

    def test_from_me_request(self):
        """
        自身からid=3へのフレンド申請を承認しようとした場合
        """
        from_user_id = 3
        self.set_pending(1, from_user_id)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend request not found.", response.data.get("error"))

    def test_no_request(self):
        """
        リクエストが来ていない場合
        """
        from_user_id = 4
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend request not found.", response.data.get("error"))

    def test_already_friend(self):
        """
        すでにフレンドの場合
        """
        from_user_id = 5
        self.set_approved(from_user_id, 1)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Friend request already approved.", response.data.get("error"))


class FriendListTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id, current_time):
        """
        フレンド申請をしている状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status="pending",
            request_sent_at=current_time,
        )

    def set_approved(self, from_user_id, to_user_id, current_time):
        """
        フレンド状態にする
        """
        Friend.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status="approved",
            request_sent_at=current_time,
            approved_at=current_time,
        )

    def test_no_friend(self):
        """
        フレンドがいない場合
        """
        url = reverse("friend-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expect_answer = {
            "friends": [],
            "total": 0,
        }
        self.assertEqual(expect_answer, response.data)

    def test_all(self):
        my_id = 1
        from_user_id = my_id
        to_user_id2 = 2
        to_user_id3 = 3
        to_user_id4 = 4
        to_user_id5 = 5

        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)
        self.set_pending(from_user_id, to_user_id2, current_time)
        self.set_pending(to_user_id3, from_user_id, current_time)
        self.set_approved(from_user_id, to_user_id4, current_time)
        self.set_approved(to_user_id5, from_user_id, current_time)
        url = reverse("friend-list")
        response = self.client.get(url)
        expect_answer = {
            "friends": [
                {
                    "fromUserId": 3,
                    "toUserId": 1,
                    "status": "pending",
                    "requestSentAt": current_time.isoformat(),
                    "approvedAt": None,
                },
                {
                    "fromUserId": 1,
                    "toUserId": 4,
                    "status": "approved",
                    "requestSentAt": current_time.isoformat(),
                    "approvedAt": current_time.isoformat(),
                },
                {
                    "fromUserId": 5,
                    "toUserId": 1,
                    "status": "approved",
                    "requestSentAt": current_time.isoformat(),
                    "approvedAt": current_time.isoformat(),
                },
            ],
            "total": 3,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)


class FriendListQueryTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # JWT トークンの作成
        self.token_payload = {"user_id": 1}
        self.token = jwt.encode(self.token_payload, "test_secret", algorithm="HS256")

        self.client.cookies["access_token"] = self.token

    def set_pending(self, from_user_id, to_user_id, current_time):
        """
        フレンド申請をしている状態にする
        """
        return Friend.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status="pending",
            request_sent_at=current_time,
        )

    def set_approved(self, from_user_id, to_user_id, current_time):
        """
        フレンド状態にする
        """
        return Friend.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            status="approved",
            request_sent_at=current_time,
            approved_at=current_time,
        )

    def create_many_users(
        self, number, current_time, offset, limit, delete_status=None
    ):
        """
        フレンドリストを4パターンに分けてまとめて作成
        1 pending(from_user_id=user_id, to_user_id=other_id)
        2 pending(from_user_id=other_id, to_user_id=user_id)
        3 approved(from_user_id=user_id, to_user_id=other_id)
        4 approved(from_user_id=other_id, to_user_id=user_id)

        number 作成するデータサイズ(人数)
        current_time 時間のずれによるassertのfalseを回避するために時間を統一する
        offset offset
        limit limit
        delete_status 消したいデータのステータス
        """
        user_id = 1
        friend_list = []
        for other_id in range(2, 2 + number):
            if other_id % 4 == 0:
                friend = self.set_pending(user_id, other_id, current_time)
                continue  # 予想の答えのリストに追加しない
            elif other_id % 4 == 1:
                friend = self.set_pending(other_id, user_id, current_time)
            elif other_id % 4 == 2:
                friend = self.set_approved(user_id, other_id, current_time)
            else:
                friend = self.set_approved(other_id, user_id, current_time)
            friend_list.append(
                {
                    "fromUserId": friend.from_user_id,
                    "toUserId": friend.to_user_id,
                    "status": friend.status,
                    "requestSentAt": friend.request_sent_at.isoformat(),
                    "approvedAt": friend.approved_at.isoformat()
                    if friend.approved_at
                    else None,
                }
            )
        if delete_status:
            friend_list = self.delete_pending_approved_data(friend_list, delete_status)
        friend_list = friend_list[offset : offset + limit]
        return {
            "friends": friend_list,
            "total": len(friend_list),
        }

    def delete_pending_approved_data(self, friend_list, delete_status):
        """
        friend_listの指定されたステータスのデータを消す
        """
        # if delete_status == "pending":
        return [friend for friend in friend_list if friend["status"] != delete_status]

    def test_no_query(self):
        """
        クエリーがない場合
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 0, 20)
        url = reverse("friend-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)

    def test_status_pending_query(self):
        """
        quert:status=pendingの時
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 0, 20, "approved")
        url = reverse("friend-list") + "?status=pending"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)

    def test_status_approved_query(self):
        """
        quert:status=approvedの時
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 0, 20, "pending")
        url = reverse("friend-list") + "?status=approved"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)

    def test_offset_error(self):
        """
        オフセットがエラーの時
        エラーメッセージはシリアライザが出すものなので比較しない
        """
        url = reverse("friend-list") + "?offset=-5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offset_over_size(self):
        """
        offsetが作成したデータの数より大きい場合
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 0, 20)
        url = reverse("friend-list") + "?offset=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expect_answer = {
            "friends": [],
            "total": 0,
        }
        self.assertEqual(expect_answer, response.data)

    def test_limit_error(self):
        """
        リミットがエラーの時
        エラーメッセージはシリアライザが出すものなので比較しない
        """
        url = reverse("friend-list") + "?limit=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offset(self):
        """
        offset=3の場合
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 3, 20)
        url = reverse("friend-list") + "?offset=3"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)

    def test_limit(self):
        """
        limit=1の場合
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(5, current_time, 0, 1)
        url = reverse("friend-list") + "?limit=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)

    def test_all(self):
        """
        queryを全て指定
        """
        japan_timezone = pytz.timezone("Asia/Tokyo")
        current_time = now().astimezone(japan_timezone)

        expect_answer = self.create_many_users(100, current_time, 5, 20, "pending")
        url = reverse("friend-list") + "?status=approved&offset=5&limit=20"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)
