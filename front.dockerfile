FROM node:16.16.0
EXPOSE 8081
WORKDIR /star-burger
COPY package.json /star-burger
COPY package-lock.json /star-burger
COPY bundles /star-burger/bundles
COPY bundles-src /star-burger/bundles-src
COPY assets /star-burger/assets
RUN npm ci --dev
