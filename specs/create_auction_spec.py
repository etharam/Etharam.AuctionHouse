from expects import expect, equal, have_len
from doublex import Stub

from specs.helpers.test_message_queue import TestMessageQueue
from specs.helpers.mamba_keywords import description, it

from src.actions.create_auction import CreateAuction


with description('Create Auction'):
    #TODO: use the aggregate in the action
    with it('raises an auction created event'):
        with Stub() as id_generator:
            id_generator.new_id().delegates(['an_auction_id'])
        message_queue = TestMessageQueue()
        create_auction = CreateAuction(message_queue, id_generator)

        create_auction.execute({
            'auctioner': 'an_auctioner_id',
            'item': 'an_item_id',
            'period': 'anything',
            'selling_price': 600 
        })

        raised_events = message_queue.events
        expect(raised_events).to(have_len(1))
        expect(message_queue.events[0]).to(equal({
            'type': 'AUCTION_CREATED',
            'auction_id': 'an_auction_id',
            'auctioner': 'an_auctioner_id',
            'item': 'an_item_id',
            'period': 'anything',
            'selling_price': 600
        }))