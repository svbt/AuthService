import os
import json
from confluent_kafka import Producer

from app.core.config import settings

# Create a single, application-wide producer instance for efficiency.
producer = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    """Callback for Kafka message delivery reports."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def get_kafka_producer() -> Producer:
    """Returns the pre-initialized Kafka producer instance."""
    return producer

def publish_login_event(user_id: str, providers: list[str]):
    """Publishes a user login event to Kafka."""
    from datetime import datetime, timezone

    login_event = {
        "user_id": user_id,
        "providers": providers,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    event_payload = json.dumps(login_event).encode('utf-8')

    producer.produce(settings.KAFKA_USER_TOPIC, value=event_payload, callback=delivery_report)
    producer.poll(0)

