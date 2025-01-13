from django.core.cache import cache

class RedisHandler:
    """Redisの操作を行うためのクラス"""

    @staticmethod
    def set(key, value, timeout=None):
        """
        Redisにキーと値を設定する。
        :param key: キャッシュキー
        :param value: 保存する値
        :param timeout: キャッシュの有効期限（秒単位、Noneの場合は無期限）
        """
        cache.set(key, value, timeout)

    @staticmethod
    def get(key):
        """
        Redisから値を取得する。
        :param key: キャッシュキー
        :return: 保存されている値、存在しない場合はNone
        """
        return cache.get(key)

    @staticmethod
    def delete(key):
        """
        Redisから値を削除する。
        :param key: キャッシュキー
        """
        cache.delete(key)

    @staticmethod
    def exists(key):
        """
        指定したキーがRedisに存在するか確認する。
        :param key: キャッシュキー
        :return: True（存在する場合）、False（存在しない場合）
        """
        return cache.has_key(key)  # noqa
