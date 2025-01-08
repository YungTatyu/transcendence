import pyotp
import qrcode
import base64
from io import BytesIO
from auth_app.utils.redis_handler import RedisHandler


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
        qr_code_base64 = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        return qr_code_base64

    @staticmethod
    def verify_otp(username: str, otp_token: str) -> bool:
        """
        ユーザー名に紐付いた秘密鍵を使ってOTPトークンを検証する。

        :param username: ユーザー名（Redisから秘密鍵を取得するキー）
        :param otp_token: ユーザーが入力したOTPトークン
        :return: OTPトークンが正しい場合はTrue、そうでない場合はFalse
        """
        # Redisから秘密鍵を取得
        secret = RedisHandler.get(key=f"otp_secret:{username}")
        if not secret:
            return False

        # OTPトークンを検証
        otp = pyotp.TOTP(secret)
        return otp.verify(otp_token)
