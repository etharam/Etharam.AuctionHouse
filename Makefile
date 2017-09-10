test:
	@docker build -t au/tests:latest .; \
	docker run -it -e GOOGLE_APPLICATION_CREDENTIALS='/code/credentials/test-pubsub.json' --name au_test au/tests:latest mamba --format documentation .; \
	docker rm au_test

start:
	@docker build -t auctionhouse:latest .; \
	docker run -p 5000:5000 auctionhouse:latest python src/hello.py;