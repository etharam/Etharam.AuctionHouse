from expects import expect, equal, have_len, raise_error

from specs.helpers.mamba_keywords import description, context, it
from datetime import date, timedelta

class Auction:
    def __init__(self, auction_id, auctioneer, item, expiration_date, selling_price):
        self._auction_id = auction_id
        self._auctioneer = auctioneer
        self._item = item
        self._expiration_date = expiration_date
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
            'expiration_date': self._expiration_date.isoformat(),
            'selling_price': self._selling_price
        }

    @classmethod
    def create(cls, auction_id, auctioneer, item, expiration_date, selling_price):
        cls.verify_invariants(selling_price=selling_price, expiration_date=expiration_date)
        auction = Auction(auction_id, auctioneer, item, expiration_date, selling_price)
        auction.events.append(auction._create_auction_event())
        return auction

    @classmethod
    def verify_invariants(cls, selling_price, expiration_date):
        if selling_price < 1:
            raise AuctionError()
        if expiration_date < date.today():
            raise AuctionError()


class AuctionError(Exception):
    pass


def auction_with(price, expiration_date=date.max):
    return Auction.create(auction_id='an_auction_id', auctioneer='an_auctioneer_id', item='an_item_id',
                          expiration_date=expiration_date, selling_price=price)


with description('Auction'):
    with context('on creation success'):
        with it('produces an event of auction created'):
            price = 600
            auction = auction_with(price=price, expiration_date=date.today())

            expect(auction.events).to(have_len(1))
            expect(auction.events[0]).to(equal({
                'type': 'AUCTION_CREATED',
                'auction_id': 'an_auction_id',
                'auctioneer': 'an_auctioneer_id',
                'item': 'an_item_id',
                'expiration_date': date.today().isoformat(),
                'selling_price': price
            }))

    with context('on invariants failed'):
        with it('does not allow the creation when selling price is less than 1'):
            auction = lambda: auction_with(price=0)

            expect(auction).to(raise_error(AuctionError))

        with it('does not allow the creation when expiration date is before today'):
            yesterday = date.today() - timedelta(days=1)
            auction = lambda: auction_with(price=600, expiration_date=yesterday)

            expect(auction).to(raise_error(AuctionError))
