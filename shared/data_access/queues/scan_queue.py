from abc import ABCMeta, abstractmethod
from typing import Callable
from uuid import UUID


class ScanQueue(metaclass=ABCMeta):
    @abstractmethod
    def send_scan(self, scan_id: UUID):
        pass

    @abstractmethod
    def subscribe(self, callback: Callable):
        pass


