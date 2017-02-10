const express = require('express');
const app = express();
const mongodb = require('mongodb');


app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/users', (req, res) => {
	mongodb.connect("mongodb://db:27017", (err, db) => {
		console.log(err);
		db.collection("users").find((err, cursor) => {
			cursor.toArray((err, users) => res.send(users));
		});
	});
})

app.post('/users', (req, res) => {
	mongodb.connect("mongodb://db:27017", (err, db) => {
		console.log(err);
		db.collection("users").insert({usuario: "pepe"}, (err, result) => {
			if (!err) {
				res.send("created!");
			}
		})
	});
})

app.listen(8080, function () {
  console.log('Example app listening on port 8080!');
});
