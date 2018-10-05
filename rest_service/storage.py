from contextlib import contextmanager

from flask import current_app

from jeeves_commons.storage.storage import get_storage_client as get_storage


@contextmanager
def storage_client():
    client = current_app.config.setdefault('storage_client', get_storage())
    try:
        yield client
    finally:
        client.close()
