FROM node:16.16.0
EXPOSE 8081
WORKDIR /star-burger/frontend
ADD frontend /star-burger/frontend
RUN npm ci --dev
