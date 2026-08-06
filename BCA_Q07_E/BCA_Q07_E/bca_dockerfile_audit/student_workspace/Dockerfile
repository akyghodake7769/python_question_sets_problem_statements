FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
USER node
CMD ["node", "server.js"]
