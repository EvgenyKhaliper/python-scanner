from abc import ABCMeta, abstractmethod
from typing import Dict


class ScanStatusCache(metaclass=ABCMeta):
    @abstractmethod
    def save(self, scans: Dict[str, str]):
        pass

    @abstractmethod
    def get_status(self, scan_id: str) -> str:
        pass


