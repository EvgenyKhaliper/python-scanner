from typing import Dict

import redis

from shared.data_access.cache.scan_status_cache import ScanStatusCache
from shared.objects.scan_status import ScanStatus


class RedisScanStatusCache(ScanStatusCache):
    _rc: redis.Redis
    _key: str = "scan_statuses"

    def __init__(self, host: str):
        self._rc = redis.Redis(host=host, port=6379, db=0)

    def save(self, scans: Dict[str, str]):
        self._rc.hmset(self._key, scans)

    def get_status(self, scan_id: str) -> str:
        id_status_map = self._rc.hgetall(self._key)
        status = id_status_map.get(scan_id.encode(encoding='UTF-8', errors='strict'), None)
        if status is not None:
            return status.decode(encoding='UTF-8')
        else:
            return ScanStatus.not_found