import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from shared.data_access.db.mock_scan_store import MockScanStore
from shared.data_access.db.postgres_scan_store import PostgresScanStore
from shared.data_access.cache.scan_status_cache import ScanStatusCache
from shared.data_access.cache.mock_scan_status_cache import MockScanStatusCache
from shared.data_access.cache.redis_scan_status_cache import RedisScanStatusCache
from shared.data_access.db.scan_store import ScanStore
from shared.data_access.queues.scan_queue import ScanQueue
from shared.data_access.queues.mock_scan_queue import MockScanQueue
from shared.data_access.queues.rabbit_scan_queue import RabbitScanQueue
from shared.objects.scan_status import ScanStatus

app = Flask(__name__)

scan_store: ScanStore
scan_cache: ScanStatusCache
scan_queue: ScanQueue


def start_new_scans():
    new_scan_ids = scan_store.get_new_scan_ids()
    for scan_id in new_scan_ids:
        scan_store.set_status(scan_id[0], ScanStatus.running)
        scan_queue.send_scan(scan_id[0])


bc_start_new_scans = BackgroundScheduler(daemon=True)
bc_start_new_scans.add_job(start_new_scans, 'interval', seconds=10)
bc_start_new_scans.start()


def update_status_cache():
    id_status_map = scan_store.get_id_status_map()
    if id_status_map:
        scan_cache.save(id_status_map)


bc_update_status_cache = BackgroundScheduler(daemon=True)
bc_update_status_cache.add_job(update_status_cache, 'interval', seconds=10)
bc_update_status_cache.start()


@app.route('/api/', methods=['GET'])
def get_scan_status():
    return "Healthy"


if __name__ == '__main__':
    if os.getenv('RABBIT_HOST', None) is not None:
        scan_queue = RabbitScanQueue(os.environ["RABBIT_HOST"])
    else:
        scan_queue = MockScanQueue()

    if os.getenv('REDIS_HOST', None) is not None:
        scan_cache = RedisScanStatusCache(os.environ["REDIS_HOST"])
    else:
        scan_cache = MockScanStatusCache()

    if os.getenv('POSTGRES_CONNECTION', None) is not None:
        scan_store = PostgresScanStore(os.environ["POSTGRES_CONNECTION"])
    else:
        scan_store = MockScanStore()

    app.run(host='0.0.0.0', port=5001, use_reloader=False, debug=True)
