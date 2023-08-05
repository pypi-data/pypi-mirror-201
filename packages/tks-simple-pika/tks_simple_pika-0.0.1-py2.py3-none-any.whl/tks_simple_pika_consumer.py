import asyncio
import os
import pika
import logging


logger = logging.getLogger(__name__)

class TksSimplePikaConsumer():
    ''' Simple pika Consumer'''

    def __init__(self, exchange):
        if None == exchange:
            raise Exception('exchange param is neccesary')
        else:
            self.RABBITMQ_EXCHANGE = exchange
        self.validate_envs()

    def callback(self, ch, method, properties, body):
        '''
            OVERWRITE CALLBACK
            This method must be overwrite as follows (verbatim)
        '''
        '''   
            consumer = TksSimplePikaConsumer('exchange_name')
            funcType = type(TksSimplePikaConsumer.callback)
            def __callback(self, ch, method, properties, body):
              ..... Here actions from you businees logic
            consumer.callback = __callback.__get__(consumer, TksSimplePikaConsumer)
            consumer.consumer_start()
        '''
        print(" [x] %r %s %s %s" % (body, ch, method, properties))


    def consumer_start(self):
        #await asyncio.sleep(0.5)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RABBITMQ_HOST,port=self.RABBITMQ_PORT))
            channel = connection.channel()
            channel.exchange_declare(exchange=self.RABBITMQ_EXCHANGE,
                                     exchange_type=self.RABBITMQ_EXCHANGE_TYPE)
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=self.RABBITMQ_EXCHANGE, queue=queue_name)
            channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=self.RABBITMQ_CHANNEL_AUTO_ACK)
            channel.start_consuming()
        except Exception as e:
            logger.error(e)

    def validate_envs(self):
        if None != os.getenv('RABBITMQ_HOST'):
            self.RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
        else:
            raise Exception('RABBITMQ_HOST env is neccesary')
        if None != os.getenv('RABBITMQ_PORT'):
            self.RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
        else:
            raise Exception('RABBITMQ_PORT env is neccesary')
        if None != os.getenv('RABBITMQ_EXCHANGE_TYPE'):
            self.RABBITMQ_EXCHANGE_TYPE = os.getenv('RABBITMQ_EXCHANGE_TYPE')
        else:
            raise Exception('RABBITMQ_EXCHANGE_TYPE env is neccesary')
        self.RABBITMQ_CHANNEL_AUTO_ACK = os.getenv('RABBITMQ_CHANNEL_AUTO_ACK') \
            if None != os.getenv('RABBITMQ_CHANNEL_AUTO_ACK') else True








