FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --production

COPY server.js ./
COPY site ./site
COPY data ./data

EXPOSE 80

CMD ["node", "server.js"]
