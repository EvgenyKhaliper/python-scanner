import datetime
import uuid
from typing import List, Dict
from uuid import UUID

import psycopg2
import psycopg2.extras

from shared.data_access.db.postgres_context import PostgresContext
from shared.data_access.db.scan_store import ScanStore
from shared.objects.scan import Scan
from shared.objects.scan_properties import ScanProperties
from shared.objects.scan_status import ScanStatus


class PostgresScanStore(ScanStore):
    def __init__(self, cn: str):
        self.cn = cn
        psycopg2.extras.register_uuid()

    def create_scan(self, scan: Scan):
        with PostgresContext(self.cn) as ctx:
            ctx.cur.execute("INSERT INTO scans (scan_id, status, date) VALUES (%s, %s, %s);",
                            (scan.scan_id, scan.status, datetime.date.today()))
            ctx.cur.execute("INSERT INTO scan_properties (scan_id, timeout) VALUES (%s, %s);",
                            (scan.scan_id, scan.properties.timeout))

    def get_new_scan_ids(self) -> List[UUID]:
        with PostgresContext(self.cn) as ctx:
            ctx.cur.execute('SELECT scan_id FROM scans WHERE status=%s;', (ScanStatus.accepted,))
            return ctx.cur.fetchall()

    def get_id_status_map(self) -> Dict[str, str]:
        with PostgresContext(self.cn) as ctx:
            ctx.cur.execute('SELECT scan_id, status FROM scans;')
            items = ctx.cur.fetchall()
            return {str(i[0]): i[1] for i in items}

    def get_scan_properties(self, scan_id: UUID) -> ScanProperties:
        with PostgresContext(self.cn) as ctx:
            ctx.cur.execute('SELECT * FROM scan_properties WHERE scan_id=%s;', (scan_id,))
            item = ctx.cur.fetchone()
            return ScanProperties(timeout=item[1])

    def set_status(self, scan_id: UUID, status: str):
        with PostgresContext(self.cn) as ctx:
            ctx.cur.execute("UPDATE scans SET status=%s WHERE scan_id=%s;", (status, scan_id,))
