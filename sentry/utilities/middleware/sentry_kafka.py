from kafka import KafkaProducer
from sentry.utilities.log import sentry_logger
from kafka import KafkaConsumer
import json
import uuid
import time


class KafkaClient:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    def produce_message(self, data):
        producer = KafkaProducer(bootstrap_servers=[self.bootstrap_servers],
                                 value_serializer=lambda v: v.encode('utf-8'))
        try:
            producer.send(self.topic, json.dumps(data))
        except:
            sentry_logger.logger.error(f'failed to produce message to topic - {self.topic}')

    def get_consumer_messages(self):
        consumer = KafkaConsumer(self.topic,
                                 auto_offset_reset='earliest',
                                 bootstrap_servers=[self.bootstrap_servers],
                                 group_id=str(uuid.uuid4()),
                                 consumer_timeout_ms=1000,
                                 enable_auto_commit=True,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                                 )
        time.sleep(3)
        record_list = {}
        while True:
            records = consumer.poll(60 * 1000)  # timeout in millis , here set to 1 min
            for tp, consumer_records in records.items():
                    for consumer_record in consumer_records:
                            record_list[consumer_record.timestamp] = consumer_record.value
            break
        return record_list