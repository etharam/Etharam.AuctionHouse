module.exports = function eventBus() {
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