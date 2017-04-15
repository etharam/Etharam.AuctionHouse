require('chai').should();

const amqp = require('amqplib/callback_api');

function eventBus() {
    const subscribers = [];
    return {
        subscribe({message, subscriber} = {}) {
            subscribers.push(subscriber);
        },
        publish(event) {
            setTimeout(() => {
                subscribers.forEach(subscriber => subscriber(event.data));
            });
            
        }
    }
}

describe('Event Bus', () => {

    it('should notify subscribers when a message is emited', (done) => {
        const bus = eventBus();
        const expectedText = "text message";
        const subscriber = (data) => {
            data.text.should.equal(expectedText);
            done();
        };

        bus.subscribe({message: 'Any message', subscriber});

        bus.publish({
            data: { 
                text: expectedText
            }
        });
    })
});