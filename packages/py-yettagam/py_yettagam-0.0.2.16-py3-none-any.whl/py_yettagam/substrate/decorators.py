import logging
import time
from functools import wraps


logging.basicConfig(format='%(process)d : %(asctime)s : %(levelname)s\n%(funcName)s():%(lineno)i\n%(message)s\n',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def wait_while_syncing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        backoff = 1
        max_backoff = 15

        while self._is_syncing:
            logging.info(
                f"\n\n============= Waiting for {backoff} seconds to sync... =============\n\n")
            time.sleep(backoff)
            backoff *= 2
            if backoff > max_backoff:
                backoff = max_backoff

        return func(self, *args, **kwargs)

    return wrapper


def skip_if_syncing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._is_syncing:
            logging.info(
                f"Skipping {func.__name__} as the node is currently syncing.")
            return

        return func(self, *args, **kwargs)

    return wrapper


def skip_if_committing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._is_committing:
            logging.info(
                f"Skipping {func.__name__} as the node is currently syncing.")
            return

        return func(self, *args, **kwargs)

    return wrapper


def skip_if_uploading(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._is_uploading:
            logging.info(
                f"Skipping {func.__name__} as the node is currently syncing.")
            return

        return func(self, *args, **kwargs)

    return wrapper
