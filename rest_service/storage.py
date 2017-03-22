from flask import current_app

from jeeves_commons.storage.storage import get_storage_client as get_storage


def get_storage_client():
    return current_app.config.setdefault('storage_client',
                                         get_storage())
