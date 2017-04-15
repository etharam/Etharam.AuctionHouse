require('chai').should();
const sinon = require('sinon');

const amqp = require('amqplib/callback_api');

function eventBus() {
    const subscriptions = [];
    return {
        subscribe({type, subscriber} = {}) {
            subscriptions.push({type, subscriber});
        },
        publish(event) {
            subscriptions
                .filter(subscription => subscription.type == event.type)
                .forEach(subscription => setTimeout(() => subscription.subscriber(event.data)));
        }
    }
}

describe('Event Bus', () => {
    it('should notify subscribers when a certain message is published', (done) => {
        const bus = eventBus();
        const eventType = 'A BUS CONCRETE MESSAGE';
        const expectedText = "text message";
        let receivedText = '';
        const subscriber = (data) => {
            receivedText = data.text;
        };
        const aShouldNonCalledSubscriber = sinon.spy();
        bus.subscribe({type: 'Another Type', subscriber: aShouldNonCalledSubscriber});
        bus.subscribe({type: eventType, subscriber});

        bus.publish({
            type: eventType,
            data: { 
                text: expectedText
            }
        });

        assertAsync(() => {
            aShouldNonCalledSubscriber.notCalled.should.be.true;
            receivedText.should.equal(expectedText);
            done();
        });
    });

    it('should notify all subscribers for the same message', (done) => {
        const bus = eventBus();
        const MESSAGE = 'A BUS CONCRETE MESSAGE';
        const expectedText = "text message";
        const firstSubscriber = sinon.spy();
        const secondSubscriber = sinon.spy();
        bus.subscribe({type: MESSAGE, subscriber: firstSubscriber});
        bus.subscribe({type: MESSAGE, subscriber: secondSubscriber});
        
        bus.publish({
            type: MESSAGE,
            data: { 
                text: expectedText
            }
        });

        assertAsync(() => {
            firstSubscriber.calledOnce.should.be.true;
            secondSubscriber.calledOnce.should.be.true;
            done();
        });
    });

    function assertAsync(assertion) {
        setTimeout(assertion);
    }
});