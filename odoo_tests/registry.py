# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).


import threading
import itertools
import psycopg2
import logging

from odoo.modules.registry import Registry, DummyRLock

_logger = logging.getLogger(__name__)
_saved_locks = {}
_cursors = {}


class TestCursor(object):
    """A pseudo-cursor to be used for tests, on top of a real cursor. It keeps
    the transaction open across requests, and simulates committing, rolling
    back, and closing:
          test cursor           | queries on actual cursor
        ------------------------+---------------------------------------
          cr = TestCursor(...)  | SAVEPOINT test_cursor_N
                                |
          cr.execute(query)     | query
                                |
          cr.commit()           | SAVEPOINT test_cursor_N
                                |
          cr.rollback()         | ROLLBACK TO SAVEPOINT test_cursor_N
                                |
          cr.close()            | ROLLBACK TO SAVEPOINT test_cursor_N
                                |
    """

    _savepoint_seq = itertools.count()

    def __init__(self, cursor, lock):
        self._closed = False
        self._cursor = cursor
        # we use a lock to serialize concurrent requests
        self._lock = lock
        self._lock.acquire()
        # in order to simulate commit and rollback, the cursor maintains a
        # savepoint at its last commit
        self._savepoint = "test_cursor_%s" % next(self._savepoint_seq)
        self._cursor.execute('SAVEPOINT "%s"' % self._savepoint)

    def close(self):
        if not self._closed:
            self._closed = True
            self._cursor.execute('ROLLBACK TO SAVEPOINT "%s"' % self._savepoint)
            self._lock.release()

    def autocommit(self, on):
        _logger.debug("TestCursor.autocommit(%r) does nothing", on)

    def commit(self):
        self._cursor.execute('SAVEPOINT "%s"' % self._savepoint)

    def rollback(self):
        self._cursor.execute('ROLLBACK TO SAVEPOINT "%s"' % self._savepoint)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        self.close()

    def __getattr__(self, name):
        value = getattr(self._cursor, name)
        if callable(value) and self._closed:
            raise psycopg2.OperationalError("Unable to use a closed cursor.")
        return value


def enter_test_mode(self, cr=False):
    """Enter the 'test' mode, where one cursor serves several requests."""
    if not cr:
        cr = _cursors.get(self.db_name, None)
    assert self.test_cr is None
    self.test_cr = cr
    self.test_lock = threading.RLock()
    assert _saved_locks.get(self.db_name, None) is None
    _saved_locks[self.db_name] = Registry._lock
    Registry._lock = DummyRLock()


def leave_test_mode(self):
    """Leave the test mode."""
    assert self.test_cr is not None
    self.test_cr = None
    self.test_lock = None
    assert _saved_locks.get(self.db_name, None) is not None
    Registry._lock = _saved_locks.get(self.db_name, None)
    _saved_locks.pop(self.db_name, None)


def cursor(self):
    """Return a new cursor for the database. The cursor itself may be used
    as a context manager to commit/rollback and close automatically.
    """
    cr = self.test_cr
    if cr is not None:
        # While in test mode, we use one special cursor across requests. The
        # test cursor uses a reentrant lock to serialize accesses. The lock
        # is granted here by cursor(), and automatically released by the
        # cursor itself in its method close().
        return TestCursor(self.test_cr, self.test_lock)
    cr = self._db.cursor()
    _cursors[self.db_name] = cr
    return cr

Registry.enter_test_mode = enter_test_mode
Registry.leave_test_mode = leave_test_mode
Registry.cursor = cursor


from odoo.workflow.helpers import Session

def __init__(self, cr, uid):
    # assert isinstance(cr, odoo.sql_db.Cursor)
    assert isinstance(uid, (int, long))
    self.cr = cr
    self.uid = uid

Session.__init__ = __init__