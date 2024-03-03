FROM node:16.13.1-alpine

WORKDIR /app

COPY package.json .
RUN npm install --registry=http://registry.npmmirror.com
CMD ["npm", "run", "serve"]