FROM node

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

ARG DEFAULT_PORT=8000

ENV PORT ${DEFAULT_PORT}

EXPOSE ${PORT}

# VOLUME [ "/app/node_modules" ]
# > docker container run -p 3000:80 -d --name feedback-node \ 
# -v feedback:/app/feedback \
# -v "/mnt/f/Learning/Docker/docker-projects/docker-practical/volumes/data-volumes-01-starting-setup:/app:ro" \
# -v /app/temp -v /app/node_modules --rm feedback-node:volumes
#
# > docker container run -p 3000:9000 --env PORT=9000 -d --name feedback-node \
# -v feedback:/app/feedback \ 
# -v "/mnt/f/Learning/Docker/docker-projects/docker-practical/volumes/data-volumes-01-starting-setup:/app:ro" \
# -v /app/temp -v /app/node_modules --rm feedback-node:env
#
# > docker container run -p 3000:9000 --env-file ./.env -d --name feedback-node \
# -v feedback:/app/feedback \ 
# -v "/mnt/f/Learning/Docker/docker-projects/docker-practical/volumes/data-volumes-01-starting-setup:/app:ro" \
# -v /app/temp -v /app/node_modules --rm feedback-node:envq 
####
CMD ["npm", "start"]