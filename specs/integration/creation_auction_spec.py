import uuid
from time import sleep

from arrow import utcnow
from doublex import Spy, assert_that, called

from specs.helpers.mamba_keywords import *
from src.actions.create_auction import CreateAuction


class PubSubMessageBus:

    def __init__(self):
        from google.cloud import pubsub_v1
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, event):

        topic_path = self.publisher.topic_path('etharam-179219', 'auction-house')
        import json
        self.publisher.publish(topic_path, data=str.encode(json.dumps(event)))

    def subscribe(self, name, callback):
        subscription = self.subscriber.subscription_path('etharam-179219', 'consumer')

        self.subscriber.subscribe(subscription, callback=callback)


class UuidGenerator:
    def new_id(self):
        return str(uuid.uuid4())


class EventConsumer:
    def __init__(self, message_bus, event_store):
        self.message_bus = message_bus
        self.event_store = event_store

    def listen(self):
        self.message_bus.subscribe('parrot', callback=self.store)

    def store(self, event):
        self.event_store.persist(event)


class EventStore:
    def persist(self, event):
        pass


with description('Create auction'):
    with it('creates an auction publishing an event in the event bus'):
        fake_event_store = Spy(EventStore)
        pub_sub_message_bus = PubSubMessageBus()
        event = {
            'auctioner': str(uuid.uuid4()),
            'item': str(uuid.uuid4()),
            'period': utcnow().floor('day').isoformat(),
            'selling_price': 600
        }
        CreateAuction(pub_sub_message_bus, UuidGenerator()).execute(event)

        EventConsumer(pub_sub_message_bus, fake_event_store).listen()

        sleep(3)
        assert_that(fake_event_store.persist,  called())