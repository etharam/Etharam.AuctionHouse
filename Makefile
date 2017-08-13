test:
	@docker build -t au/tests:1.0 .; \
	docker run -it -d --name au_test au/tests:1.0;
	docker exec -it au_test  mamba --format documentation .
	docker stop au_test
	docker rm au_test

start:
	@docker build -t auctionhouse:1.0 .; \
	docker run -p 5000:5000 auctionhouse:1.0; 