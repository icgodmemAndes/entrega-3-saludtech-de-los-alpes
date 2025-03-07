import logging
import traceback
import _pulsar
import aiopulsar

from . import utils


async def subscribe_to_topic(topic: str, schema: str, subscription: str,
                             consumer_type: _pulsar.ConsumerType = _pulsar.ConsumerType.Shared, events=None):
    if events is None:
        events = []

    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as client:
            json_schema = utils.get_schema_registry(schema)
            avro_schema = utils.get_schema_avro_to_dict(json_schema)

            async with client.subscribe(
                    topic,
                    consumer_type=consumer_type,
                    subscription_name=subscription,
                    schema=avro_schema,
            ) as consumer:
                while True:
                    message = await consumer.receive()
                    data = message.value()
                    print(f'Consumed message from {topic}: {data}')
                    events.append({ 'topic': topic, 'data': str(data) })
                    await consumer.acknowledge(message)
    except:
        logging.error(f'Error: During subscription total {subscription} to topic! {topic}')
        traceback.print_exc()
