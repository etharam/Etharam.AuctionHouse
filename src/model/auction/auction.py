from datetime import date

from src.model.auction.auction_error import AuctionError


class Auction:
    AUCTION_CREATED_TYPE = 'AUCTION_CREATED'

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
            'type': self.AUCTION_CREATED_TYPE,
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
            raise AuctionError('selling price must be greater than 1')
        if expiration_date < date.today():
            raise AuctionError('expiration date cannot be before today')