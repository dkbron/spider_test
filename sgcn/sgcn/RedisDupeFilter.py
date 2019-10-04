from redis import StrictRedis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

class RedisDupeFilter(BaseDupeFilter):

    def __init__(self, redisHost, redisPort, redisDB):
        self.redis = StrictRedis(
            host=redisHost,
            port=redisPort,
            db=redisDB
        )

    @classmethod
    def from_settings(cls, settings):
        redisHost = settings.get('REDISHOST')
        redisPort = settings.get('REDISPORT')
        reidsDB = settings.get('REDISDB')

        return cls(
            redisHost,
            redisPort,
            reidsDB
        )

    def request_seen(self, request):
        fp = request_fingerprint(request)
        KEY = 'URLFINGER'
        if not self.redis.sismember(KEY, fp):
            self.redis.sadd(KEY, fp)
            return False
        return True