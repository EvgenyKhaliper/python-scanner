import multiprocessing
import os
import uuid

from flask import Flask

from scan_executer.executer import ScanExecuter
from shared.data_access.db.mock_scan_store import MockScanStore
from shared.data_access.db.postgres_scan_store import PostgresScanStore
from shared.data_access.queues.mock_scan_queue import MockScanQueue
from shared.data_access.queues.rabbit_scan_queue import RabbitScanQueue

app = Flask(__name__)

if os.getenv('RABBIT_HOST', None) is not None:
    scan_queue = RabbitScanQueue(os.environ["RABBIT_HOST"])
else:
    scan_queue = MockScanQueue()

if os.getenv('POSTGRES_CONNECTION', None) is not None:
    scan_store = PostgresScanStore(os.environ["POSTGRES_CONNECTION"])
else:
    scan_store = MockScanStore()


@app.route('/api/', methods=['GET'])
def get_scan_status():
    return "Healthy"


def on_message(ch, method, properties, body):
    scan_id = body.decode(encoding='UTF-8')
    ScanExecuter(scan_store).start(uuid.UUID(scan_id))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    scan_queue.subscribe(on_message)


if __name__ == '__main__':
    workers = 2
    pool = multiprocessing.Pool(processes=workers)
    for i in range(0, workers):
        pool.apply_async(run)

    try:
        app.run(host='0.0.0.0', port=5002, use_reloader=False, debug=True)
    except:
        pool.close()
        pool.join()
