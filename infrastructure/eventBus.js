const _ = require('lodash');

module.exports = function eventBus() {
    const subscriptions = [];
    return {
        subscribe({type, subscriber} = {}) {
            subscriptions.push({type, subscriber});
        },
        publish(event) {
            _(subscriptions)
                .filter({type: event.type})
                .each(subscription => setTimeout(() => subscription.subscriber(event.data)));
        }
    }
}