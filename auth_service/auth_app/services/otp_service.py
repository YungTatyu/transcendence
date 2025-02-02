import base64
import json
import logging
from io import BytesIO

import pyotp
import qrcode
from django.conf import settings

from auth_app.client.user_client import UserClient
from auth_app.models import CustomUser
from auth_app.utils.redis_handler import RedisHandler

logger = logging.getLogger(__name__)


class OTPService:
    """OTP関連のサービスクラス"""

    @staticmethod
    def generate_qr_code(email: str, secret: str, issuer_name: str = "auth_app") -> str:
        """
        OTPの秘密鍵を生成し、QRコードを生成する。

        :param email: メールアドレス（QRコードのプロビジョニングURIに使用）
        :param secret: OTPの秘密鍵
        :param issuer_name: OTPの発行者名（デフォルト: "auth_app"）
        :return: Base64エンコードされたQRコード
        """

        # OTPプロビジョニングURIを作成
        otp = pyotp.TOTP(secret)
        provisioning_uri = otp.provisioning_uri(name=email, issuer_name=issuer_name)

        # QRコードを生成してBase64エンコード
        img = qrcode.make(provisioning_uri)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = (
            f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        )
        return qr_code_base64

    @staticmethod
    def verify_otp(username: str, otp_token: str) -> bool:
        """
        ユーザー名に紐付いた秘密鍵を使ってOTPトークンを検証する。

        :param username: ユーザー名（Redisから秘密鍵を取得するキー）
        :param otp_token: ユーザーが入力したOTPトークン
        :return: OTPトークンが正しい場合はTrue、そうでない場合はFalse
        """
        # Redisから仮登録データを取得
        redis_key = f"pending_user:{username}"
        redis_data = RedisHandler.get(key=redis_key)

        if redis_data:
            #  仮登録データがJSON形式なので、デコード
            user_data = json.loads(redis_data)

            # OTP秘密鍵を取得
            secret = user_data.get("otp_secret")
            if not secret:
                logger.debug("there no secret")
                return False  # OTP秘密鍵がない場合

            # OTPトークンを検証
            otp = pyotp.TOTP(secret)
            return otp.verify(otp_token)
        else:
            logger.warn("there no temporary user")

            try:
                # DBからユーザー情報を取得
                client = UserClient(
                    base_url=settings.USER_API_BASE_URL,
                    use_mock=settings.USER_API_USE_MOCK,
                    mock_search_data={"userId": "12345", "username": "mockuser"},
                )

                # `username` でユーザーを検索
                res = client.search_users({"username": username})
                user_data = res.json()
                if not user_data or "userId" not in user_data:
                    raise ValueError("User not found")
                user_id = user_data["userId"]

                user = CustomUser.objects.get(user_id=user_id)

                # ユーザーのOTP秘密鍵を取得
                secret = user.secret_key
                if secret:
                    otp = pyotp.TOTP(secret)
                    return otp.verify(otp_token)
                else:
                    logger.debug(f"No OTP secret found for user {username}.")
                    return False

            except ValueError as ve:
                logger.error(f"Error: {str(ve)}")
                return False  # ユーザーが見つからない場合

            except CustomUser.DoesNotExist:
                logger.error(f"User with username {username} does not exist in the database.")
                return False  # DB内にユーザーが存在しない場合

            except Exception as e:
                logger.error(f"Unexpected error occurred: {str(e)}")
                return False  # その他の予期しないエラー
