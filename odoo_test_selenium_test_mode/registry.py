# -*- coding: utf-8 -*--
# © 2022 Atingo Tadeusz Karpiński
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).


from odoo.modules.registry import Registry, DummyRLock
import threading

_saved_locks = {}


def enter_test_mode(self, cr):
    """Enter the 'test' mode, where one cursor serves several requests."""
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


Registry.enter_test_mode = enter_test_mode
Registry.leave_test_mode = leave_test_mode
