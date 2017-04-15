require('chai').should();
const sinon = require('sinon');

const eventBus = require('../infrastructure/eventBus');

describe('Event Bus', () => {
    const eventType = 'A BUS CONCRETE MESSAGE';
    let bus;

    beforeEach(() => {
        bus = eventBus();
    });

    it('should notify subscribers when a certain message is published', (done) => {
        const expectedText = "text message";
        const aShouldNonCalledSubscriber = sinon.spy();
        const subscriber = sinon.spy();
        bus.subscribe({type: 'Another Type', subscriber: aShouldNonCalledSubscriber});
        bus.subscribe({type: eventType, subscriber});

        const expectedData = { text: expectedText };
        bus.publish({
            type: eventType,
            data: expectedData
        });

        assertAsync(() => {
            aShouldNonCalledSubscriber.notCalled.should.be.true;
            subscriber.withArgs(expectedData).calledOnce.should.be.true;
            done();
        });
    });

    it('should notify all subscribers for the same message', (done) => {
        const firstSubscriber = sinon.spy();
        const secondSubscriber = sinon.spy();
        bus.subscribe({type: eventType, subscriber: firstSubscriber});
        bus.subscribe({type: eventType, subscriber: secondSubscriber});
        
        bus.publish({
            type: eventType
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