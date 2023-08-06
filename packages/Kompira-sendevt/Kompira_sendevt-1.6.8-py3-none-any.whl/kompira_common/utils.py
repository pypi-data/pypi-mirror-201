# -*- coding: utf-8 -*-
import pytz
import sys
import psutil
from contextlib import contextmanager
from itertools import islice
from datetime import datetime
from multiprocessing.managers import SyncManager
from setproctitle import setproctitle, getproctitle

BASE_DATETIME = datetime(2020, 1, 1)


@contextmanager
def redirect_stdio(stdout, stderr):
    _stdout = sys.stdout
    _stderr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    try:
        yield
    finally:
        sys.stdout = _stdout
        sys.stderr = _stderr


def system_timezone():
    dt_aware = BASE_DATETIME.astimezone()
    tzname = dt_aware.tzname()
    for tz in pytz.all_timezones:
        if tzname == pytz.timezone(tz).tzname(BASE_DATETIME):
            return tz
    return 'UTC'


def ignore_exception(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        pass


def truncate_repr(data, length=64, end='...'):
    ext = '...' if len(data) > length else ''
    return repr(data[:length]) + ext


def truncate_join(iterable, limit=3, sep=', ', model='objects', end='...({} {})'):
    count = len(iterable)
    text = sep.join(str(o) for o in islice(iterable, limit))
    tail = end.format(count, model) if count > limit else ''
    return text + tail


class KompiraMPManager(SyncManager):
    @classmethod
    def _run_server(cls, *args, **kwargs):
        name = getproctitle().split(' ', 1)[0]
        setproctitle(f'{name} [MP-Manager]')
        return super()._run_server(*args, **kwargs)


_manager = None
def make_mpqueue(maxsize=0):
    global _manager
    if not isalive_mpmanager():
        _manager = KompiraMPManager()
        _manager.start()
    return _manager.Queue(maxsize)


def shutdown_mpmanager():
    global _manager
    if _manager:
        _manager.shutdown()
        _manager = None


def isalive_mpmanager():
    global _manager
    return _manager and _manager._process and _manager._process.is_alive()


def terminate_children(logger, timeout=5):
    def on_terminate(p):
        logger.debug("terminate_children: %s terminated", p)

    def is_exclude(p):
        global _manager
        if _manager and _manager._process and _manager._process.pid == p.pid:
            return True
        return False

    logger.debug("terminate_children: start")
    children = [p for p in psutil.Process().children() if not is_exclude(p)]
    for p in children:
        logger.warn("terminate_children: terminate process: %s", p)
        p.terminate()
    gone, alive = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
    for p in alive:
        logger.warn("terminate_children: kill process: %s", p)
        p.kill()
    logger.info("terminate_children: finish (terminated=%s, killed=%s)", len(gone), len(alive))
