test:
	@docker build -t au/tests:1.0 .; \
	docker run -it au/tests:1.0 mamba --format documentation .;

start:
	@docker build -t au/tests:1.0 .; \
	docker run -p 5000:5000 au/tests:1.0; 