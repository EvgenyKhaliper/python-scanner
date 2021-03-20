import time
import uuid
from random import choice

from shared.data_access.db.scan_store import ScanStore
from shared.objects.scan_properties import ScanProperties
from shared.objects.scan_status import ScanStatus


class ScanExecuter:
    def __init__(self, scan_store: ScanStore):
        self.scan_store = scan_store

    def start(self, scan_id: uuid.UUID):
        try:
            scan_properties = self.scan_store.get_scan_properties(scan_id)
            self._execute(scan_properties)
            self.scan_store.set_status(scan_id, ScanStatus.complete)
        except Exception as ex:
            print(ex)
            self.scan_store.set_status(scan_id, ScanStatus.error)

    """
        imitates execution
    """
    @staticmethod
    def _execute(scan_properties: ScanProperties):
        failed = choice([True, False])
        time.sleep(scan_properties.timeout)
        if failed:
            raise Exception("scan has failed...")
