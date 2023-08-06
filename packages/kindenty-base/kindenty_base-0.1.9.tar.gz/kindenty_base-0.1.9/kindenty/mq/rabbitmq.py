import time
from configparser import ConfigParser

import pika
from kindenty.base import log
from pika.exchange_type import ExchangeType


class RabbitMq:
    def __init__(self):
        self.connection = None
        self.queue = None
        self.channel = None
        configParser = ConfigParser()
        configParser.read('conf/config.ini')
        host = configParser.get('rabbitmq', 'host')
        user = configParser.get('rabbitmq', 'userName')
        password = configParser.get('rabbitmq', 'password')
        virtualHost = configParser.get('rabbitmq', 'virtualHost')
        self.queueName = configParser.get('rabbitmq', 'queueName')
        self.routingKey = configParser.get('rabbitmq', 'routingKey')
        self.exchange = 'strategy.topic.exchange'
        userX = pika.PlainCredentials(user, password)
        self.parameters = pika.ConnectionParameters(host=host, virtual_host=virtualHost, credentials=userX)
        self.connect()

    def bindConsumer(self, fun):
        def callback(ch, method, prop, body):
            log.debug('method:%s,prop:%s,body:%s' % (method, prop, body))
            fun(method.routing_key, body)
            # self.channel.basic_ack(delivery_tag=method.delivery_tag)
        self.channel.basic_consume(queue=self.queueName, on_message_callback=callback, auto_ack=True)
        while True:
            try:
                self.channel.start_consuming()
            except Exception as e:
                log.error('rabbitmq consumer error', exc_info=e)
                if not self.connection or self.channel.is_closed:
                    self.connect()
                    self.channel.basic_consume(queue=self.queueName, on_message_callback=callback, auto_ack=True)
                time.sleep(1)

    def sendMsg(self, routingKey, body):
        self.channel.basic_publish(self.exchange, routing_key=routingKey, body=body)

    def close(self):
        self.connection.close()

    def connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=ExchangeType.topic,
                                      durable=True)
        self.queue = self.channel.queue_declare(self.queueName, durable=True)
        keys = self.routingKey.split(',')
        for key in keys:
            self.channel.queue_bind(queue=self.queueName, exchange=self.exchange, routing_key=key)
