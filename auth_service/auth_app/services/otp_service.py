import base64
import logging
from io import BytesIO

import pyotp
import qrcode

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
    def verify_otp(otp_secret: str, otp_token: str) -> bool:
        """
        ユーザー名に紐付いた秘密鍵を使ってOTPトークンを検証する。

        :param otp_secret: ユーザー名に紐付いた秘密鍵
        :param otp_token: ユーザーが入力したOTPトークン
        :return: OTPトークンが正しい場合はTrue、そうでない場合はFalse
        """
        otp = pyotp.TOTP(otp_secret)
        return otp.verify(otp_token)
