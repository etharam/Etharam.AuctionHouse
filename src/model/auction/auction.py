from datetime import date

from src.model.auction.auction_error import AuctionError


class Auction:
    AUCTION_BID_ACCEPTED = 'AUCTION_BID_ACCEPTED'
    AUCTION_BID_SUBMITTED = 'AUCTION_BID_SUBMITTED'
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
        cls._verify_creation(selling_price=selling_price, expiration_date=expiration_date)
        auction = Auction()
        auction_created = cls._create_auction_event(auction_id, auctioneer, item, expiration_date, selling_price)
        auction.events.append(auction_created)
        return auction

    def buy(self):
        auction_purchased = {'auction_id': self.id, 'type': self.AUCTION_PURCHASED}
        self.events.append(auction_purchased)

    def bid_up(self, bid):
        if self._current_bid_amount > bid['amount']:
            raise AuctionError('new bids must increase the current one')
        self.events.append({
            'auction_id': self.id,
            'type': self.AUCTION_BID_SUBMITTED,
            'bidder_id': bid['id'],
            'bid_amount': bid['amount']
        })

    @classmethod
    def rebuild(cls, events):
        auction = Auction()
        for event in events:
            auction._process(event)
        return auction

    @classmethod
    def _verify_creation(cls, selling_price, expiration_date):
        if selling_price < 1:
            raise AuctionError('selling price must be greater than 1')
        if expiration_date < date.today():
            raise AuctionError('expiration date cannot be before today')

    def _process(self, event):
        processors = {
            self.AUCTION_CREATED_TYPE: self._process_created_event,
            self.AUCTION_BID_ACCEPTED: self._process_bid_accepted
        }
        processors[event['type']](event)

    def _process_bid_accepted(self, event):
        self._current_bid_amount = event['bid_amount']

    def _process_created_event(self, event):
        self.id = event['auction_id']
        self._current_bid_amount = 0

