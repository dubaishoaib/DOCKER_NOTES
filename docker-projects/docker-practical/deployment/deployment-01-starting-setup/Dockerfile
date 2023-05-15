FROM node:14-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

EXPOSE 80

CMD ["node", "app.js"]


# docker build -t node-dep-example .
# docker container run -d --rm -p 80:80 --name node-dep node-dep-example
# docker tag node-dep-example-1 shoaibsoomro/node-example-1
# docker push shoaibsoomro/node-example-1