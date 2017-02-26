FROM node:7.5

RUN mkdir /code
COPY . /code
WORKDIR /code

RUN npm install

EXPOSE 8080