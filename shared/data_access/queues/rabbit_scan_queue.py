from typing import Callable, Tuple
from uuid import UUID

import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel

from shared.data_access.queues.scan_queue import ScanQueue


class RabbitScanQueue(ScanQueue):
    host: str
    queue: str = 'scans'

    def __init__(self, host: str):
        self.host = host

    def send_scan(self, scan_id: UUID):
        cn, ch = self._connect()
        message = str(scan_id)
        ch.basic_publish(exchange='', routing_key=self.queue, body=message)
        cn.close()

    def subscribe(self, callback: Callable):
        print('rabbitmq worker up')
        cn, ch = self._connect()
        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=self.queue, on_message_callback=callback)
        ch.start_consuming()

    def _connect(self) -> Tuple[BlockingConnection, BlockingChannel]:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        return connection, channel