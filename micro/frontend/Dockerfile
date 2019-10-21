FROM node:14.1.0-stretch

WORKDIR /code
COPY package.json /tmp/
COPY yarn.lock /tmp/
RUN npm i -g npm

RUN cd /tmp && yarn install

RUN cp -a /tmp/node_modules .
