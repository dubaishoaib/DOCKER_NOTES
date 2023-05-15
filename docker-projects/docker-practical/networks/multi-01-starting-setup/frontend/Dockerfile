FROM node


WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]

# docker build -t goals-react .
# docker container run --name goals-frontend --rm -d -p 3000:3000 goals-react
# after create network # docker network create goals-net
# update http://localhost/goals/ to http://goals-backend/goals/ in App.js
# docker build -t goals-react .
# docker container run --name goals-frontend --rm -d --network goals-net -p 3000:3000 goals-react
# revert changes  http://goals-backend/goals/ to http://localhost/goals/ in App.js
# docker build -t goals-react .
# docker container run --name goals-frontend --rm -d -p 3000:3000 goals-react
# docker container run --name goals-frontend --rm -d -p 3000:3000 goals-react
# docker container run -v /home/shoaib/my-docker-tests/multi-container/frontend/src:/app/src --name goals-frontend --rm -d -p 3000:3000 goals-react