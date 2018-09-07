import os
from jeeves_commons.utils import wait_for_port

from jeeves_commons.constants import (POSTGRES_HOST_IP_ENV,
                                      POSTGRES_HOST_PORT_ENV,
                                      RABBITMQ_HOST_IP_ENV,
                                      RABBITMQ_HOST_PORT_ENV,
                                      DEFAULT_BROKER_PORT,
                                      DEFAULT_POSTGRES_PORT)


try:
    postgres_port = int(os.getenv(POSTGRES_HOST_PORT_ENV,
                                  DEFAULT_POSTGRES_PORT))
except ValueError:
    postgres_port = DEFAULT_POSTGRES_PORT

try:
    rabbitmq_port = int(os.getenv(RABBITMQ_HOST_PORT_ENV,
                                  DEFAULT_BROKER_PORT))
except ValueError:
    rabbitmq_port = DEFAULT_BROKER_PORT


def wait():
    print 'waiting for postgres DB service...'
    connected = wait_for_port(host=os.getenv(POSTGRES_HOST_IP_ENV,
                                             '172.17.0.2'),
                              port=postgres_port,
                              duration=30)
    if not connected:
        raise RuntimeError('failed waiting for postgres DB')

    print 'waiting for rabbitmq service...'
    connected = wait_for_port(host=os.getenv(RABBITMQ_HOST_IP_ENV,
                                             '172.17.0.3'),
                              port=rabbitmq_port,
                              duration=30)
    if not connected:
        raise RuntimeError('failed waiting for rabbitmq broker')

wait()
