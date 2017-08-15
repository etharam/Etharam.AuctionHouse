from expects import expect, equal, have_len, raise_error

from specs.helpers.mamba_keywords import description, it


class Auction:
    def __init__(self, auction_id, auctioneer, item, period, selling_price):
        self._auction_id = auction_id
        self._auctioneer = auctioneer
        self._item = item
        self._period = period
        self._selling_price = selling_price
        self._events = []
        self._create_auction_event()

    @property
    def events(self):
        return self._events

    def _create_auction_event(self):
        return {
            'type': 'AUCTION_CREATED',
            'auction_id': self._auction_id,
            'auctioneer': self._auctioneer,
            'item': self._item,
            'period': self._period,
            'selling_price': self._selling_price
        }

    @classmethod
    def create(cls, auction_id, auctioneer, item, period, selling_price):
        cls.verify_invariants(selling_price=selling_price)
        auction = Auction(auction_id, auctioneer, item, period, selling_price)
        auction.events.append(auction._create_auction_event())
        return auction

    @classmethod
    def verify_invariants(cls, selling_price):
        if selling_price < 1:
            raise AuctionException()


class AuctionException(Exception):
    pass


with description('Auction'):
    with it('produces an event of auction created'):
        auction = Auction.create(auction_id='an_auction_id', auctioneer='an_auctioneer_id', item='an_item_id', period='anything', selling_price=600)

        expect(auction.events).to(have_len(1))
        expect(auction.events[0]).to(equal({
            'type': 'AUCTION_CREATED',
            'auction_id': 'an_auction_id',
            'auctioneer': 'an_auctioneer_id',
            'item': 'an_item_id',
            'period': 'anything',
            'selling_price': 600
        }))

    with it('does not allow the creation when selling price is less than 1'):
        auction = lambda: Auction.create(auction_id='an_auction_id', auctioneer='an_auctioneer_id', item='an_item_id', period='anything', selling_price=0)

        expect(auction).to(raise_error(AuctionException))