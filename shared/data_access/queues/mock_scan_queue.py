from typing import List, Callable
from uuid import UUID

from apscheduler.schedulers.background import BackgroundScheduler

from shared.data_access.queues.scan_queue import ScanQueue


class MockScanQueue(ScanQueue):
    _ids: List[UUID]

    def __init__(self):
        self._ids = list()

    def send_scan(self, scan_id: UUID):
        self._ids.append(scan_id)

    def subscribe(self, callback: Callable):
        bc = BackgroundScheduler(daemon=True)
        bc.add_job(lambda c: self._take_one(callback), 'interval', seconds=1)
        bc.start()

    def _take_one(self, callback: Callable):
        if self._ids:
            current_id = self._ids.pop(0)
            callback(None, None, None, str(current_id).encode(encoding="UTF-8"))
