test:
	@docker build -t au/tests:1.0 .; \
	docker run -it au/tests:1.0 mamba --format documentation .;