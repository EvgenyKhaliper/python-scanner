import uuid
from typing import List, Dict
from uuid import UUID

from shared.data_access.db.scan_store import ScanStore
from shared.objects.scan_properties import ScanProperties
from shared.objects.scan_status import ScanStatus
from shared.objects.scan import Scan


class MockScanStore(ScanStore):
    _scans: List[Scan]

    def __init__(self):
        self._scans = list()

    def create_scan(self, scan: Scan):
        self._scans.append(scan)

    def get_new_scan_ids(self) -> List[UUID]:
        return [scan.scan_id for scan in self._scans if scan.status == ScanStatus.accepted]

    def get_id_status_map(self) -> Dict[str, str]:
        return {str(scan.scan_id): scan.status for scan in self._scans if scan.status == ScanStatus.accepted}

    def get_scan_properties(self, scan_id: UUID) -> ScanProperties:
        return next(iter([scan.properties for scan in self._scans if scan.scan_id == scan_id]), None)

    def set_status(self, scan_id: UUID, status: str):
        scan = next(iter([scan for scan in self._scans if scan.scan_id == scan_id]), None)
        if scan is not None:
            scan.status = status
