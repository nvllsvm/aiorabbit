# coding: utf-8
import asyncio
import contextlib
import logging
import typing

from aiorabbit import client, exceptions
from aiorabbit.__version__ import version
from aiorabbit.client import DEFAULT_LOCALE, DEFAULT_PRODUCT, DEFAULT_URL

LOGGER = logging.getLogger('aiorabbit')


@contextlib.asynccontextmanager
async def connect(url: str = DEFAULT_URL,
                  locale: str = DEFAULT_LOCALE,
                  product: str = DEFAULT_PRODUCT,
                  loop: typing.Optional[asyncio.AbstractEventLoop] = None):
    """Asynchronous context manager that connects to RabbitMQ, returning
    a connected :class:`~aiorabbit.client.Client` as the target.

    .. code-block:: python3
       :caption: Example Usage

       async with aiorabbit.connect(RABBITMQ_URL) as client:
            await client.exchange_declare('test', 'topic')

    :param url: The URL to connect to RabbitMQ with
    :param locale: The locale for the connection, default `en-US`
    :param product: The product name for the connection, default `aiorabbit`
    :param loop: Optional :mod:`asyncio` event loop to use

    """
    rmq_client = client.Client(url, locale, product, loop)
    await rmq_client.connect()
    try:
        yield rmq_client
    finally:
        if not rmq_client.is_closed:
            LOGGER.debug('Closing the client from context manager')
            await rmq_client.close()

__all__ = [
    'client',
    'connect',
    'DEFAULT_PRODUCT',
    'DEFAULT_LOCALE',
    'DEFAULT_URL',
    'exceptions',
    'version'
]
