FROM node

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

ENV MONGODB_USERNAME root
ENV MONGODB_PASSWORD secret

EXPOSE 80

CMD ["npm", "start"]

# docker run -d --rm -p 27017:27017 --name mongodb mongo
# update 'mongodb://172.18.0.2:27017/course-goals', i.e. container ip
# docker build -t goals-node .
# docker container run --name goals-backend --rm -d -p 80:80 goals-node
# docker network create goals-net
# docker run -d --rm --network goals-net --name mongodb mongo
# update 'mongodb://mongodb:27017/course-goals', i.e. container name
# docker build -t goals-node .
# docker container run --name goals-backend --rm -d --network goals-net goals-node
# docker container stop goals-backend
# docker container run --name goals-backend --rm -d -p 80:80 --network goals-net goals-node
# docker container stop mongodb
# docker container run -d --rm --network goals-net --name mongodb -v data:/data/db mongo
# docker container stop mongodb
# docker container run -d --rm --network goals-net --name mongodb -v data:/data/db mongo
# docker run -d --rm --network goals-net --name mongodb -v data:/data/db -e MONGO_INITDB_ROOT_USERNAME=max -e MONGO_INITDB_ROOT_PASSWORD=secret mongo
# docker container stop goals-backend
# update url to mongodb://max:secret@mongodb:27017/course-goals
# docker build -t goals-node .
# docker container run --name goals-backend --rm -d -p 80:80 --network goals-net goals-node
# docker run --name goals-backend -v /home/shoaib/my-docker-tests/multi-container/backend:/app \ 
#  -v logs:/app/logs -v /app/node_modules -d --rm -p 80:80 --network goals-net goals-node
# change to CMD ["npm", "start"] with nodemon
# docker container stop goals-backend
# docker build -t goals-node .
## docker run --name goals-backend -v /home/shoaib/my-docker-tests/multi-container/backend:/app \ 
#  -v logs:/app/logs -v /app/node_modules -e MONGODB_USERNAME max -d --rm -p 80:80 --network goals-net goals-node
