import json
import os
import uuid

from flask import Flask, request, jsonify
from flask_injector import FlaskInjector
from injector import singleton
from werkzeug.exceptions import HTTPException

from shared.data_access.cache.mock_scan_status_cache import MockScanStatusCache
from shared.data_access.cache.redis_scan_status_cache import RedisScanStatusCache
from shared.data_access.cache.scan_status_cache import ScanStatusCache
from shared.data_access.db.mock_scan_store import MockScanStore
from shared.data_access.db.postgres_scan_store import PostgresScanStore
from shared.data_access.db.scan_store import ScanStore
from shared.objects.scan import Scan
from shared.objects.scan_properties import ScanProperties
from shared.objects.scan_status import ScanStatus

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print(str(e))
    return jsonify(error="Service is not available, please try again later"), code


@app.route('/api/scan', methods=['POST'])
def create_scan(scan_store: ScanStore):
    data = json.loads(request.data)
    scan_id = uuid.uuid1()
    scan_store.create_scan(Scan(scan_id=scan_id,
                                status=ScanStatus.accepted,
                                properties=ScanProperties(
                                    timeout=data["timeout"])))

    return jsonify({"id": scan_id}), 202


@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan_status(cache: ScanStatusCache, scan_id):
    status = cache.get_status(scan_id=scan_id)
    return jsonify({"status": status})  # 404 should be better than custom status...


def configure(binder):
    if os.getenv('REDIS_HOST', None) is not None:
        binder.bind(
            ScanStatusCache,
            to=RedisScanStatusCache(os.environ["REDIS_HOST"]),
            scope=singleton,
        )
    else:
        binder.bind(
            ScanStatusCache,
            to=MockScanStatusCache(),
            scope=singleton,
        )

    if os.getenv('POSTGRES_CONNECTION', None) is not None:
        # host='localhost' dbname='testdb' user='admin' password='admin'
        binder.bind(
            ScanStore,
            to=PostgresScanStore(os.environ["POSTGRES_CONNECTION"]),
            scope=request,
        )
    else:
        binder.bind(
            ScanStore,
            to=MockScanStore(),
            scope=request,
        )


FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
