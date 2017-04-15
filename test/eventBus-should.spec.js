require('chai').should();

const amqp = require('amqplib/callback_api');

function eventBus() {
    const subscribers = {};
    return {
        subscribe({message, subscriber} = {}) {
            subscribers[message] = [subscriber];
        },
        publish(event) {
            setTimeout(() => {
                subscribers[event.message].forEach(subscriber => subscriber(event.data));
            });
            
        }
    }
}

describe('Event Bus', () => {
    it('should notify subscribers when a certain message is published', (done) => {
        const bus = eventBus();
        const MESSAGE = 'A BUS CONCRETE MESSAGE';
        const expectedText = "text message";
        let nonCalledSubscriberStatus = false;
        const subscriber = (data) => {
            data.text.should.equal(expectedText);
            nonCalledSubscriberStatus.should.be.false;
            done();
        };
        const aShouldNonCalledSubscriber = () => {
            nonCalledSubscriberStatus = true;
        }
        bus.subscribe({message: 'Another Message', subscriber: aShouldNonCalledSubscriber});

        bus.subscribe({message: MESSAGE, subscriber});

        bus.publish({
            message: MESSAGE,
            data: { 
                text: expectedText
            }
        });
    })
});