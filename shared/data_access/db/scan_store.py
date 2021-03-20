from abc import ABCMeta, abstractmethod
from typing import List, Dict
from uuid import UUID

from shared.objects.scan import Scan
from shared.objects.scan_properties import ScanProperties


class ScanStore(metaclass=ABCMeta):
    @abstractmethod
    def create_scan(self, scan: Scan):
        pass

    @abstractmethod
    def get_new_scan_ids(self) -> List[UUID]:
        pass

    @abstractmethod
    def get_id_status_map(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_scan_properties(self, scan_id: UUID) -> ScanProperties:
        pass

    @abstractmethod
    def set_status(self, scan_id: UUID, status: str):
        pass



