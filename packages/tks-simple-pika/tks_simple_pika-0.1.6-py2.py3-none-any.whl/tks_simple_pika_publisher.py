import pika
import os
import json
from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class Message(BaseModel):
    ''' DTO Notification'''
    id: str 
    type: str
    msg: str
    email: Optional[EmailStr]
    subject: Optional[str]
    phone: Optional[int]
    description: Optional[str]
    slack_channel: Optional[str]
    data: Optional[list]

    @validator('id')
    def default_id(cls, v):
        assert str(v).isnumeric(), 'must be numeric'
        return v

class TksSimplePikaPublisher():
    def __init__(self,  exchange, **message):
        if None == exchange:
            raise Exception('exchange param is neccesary')
        else:
            self.RABBITMQ_EXCHANGE = exchange
        self.validate_envs()
        self.message = Message(**message)

    #async def send(self): @TODO async
    def send(self):
        credentials = pika.PlainCredentials(self.RABBITMQ_USER, self.RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RABBITMQ_HOST, port=self.RABBITMQ_PORT))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.RABBITMQ_EXCHANGE, exchange_type=self.RABBITMQ_EXCHANGE_TYPE)
        #channel.queue_declare(queue='notifications', durable=True, arguments={'x-max-priority': 10})
        channel.confirm_delivery()
        try:
            body = json.dumps(json.loads(self.message.json()))
            # @TODO async await channel.basic_publish(exchange=self.RABBITMQ_NOTIFICATIONS_EXCHANGE, routing_key='', body=json.dumps(self.message), mandatory=True)
            channel.basic_publish(exchange=self.RABBITMQ_EXCHANGE, routing_key='', body=body, mandatory=True)
        except Exception as e:
            print(e)
        connection.close()

    def validate_envs(self):
        if None != os.getenv('RABBITMQ_HOST'):
            self.RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
        else:
            raise Exception('RABBITMQ_HOST env is neccesary')
        if None != os.getenv('RABBITMQ_PORT'):
            self.RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
        else:
            raise Exception('RABBITMQ_PORT env is neccesary')
        if None != os.getenv('RABBITMQ_USER'):
            self.RABBITMQ_USER = os.getenv('RABBITMQ_USER')
        else:
            raise Exception('RABBITMQ_PASSWORD env is neccesary')
        if None != os.getenv('RABBITMQ_PASSWORD'):
            self.RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
        else:
            raise Exception('RABBITMQ_PASSWORD env is neccesary')
        if None != os.getenv('RABBITMQ_EXCHANGE_TYPE'):
            self.RABBITMQ_EXCHANGE_TYPE = os.getenv('RABBITMQ_EXCHANGE_TYPE')
        else:
            raise Exception('RABBITMQ_EXCHANGE_TYPE env is neccesary')
