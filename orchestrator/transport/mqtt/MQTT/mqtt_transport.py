# mqtt_transport.py

from sb_utils import Consumer, safe_cast
from callbacks import Callbacks

# Begin consuming messages from internal message queue
try:
    consumer = Consumer(
        exchange='transport',
        routing_key="mqtt",
        callbacks=[Callbacks.send_mqtt]
    )
except:
    consumer.shutdown()


    