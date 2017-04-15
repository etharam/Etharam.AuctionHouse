require('chai').should();

const amqp = require('amqplib/callback_api');

function eventBus() {
    const subscriptions = [];
    return {
        subscribe({message, subscriber} = {}) {
            subscriptions.push({message, subscriber});
        },
        publish(event) {
            subscriptions
                .filter((subscription => subscription.message == event.message))
                .forEach(subscription => setTimeout(() => subscription.subscriber(event.data)));
        }
    }
}

describe('Event Bus', () => {
    it('should notify subscribers when a certain message is published', (done) => {
        const bus = eventBus();
        const MESSAGE = 'A BUS CONCRETE MESSAGE';
        const expectedText = "text message";
        let receivedText = '';
        let nonCalledSubscriberStatus = false;
        const subscriber = (data) => {
            receivedText = data.text;
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

        setTimeout(() => {
            nonCalledSubscriberStatus.should.be.false;
            receivedText.should.equal(expectedText);
            done();
        });
    });

    it('should notify all subscribers for the same message', (done) => {
        const bus = eventBus();
        const MESSAGE = 'A BUS CONCRETE MESSAGE';
        const expectedText = "text message";
        let firstSubscriberCalled = false;
        let secondSubscriberCalled = false;
        const firstSubscriber = (data) => {
            firstSubscriberCalled = true;
        };
        const secondSubscriber = (data) => {
            secondSubscriberCalled = true;
        };
        bus.subscribe({message: MESSAGE, subscriber: firstSubscriber});

        bus.subscribe({message: MESSAGE, subscriber: secondSubscriber});

        
        bus.publish({
            message: MESSAGE,
            data: { 
                text: expectedText
            }
        });
        setTimeout(() => {
            firstSubscriberCalled.should.be.true;
            secondSubscriberCalled.should.be.true;
            done();
        });
    });
});