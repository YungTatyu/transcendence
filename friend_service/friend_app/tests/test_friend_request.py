from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from friend_app.models import Friends 

class FriendRequestTests_POST(APITestCase):

    def set_pending(self, from_user_id, to_user_id):
        '''
        フレンド申請をしている状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="pending")
    
    def set_approved(self, from_user_id, to_user_id):
        '''
        フレンド状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="approved")

    def test_create_request(self):
        """
        フレンド申請をしていない場合
        """
        url = reverse("friend-request", kwargs={"user_id": 2})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Friend request sent successfully", response.data.get("message"))

    def test_same_account(self):
        '''
        自分自身にフレンド申請をした場合
        '''
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.post(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot send a request to yourself.", response.data.get("error"))  # メッセージ確認

    def test_already_sent_request(self):
        """
        同じ相手にフレンド申請を二度した場合
        """
        url = reverse("friend-request", kwargs={"user_id": 3})

        # 1回目のリクエスト（成功することを期待）
        response1 = self.client.post(url)

        # 2回目のリクエスト（エラーが返ることを期待）
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Friend request already sent", response2.data.get("error"))

    def test_already_sent_request2(self):
        """
        相手からフレンド申請が来ている場合
        """
        self.set_pending(7,1)
        url = reverse("friend-request", kwargs={"user_id": 7})
        response = self.client.post(url)

        print(response.data)  # レスポンス内容をデバッグ

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Friend requests have already been received.", response.data.get("error", ""))


    def test_already_friend(self):
        '''
        すでにフレンドの相手にフレンド申請した場合
        '''
        self.set_approved(4, 1)
        # self.set_pending()
        url = reverse("friend-request", kwargs={"user_id": 4})
        response = self.client.post(url)

        print(response.data)  # レスポンス内容をデバッグ

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))

    def test_already_friend2(self):
        '''
        すでにフレンドの相手にフレンド申請した場合
        '''
        self.set_approved(1,5)
        # self.set_pending()
        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.post(url)

        print(response.data)  # レスポンス内容をデバッグ

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))


class FriendRequestTests_DELETE(APITestCase):
    def set_pending(self, from_user_id, to_user_id):
        '''
        フレンド申請をしている状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="pending")
    
    def set_approved(self, from_user_id, to_user_id):
        '''
        フレンド状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="approved")

    def test_delete_request(self):
        '''
        フレンド申請を削除した場合
        '''
        self.set_pending(1, 2)
        url = reverse("friend-request", kwargs={"user_id": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_same_account(self):
        '''
        自分自身にフレンド申請の削除をした場合
        '''
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot send a request to yourself.", response.data.get("error"))
 
    def test_no_request(self):
        '''
        フレンド申請していないのに削除した場合
        '''
        url = reverse("friend-request", kwargs={"user_id": 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No friend request exists from the specified user.", response.data.get("error"))

    def test_already_friend(self):
        '''
        すでにフレンドの相手を削除した場合
        '''
        self.set_approved(1, 4)
        url = reverse("friend-request", kwargs={"user_id": 4})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Already friend.", response.data.get("error"))

    def test_already_sent_request(self):
        '''
        2回削除しようとした場合
        '''
        self.set_pending(1, 5)
        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("friend-request", kwargs={"user_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No friend request exists from the specified user.", response.data.get("error"))


class FriendTest_delete(APITestCase):
    def set_pending(self, from_user_id, to_user_id):
        '''
        フレンド申請をしている状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="pending")
    
    def set_approved(self, from_user_id, to_user_id):
        '''
        フレンド状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="approved")

    def test_delete_friend(self):
        '''
        フレンドの削除
        '''
        self.set_approved(1,2)
        url = reverse("friend", kwargs={"friend_id": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_friend2(self):
        '''
        フレンドの削除
        fromとtoを逆にした場合
        '''
        self.set_approved(3,1)
        url = reverse("friend", kwargs={"friend_id": 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_same_account(self):
        '''
        自分自身にフレンドの削除をした場合
        '''
        url = reverse("friend", kwargs={"friend_id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot send a request to yourself.", response.data.get("error"))
 
    def test_no_request(self):
        '''
        フレンド申請していない場合
        '''
        url = reverse("friend", kwargs={"friend_id": 4})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))

    def test_not_receive_request(self):
        '''
        フレンド申請を受諾していない場合
        '''
        self.set_pending(1,5)
        url = reverse("friend", kwargs={"friend_id": 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))

    def test_not_receive_request2(self):
        '''
        フレンド申請を受諾していない場合
        fromとtoを逆にした場合
        '''
        self.set_pending(6,1)
        url = reverse("friend", kwargs={"friend_id": 6})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found.", response.data.get("error"))
        

#add_functionのテスト

class FriendRequestTests_PATCH(APITestCase):
    def set_pending(self, from_user_id, to_user_id):
        '''
        フレンド申請をしている状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="pending")
    
    def set_approved(self, from_user_id, to_user_id):
        '''
        フレンド状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="approved")

    def test_approved_friend(self):
        '''
        id=2からのフレンド申請の承認
        '''
        from_user_id=2
        self.set_pending(from_user_id, 1)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(from_user_id, response.data.get("userId"))
    
    def test_same_account(self):
        '''
        自分自身にフレンド申請の削除をした場合
        '''
        url = reverse("friend-request", kwargs={"user_id": 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot send a request to yourself.", response.data.get("error"))

    def test_from_me_request(self):
        '''
        自身からid=3へのフレンド申請を承認しようとした場合
        '''
        from_user_id=3
        self.set_pending(1,from_user_id)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend request not found.", response.data.get("error"))

    def test_no_request(self):
        '''
        リクエストが来ていない場合
        '''
        from_user_id=4
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend request not found.", response.data.get("error"))

    def test_already_friend(self):
        '''
        すでにフレンドの場合
        '''
        from_user_id=5
        self.set_approved(from_user_id, 1)
        url = reverse("friend-request", kwargs={"user_id": from_user_id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Friend request already approved.", response.data.get("error"))

from datetime import datetime
from django.utils.timezone import now 
import pytz

class FriendListTest(APITestCase):
    '''
    getのテスト
    自分のid=1とする
    '''
    def set_pending(self, from_user_id, to_user_id, current_time):
        '''
        フレンド申請をしている状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="pending", request_sent_at=current_time)
    
    def set_approved(self, from_user_id, to_user_id, current_time):
        '''
        フレンド状態にする
        '''
        Friends.objects.create(from_user_id=from_user_id, to_user_id=to_user_id, status="approved", request_sent_at=current_time, approved_at=current_time)

    def test_no_friend(self):
        '''
        フレンドがいない場合
        '''
        url = reverse("friend-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Friend not found", response.data.get("error"))

    def test_all(self):
        my_id = 1
        from_user_id = my_id
        to_user_id2 = 2
        to_user_id3 = 3
        to_user_id4 = 4
        to_user_id5 = 5

        japan_timezone = pytz.timezone('Asia/Tokyo')
        current_time = now().astimezone(japan_timezone)
        self.set_pending(from_user_id, to_user_id2, current_time)
        self.set_pending(to_user_id3, from_user_id, current_time)
        self.set_approved(from_user_id, to_user_id4, current_time)
        self.set_approved(to_user_id5, from_user_id,current_time)
        url = url = reverse("friend-list")
        response = self.client.get(url)
        expect_answer = {
        "friends": [
            {
                "userId": 2,
                "username": "test",
                "status": "pending",
                "request_sent_at":current_time.isoformat(),
                "approved_at": None
            },
            {
                "userId": 3,
                "username": "test",
                "status": "pending",
                "request_sent_at":current_time.isoformat(),
                "approved_at": None
            },
            {
                "userId": 4,
                "username": "test",
                "status": "approved",
                "request_sent_at":current_time.isoformat(),
                "approved_at":current_time.isoformat()
            },
            {
                "userId": 5,
                "username": "test",
                "status": "approved",
                "request_sent_at":current_time.isoformat(),
                "approved_at":current_time.isoformat()
            }
        ],
         "total": 4
    }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.maxDiff = None
        self.assertEqual(expect_answer, response.data)
    

