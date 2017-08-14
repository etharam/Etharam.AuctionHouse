class CreateAuction:
    def __init__(self, message_queue, id_generator):
        self._message_queue = message_queue
        self._id_generator = id_generator

    def execute(self, auction):
        self._message_queue.publish({
            'type': 'AUCTION_CREATED',
            'auction_id': self._id_generator.new_id(),
            'auctioner': auction['auctioner'],
            'item': auction['item'],
            'period': auction['period'],
            'selling_price': auction['selling_price']
        })