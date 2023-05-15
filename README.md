# DOCKER PRACTICE NOTES

## Docker Commands

* Run docker image
```
docker run nginx
```

* Pull/Download image
```
docker pull mysql
```

* Stop container
```
docker stop container-id
```

* List processes
```
docker ps 
docker ps -a
```

### Interactive Terminal mode (it) 
* (i)Keep STDIN open even if not attached 
* (t) Allocate a pseudo-TTY
```
docker run -it mysql 
```

* Mapping external volume
```
docker run -v /opt/datadir:/var/lib/mysql mysql
```

* Run docker image with environment variable
```
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql
```

* Run container and execute command when exit container
```
docker run ubuntu cat /etc/*release*
```

* Attach to running container
```
docker attach container-id
```

* Docker Run with Volume and Port Forwarding
```
docker run -p 8080:8080 -p 50000:50000 --restart=on-failure -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11
```

* Docker inpspect to view docker container properties
```
docker inspect cotanier-id/name
```

* Override entrypoint 
```
docker run --entrypoint sleep2.0 ubuntu-sleeper 10
```

* Docker run name the container
* docker run --links to link two container via a command line
```
docker run -d --name=redis redis
docker run -d -e POSTGRES_PASSWORD=password -e POSTGRES_HOST_AUTH_METHOD=trust --name=db postgres
docker run -d --name=vote -p 5000:80 --link redis:redis voting-app
docker run -d --name=result -p 5001:80 --link db:db result-app
docker run -d --name=worker --link redis:redis --link db:db worker
```

## Setting up docker private registry
https://github.com/rchidana/Docker-Private-Registry/
```
sudo docker run -d -p 5000:5000 --restart=always --name registry -v /certificates:/certificates -e REGISTRY_HTTP_TLS_CERTIFICATE=/certificates/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certificates/domain.key registry:2
```

* Docker file build by filename
```
docker build . -f Dockerfile2 -t tagName
```

* Docker image disk consumption by Images, Containers, Local Volumes, Build Cache.
```
> docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          4         0         563.8MB   563.8MB (100%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     0         0         0B        0B
```

* To view all the images and space consumption use -v flag.
```
> docker system df -v

Images space usage:

REPOSITORY         TAG       IMAGE ID       CREATED          SIZE      SHARED SIZE   UNIQUE SIZE   CONTAINERS
my-color-webapp    latest    39b2b5a6cccb   14 minutes ago   563.8MB   563.8MB       308B          0
my-simple-webapp   latest    2cc63189dffc   4 hours ago      563.8MB   563.8MB       254B          0
ubuntu             latest    6b7dfa7e8fdb   8 days ago       77.8MB    77.8MB        0B            0
hello-world        latest    feb5d9fea6a5   14 months ago    13.26kB   0B            13.26kB       0

Containers space usage:

CONTAINER ID   IMAGE     COMMAND   LOCAL VOLUMES   SIZE      CREATED   STATUS    NAMES

Local Volumes space usage:

VOLUME NAME   LINKS     SIZE

Build cache usage: 0B

CACHE ID   CACHE TYPE   SIZE      CREATED   LAST USED   USAGE     SHARED
```

* Docker orchestration
```
docker service create --replicas=100 nodejs
```

usefull linux commands
```
> docker stats
> uptime
> free -m
> df -h
> cat /proc/cpuinfo
> reboot
> shutdown now
> while :; do echo 'Hello World'; done
> fallocate
> truncate
> dd
```

## Docker Capabilities and no-new-privileges

```console
> docker run -it -u $(id -u) --security-opt no-new-privileges -v `pwd`:/exploit ubuntu bash
```

[Docker Capabilities and no-new-privileges
](https://raesene.github.io/blog/2019/06/01/docker-capabilities-and-no-new-privs/)

> --security-opt=no-new-privlileges this prevents the exploit from executing.

```console
> docker run -it -u $(id -u) --security-opt no-new-privlileges -v `pwd`:/exploit ubuntu bash
```

## To count number of packages in linux

```
> dpkg -l | wc -l
```

## List last run docker process
```
> docker ps -l
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS     NAMES
89d71fe62ae9   jpetazzo/clock   "/bin/sh -c 'while d…"   15 seconds ago   Up 14 seconds             youthful_villani
```

## Short form of docker processes
```
> docker ps -q
89d71fe62ae9
2591cb1dd248
24731652b6db
```

## Last Docker process started.
```
> docker ps -ql
89d71fe62ae9
```

## Docker logs
### Docker logs tail last 3 lines
```
> docker logs --tail 3 068
```

### Docker logs for last docker container 
```
> docker logs $(docker ps -ql)
```

### Docker logs for last docker container 
```
> docker logs $(docker ps -ql)
```

### Follow logs runtime
```
> docker logs --tail 10 --follow $(docker ps -ql)
```

## docker Stop and docker kill
 If after 10 sec of docker stop container is still runnning than it will send kill signal to exit the container forcefully.

## Process tree
```
> ps faux
```

## Detaching from container
use ^P^Q in sequence. Otherwise ^C will detach and kill the terminal.
* -t means "allocate me a terminal"
* -i means "connect stdin to the terminal"
REPL Read Eval Print loop. When attaching to REPL container the shell doesnot know what you just attached so ENTR or ^L will print the shell.

## Docker search registry online
docker search zookeeper

## Creating docker file from exsiting run instance.
```
> docker commit image-id image-tag-name 
```

## Creating tag of an image if not provided proper tag name.
```
> docker tag 105e8294a29b ubu-figlet
```

## Finding difference between the container base image and the current state of the container.
```
> docker diff contaier-id
```

## Docker Inspect
```
> docker inspect ticktock | less
```

## Give Container running status True or False
```
> docker inspect --format '{{.State.Running}}' ticktock
```

## Port Mapping
  * A simple, static web-server
  ```
  > docker run -d -P nginx
  ```
  * -d tells Docker to run image in background
  * -P tells Docker to make this service reachable from other Computers. -P is  short-version of --publish-all
  ```
  > docker ps -a 
  CONTAINER ID   IMAGE             COMMAND                  PORTS                                  
  7987bb3c5c24   nginx             "/docker-entrypoint.…"   0.0.0.0:49153->80/tcp, :::49153->80/tcp
  ```
  * 0.0.0.0:49153->80/tcp, :::49153->80/tcp means web server is running on port 80 inside container
  * That ports is mapped to port 49153 on Docker host
  * Manual allocation of port numbers
  ```
  > docker run -d -p 80:80 nginx
  > docker run -d -p 8000:80 nginx
  > docker run -d -p 8080:80 -p 8888:80 nginx
  ```
  * The convention is port-on-host:port-on-container

## List all the running containers ID
```
> docker ps -q
```
## Kill all the running dockers
```
> docker ps -q | xargs docker kill
```

## Start the redis container
```
> docker run --name red28 -d redis:2.8
```

## This is alpine container running in same network stack as redis network.
```
> docker run --net container:red28 -ti alpine sh
> apk add busybox-extras
```

## Connect to the redis server on localhost
```
> telnet localhost 6379
> INFO SERVER
> SET PLACE DXB
> SAVE
> QUIT
> docker stop red28
# Reusing red28 volume on new redis container of other version.
> docker run --volumes-from red28 -d --name red30 redis:3.0
> docker run --net container:red30 -ti alpine sh
```

## Not an init system
```
> sudo systemctl status docker
```
As two general rules, you shouldn't install software inside running containers 
(it will get lost as soon as your container exits), and commands like systemctl just don't work inside Docker. You might think of Docker as a way to package an application and not like a full-blown VM with an init system and users and processes

## Search 
```
> docker search --filter is-official=true mysql
> docker search --limit 7 mysql
> docker search --format "table {{.Name}}\t{{.Description}}\t{{.IsOfficial}}" --limit 10 --no-trunc mysql
```

## Registry
```
> docker run -d --name registry -p 5000:5000 --restart=always registry
> docker pull busybox
> docker tag busybox:latest localhost:5000/my-busybox
> docker push localhost:5000/my-busybox
> docker rmi localhost:5000/my-busybox
> docker pull localhost:5000/my-busybox
```
