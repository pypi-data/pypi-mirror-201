import json
import base64
import asyncio
import aio_pika
import logging
import copy
from typing import Optional
from aiormq.exceptions import ChannelNotFoundEntity
from aio_pika import Channel, Queue, Exchange, ExchangeType
import constants.rmq_config as rmq_config
from .abstract_rmq_consumer import RabbitMQConsumer

logger = logging.getLogger("async_rmq")


# Create a consumed queue
async def _prepare_consumed_queue(channel: Channel,
                                  queue_name: str,
                                  exchange_name: str,
                                  exchange_type: ExchangeType,
                                  binding: str,
                                  default_queue_params: dict,
                                  default_exchange_params: dict,
                                  dl_enabled: Optional[bool] = False,
                                  dl_exchange: Optional[str] = None) -> Queue:
    queue_params = copy.deepcopy(default_queue_params)
    exchange_params = copy.deepcopy(default_exchange_params)

    if dl_enabled:
        queue_params["arguments"]["x-dead-letter-exchange"] = dl_exchange
    queue = await channel.declare_queue(
        queue_name,
        **queue_params
    )
    await channel.declare_exchange(exchange_name, exchange_type, **exchange_params)
    await queue.bind(exchange_name, binding)

    return queue


# Create dead letter queue
async def _prepare_dead_letter_queue(channel: Channel,
                                     dl_queue_name: str,
                                     dl_exchange_name: str,
                                     dl_exchange_type: str,
                                     default_queue_params: dict,
                                     default_exchange_params: dict,
                                     bindings: Optional[list] = []) -> Queue:
    queue_params = copy.deepcopy(default_queue_params)
    exchange_params = copy.deepcopy(default_exchange_params)
    dead_letter_queue: Queue = await channel.declare_queue(dl_queue_name, **queue_params)
    dead_letter_exchange: Exchange = await channel.declare_exchange(dl_exchange_name, dl_exchange_type, **exchange_params)
    for routing_key in bindings:
        await dead_letter_queue.bind(dl_exchange_name, routing_key)

    return dead_letter_queue, dead_letter_exchange


# Running a consumer
async def run_consumer(consumer_class: RabbitMQConsumer,
                       default_queue_params: dict,
                       default_exchange_params: dict,
                       host: str,
                       port: int,
                       login: str,
                       password: str,
                       vhost: str,
                       queue_name: str,
                       exchange_name: str,
                       exchange_type: str,
                       binding: str,
                       dl_enabled: Optional[bool] = False,
                       dl_queue_name: Optional[str] = None,
                       dl_queue_params: Optional[dict] = {},
                       dl_exchange_name: Optional[str] = None,
                       dl_exchange_type: Optional[str] = None,
                       dl_exchange_params: Optional[dict] = {},
                       dl_bindings: Optional[list] = []) -> None:
    loop = asyncio.get_event_loop()

    rabbitmq_connection = await aio_pika.connect_robust(
        loop=loop,
        host=host,
        port=port,
        login=login,
        password=password,
        virtualhost=vhost
    )

    async with rabbitmq_connection.channel() as channel:
        await channel.set_qos(prefetch_count=1)

        if dl_enabled:
            dead_letter_queue, dead_letter_exchange = await _prepare_dead_letter_queue(channel,
                                                                                       dl_queue_name,
                                                                                       dl_exchange_name,
                                                                                       get_exchange_type(dl_exchange_type),
                                                                                       dl_queue_params,
                                                                                       dl_exchange_params,
                                                                                       dl_bindings)
        queue = await _prepare_consumed_queue(channel,
                                              queue_name,
                                              exchange_name,
                                              get_exchange_type(exchange_type),
                                              binding,
                                              default_queue_params,
                                              default_exchange_params,
                                              dl_enabled,
                                              dl_exchange_name)
        consumer = consumer_class(
            queue=queue
        )
        await consumer.consume()

    logger.info("Shutdown complete")
    await rabbitmq_connection.close()

async def send_message(msg_data, exchange_name, routing_key, host, port, login, password, vhost):
    connection = await aio_pika.connect_robust(
        host=host,
        port=port,
        login=login,
        password=password,
        virtualhost=vhost
    )
    async with connection:
        channel = await connection.channel()

        try:
            exchange = await channel.get_exchange(exchange_name)
            msg = aio_pika.Message(body=msg_data)
            await exchange.publish(
                msg,
                routing_key=routing_key
            )

        except ChannelNotFoundEntity:
            logger.warning("The message could not be sent because the exchange with the name '%s' was not found"
                           % exchange_name)


def get_exchange_type(s):
    if s == ExchangeType.DIRECT.value:
        return ExchangeType.DIRECT
    elif s == ExchangeType.TOPIC.value:
        return ExchangeType.TOPIC
    elif s == ExchangeType.FANOUT.value:
        return ExchangeType.FANOUT
    elif s == ExchangeType.HEADERS.value:
        return ExchangeType.HEADERS
    elif s == ExchangeType.X_CONSISTENT_HASH.value:
        return ExchangeType.X_CONSISTENT_HASH
    else:
        return None