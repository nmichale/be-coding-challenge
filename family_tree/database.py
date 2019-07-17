from sqlalchemy import create_engine
from contextlib import contextmanager

from . import config


class FakeConnection(object):
    '''
    Fake connection object that just prints whatever sql is executed. SQLAlchemy would handle any extra
    formatting automatically if anything printed has incorrect syntax.

    '''


    def __init__(self):
        self.last_id = 0

    def execute(self, sql, params=None):
        # Uncomment to see SQL statements

        # if params:
        #     print(sql % params)
        # else:
        #     print(sql)

        if sql == 'SELECT LAST_INSERT_ID() as id;':
            self.last_id += 1
            return self.last_id


fake_conn = FakeConnection()


@contextmanager
def get_conn():
    '''
    Just a toy example of how I might interface with a database using a context manager to store data.
    :return: Database connection
    '''
    # db_engine = create_engine(config.db_url, pool_recycle=3600)
    # conn = db_engine.connect()

    try:
        yield fake_conn
    finally:
        # conn.close()
        # db_engine.dispose()
        pass

