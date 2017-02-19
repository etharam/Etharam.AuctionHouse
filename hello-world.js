console.log("Hello World!! From Docker");

var amqp = require('amqplib/callback_api');

amqp.connect('amqp://message_broker', function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'hello';

    ch.assertQueue(q, {durable: false});
    // Note: on Node 6 Buffer.from(msg) should be used
    ch.sendToQueue(q, new Buffer('Hello World!'));
    console.log(" [x] Sent 'Hello World!'");
  });
  setTimeout(() => conn.close(), 500);
});

amqp.connect('amqp://message_broker', function(err, conn) {
  conn.createChannel(function(err, ch) {
    var q = 'hello';

    ch.assertQueue(q, {durable: false});

    console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q);
    ch.consume(q, function(msg) {
    console.log(" [x] Received %s", msg.content.toString());
    }, {noAck: true});
  });
});