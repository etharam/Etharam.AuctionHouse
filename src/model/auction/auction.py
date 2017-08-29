from datetime import date

from src.model.auction.auction_error import AuctionError


class Auction:
    AUCTION_PURCHASED = 'AUCTION_PURCHASED'
    AUCTION_CREATED_TYPE = 'AUCTION_CREATED'

    def __init__(self):
        self._events = []

    @property
    def events(self):
        return self._events

    @classmethod
    def _create_auction_event(cls, auction_id, auctioneer, item, expiration_date, selling_price):
        return {
            'type': cls.AUCTION_CREATED_TYPE,
            'auction_id': auction_id,
            'auctioneer': auctioneer,
            'item': item,
            'expiration_date': expiration_date.isoformat(),
            'selling_price': selling_price
        }

    @classmethod
    def create(cls, auction_id, auctioneer, item, expiration_date, selling_price):
        cls.verify_invariants(selling_price=selling_price, expiration_date=expiration_date)
        auction = Auction()
        auction_created = cls._create_auction_event(auction_id, auctioneer, item, expiration_date, selling_price)
        auction.events.append(auction_created)
        return auction

    def buy(self):
        auction_purchased = {'auction_id': self.id, 'type': self.AUCTION_PURCHASED}
        self.events.append(auction_purchased)
        

    @classmethod
    def verify_invariants(cls, selling_price, expiration_date):
        if selling_price < 1:
            raise AuctionError('selling price must be greater than 1')
        if expiration_date < date.today():
            raise AuctionError('expiration date cannot be before today')

    @classmethod
    def rebuild(cls, events):
        auction = Auction()
        for event in events:
            auction._process(event)
        return auction

    def _process(self, event):
        processors = {
            self.AUCTION_CREATED_TYPE: self._process_created_event
        }
        processors[event['type']](event)

    def _process_created_event(self, event):
        self.id = event['auction_id']

