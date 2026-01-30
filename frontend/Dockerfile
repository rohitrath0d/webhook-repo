FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build

EXPOSE 3000

RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]