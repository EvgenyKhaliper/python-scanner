from uuid import UUID

from shared.objects.scan_properties import ScanProperties


class Scan:
    scan_id: UUID
    status: str
    properties: ScanProperties

    def __init__(self, scan_id: UUID, status: str, properties: ScanProperties):
        self.scan_id = scan_id
        self.status = status
        self.properties = properties
