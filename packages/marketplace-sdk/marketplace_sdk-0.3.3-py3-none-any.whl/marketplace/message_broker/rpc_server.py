import json
import logging

import pika
from marketplace_standard_app_api.models.message_broker import MessageBrokerRequestModel

from .utils import calc_queue_name

logger = logging.getLogger(__name__)


class RpcServer:
    def __init__(self, host, application_id, application_secret, message_handler):
        self.queue_name = calc_queue_name(application_id, application_secret)
        self.message_handler = message_handler
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

        self.channel.queue_declare(queue=self.queue_name)

    def consume_messages(self):
        def callback(ch, method, properties, body):
            request_message = MessageBrokerRequestModel.parse_obj(
                json.loads(body.decode())
            )

            response_message = self.message_handler(request_message)

            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id,
                ),
                body=response_message.json(),
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        logger.info("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
