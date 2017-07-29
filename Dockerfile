WORKDIR /usr/src/app
RUN mkdir example
WORKDIR ./example

COPY * ./

CMD ["python", "-m", "http.server", "8080"]

EXPOSE 8080
