test:
	@docker build -t au/tests:1.0 ./specs/; \
	docker run -it au/tests:1.0 mamba .;