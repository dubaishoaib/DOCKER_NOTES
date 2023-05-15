FROM node

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

CMD ["node", "app.js"]

# host.docker.internal use to access host system network 
# docker build -t fav-node .
# docker run -d --rm --network favs-network --name mongodb mongo
# docker run --name favs --network favs-network -d --rm -p 3000:3000 fav-node