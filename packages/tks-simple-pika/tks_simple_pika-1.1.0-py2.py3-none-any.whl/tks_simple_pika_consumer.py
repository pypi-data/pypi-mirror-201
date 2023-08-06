# Simple pika implementation consumer
# Change os.env to decouple
import asyncio
import os
import pika
import logging
from decouple import config 
 


logger = logging.getLogger(__name__)

class TksSimplePikaConsumer():
    ''' Simple pika Consumer'''

    def __init__(self, exchange):
        if None == exchange:
            raise Exception('exchange param is neccesary')
        else:
            self.RABBITMQ_EXCHANGE = exchange
        self.validate_envs()

    async def callback(self, ch, method, properties, body):
        '''
            OVERWRITE CALLBACK
            This method must be overwrite as follows (verbatim)
        '''
        '''   
            consumer = TksSimplePikaConsumer('exchange_name')
            funcType = type(TksSimplePikaConsumer.callback)
            aysnc def __callback(self, ch, method, properties, body):
              ..... Here actions from you businees logic
            consumer.callback = __callback.__get__(consumer, TksSimplePikaConsumer)
            await consumer.consumer_start()
        '''
        print(" [x] %r %s %s %s" % (body, ch, method, properties))


    async def consumer_start(self):
        await asyncio.sleep(0.5)
        try:
            connection = await pika.BlockingConnection(pika.ConnectionParameters(host=self.RABBITMQ_HOST,port=self.RABBITMQ_PORT))
            channel = await connection.channel()
            await channel.exchange_declare(exchange=self.RABBITMQ_EXCHANGE,
                                     exchange_type=self.RABBITMQ_EXCHANGE_TYPE)
            result = await channel.queue_declare(queue='', exclusive=True)
            queue_name = await result.method.queue
            await channel.queue_bind(exchange=self.RABBITMQ_EXCHANGE, queue=queue_name)
            await channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=self.RABBITMQ_CHANNEL_AUTO_ACK)
            await channel.start_consuming()
        except Exception as e:
            logger.error(e)

    def validate_envs(self):
        if None != config('RABBITMQ_HOST'):
            self.RABBITMQ_HOST = config('RABBITMQ_HOST')
        else:
            raise Exception('RABBITMQ_HOST env is neccesary')
        if None != config('RABBITMQ_PORT'):
            self.RABBITMQ_PORT = config('RABBITMQ_PORT')
        else:
            raise Exception('RABBITMQ_PORT env is neccesary')
        if None != config('RABBITMQ_EXCHANGE_TYPE'):
            self.RABBITMQ_EXCHANGE_TYPE = config('RABBITMQ_EXCHANGE_TYPE')
        else:
            raise Exception('RABBITMQ_EXCHANGE_TYPE env is neccesary')
        self.RABBITMQ_CHANNEL_AUTO_ACK = config('RABBITMQ_CHANNEL_AUTO_ACK', True)








