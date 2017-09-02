from datetime import date, timedelta

from expects import expect, equal, have_len, raise_error

from specs.helpers.mamba_keywords import description, context, it
from src.model.auction.auction import Auction
from src.model.auction.auction_error import AuctionError

AN_ITEM_ID = 'an_item_id'

AN_AUCTIONEER_ID = 'an_auctioneer_id'

AN_AUCTION_ID = 'an_auction_id'


def auction_with(price, expiration_date=date.max):
    return Auction.create(auction_id=AN_AUCTION_ID, auctioneer=AN_AUCTIONEER_ID, item=AN_ITEM_ID,
                          expiration_date=expiration_date, selling_price=price)

with description('Auction'):
    with it('is created'):
        expected_price = 600

        auction = Auction.create(
            auction_id=AN_AUCTION_ID,
            auctioneer=AN_AUCTIONEER_ID,
            item=AN_ITEM_ID,
            expiration_date=date.today(),
            selling_price=expected_price)

        expect(auction.events).to(have_len(1))
        expect(auction.events[0]).to(equal({
            'type': Auction.AUCTION_CREATED_TYPE,
            'auction_id': AN_AUCTION_ID,
            'auctioneer': AN_AUCTIONEER_ID,
            'item': AN_ITEM_ID,
            'expiration_date': date.today().isoformat(),
            'selling_price': expected_price
        }))

    with it('is not created when selling price is less than 1'):
        auction = lambda: auction_with(price=0)

        expect(auction).to(raise_error(AuctionError, 'selling price must be greater than 1'))

    with it('is not created when expiration date is before today'):
        yesterday = date.today() - timedelta(days=1)
        auction = lambda: auction_with(price=600, expiration_date=yesterday)

        expect(auction).to(raise_error(AuctionError, 'expiration date cannot be before today'))

    with it('accepts purchase of the item by its selling_price'):
        expected_price = 600
        auction = Auction.rebuild(
            [{
                'type': Auction.AUCTION_CREATED_TYPE,
                'auction_id': AN_AUCTION_ID,
                'auctioneer': AN_AUCTIONEER_ID,
                'item': AN_ITEM_ID,
                'expiration_date': date.today().isoformat(),
                'selling_price': expected_price
            }]
        )

        auction.buy()

        expect(auction.events).to(have_len(1))
        expect(auction.events[0]).to(equal({
            'auction_id': AN_AUCTION_ID,
            'type': Auction.AUCTION_PURCHASED
        }))

    with it('accepts a bid'):
        auction = Auction.rebuild(
            [{
                'type': Auction.AUCTION_CREATED_TYPE,
                'auction_id': AN_AUCTION_ID,
                'auctioneer': AN_AUCTIONEER_ID,
                'item': AN_ITEM_ID,
                'expiration_date': date.today().isoformat(),
                'selling_price': 600
            }]
        )

        auction.bid_up({'id': 'any_bidder', 'amount': 100})

        expect(auction.events).to(have_len(1))
        expect(auction.events[0]).to(equal({
            'auction_id': AN_AUCTION_ID,
            'type': Auction.AUCTION_BID_SUBMITTED,
            'bidder_id': 'any_bidder',
            'bid_amount': 100
        }))

    with it('does not accept bids which dont increase the previous one'):
        auction = Auction.rebuild(
            [{
                'type': Auction.AUCTION_CREATED_TYPE,
                'auction_id': AN_AUCTION_ID,
                'auctioneer': AN_AUCTIONEER_ID,
                'item': AN_ITEM_ID,
                'expiration_date': date.today().isoformat(),
                'selling_price': 600
            }, {
                'auction_id': AN_AUCTION_ID,
                'type': Auction.AUCTION_BID_ACCEPTED,
                'bidder_id': 'any_bidder',
                'bid_amount': 200
            }]
        )

        def bid_up():
            auction.bid_up({'id': 'another_bidder', 'amount': 100})

        expect(bid_up).to(raise_error(AuctionError, 'new bids must increase the current one'))
