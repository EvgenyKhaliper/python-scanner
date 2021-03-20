import psycopg2


class PostgresContext:
    cn: str

    def __init__(self, cn: str):
        self.cn = cn

    def __enter__(self):
        self.conn = psycopg2.connect(self.cn)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.conn:
            self.conn.commit()

        if self.conn:
            self.conn.close()

        if self.conn:
            self.conn.close()
