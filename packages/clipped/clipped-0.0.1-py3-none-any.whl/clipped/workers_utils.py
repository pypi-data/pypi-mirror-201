import logging
import os
import signal
import threading
from contextlib import contextmanager
from typing import Generator, Optional

_logger = logging.getLogger("clipped.workers")


def get_pool_workers() -> int:
    return min(32, (os.cpu_count() or 1) + 4)


def get_core_workers(per_core: int, max_workers: Optional[int] = None) -> int:
    count = per_core * (os.cpu_count() or 1) + 1
    return max(count, max_workers) if max_workers else count


@contextmanager
def exit_context() -> Generator:
    exit_event = threading.Event()

    def _exit_handler(*args, **kwargs) -> None:
        _logger.info("Keyboard Interrupt received, exiting pool.")
        exit_event.set()

    original = signal.getsignal(signal.SIGINT)
    try:
        signal.signal(signal.SIGINT, _exit_handler)
        yield exit_event
    except SystemExit:
        pass
    finally:
        signal.signal(signal.SIGINT, original)


def get_wait(current: int) -> float:
    intervals = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

    if current >= 5:
        current = 5
    return intervals[current]
