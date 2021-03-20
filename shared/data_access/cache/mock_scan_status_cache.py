from typing import Dict

from shared.data_access.cache.scan_status_cache import ScanStatusCache
from shared.objects.scan_status import ScanStatus


class MockScanStatusCache(ScanStatusCache):
    _scans: Dict[str, str]

    def __init__(self):
        self._scans = dict()

    def save(self, id_status_map: Dict[str, str]):
        self._scans.update(id_status_map)

    def get_status(self, scan_id: str) -> str:
        status = self._scans.get(scan_id, default=None)
        if status is not None:
            return status
        else:
            return ScanStatus.not_found
