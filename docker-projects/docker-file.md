# Docker File
Starts with the bootfs (Boot File System) are used to store boot loaders i.e. the scripts that starts the system. This is where the container isolation begins. The bootfs provides isolated and reserves resource allocations. Which virtually separates the image from rest of the files on the host or on cloud. On top of that we have Base Image layer which is generally specified by the Dockerfile authors.
>
Next we have standard layers `RUN`, `WORKDIR`, `ENV`, `EXPOSE`, `CMD` etc. These layers are stored as intermediate images. These intermediate images are read-only and have there own image id. Intermediate Image layers are used for caching. To make caching simple we have intermediate images where each layer has its own significant identity and it separates itself from all other layers interm of use-ability. But intermediate images cannot be used on there own. Since they wouldn't be suffcient to run a container or process by themself. Because even the small image would consist of one `CMD` or `ENTERYPOINT` layer, which is not present in any simple `ADD` and `COPY` image.

# Docker File Format

  * First statement in Dockerfile should be `FROM` i.e. base image.
  * `MAINTAINER` goes into the metadata instruction about who is creating image.
  * The `RUN` instruction can be specified in two ways
  * 1: with shell wrapping, which runs the specified command inside a shell, with /bin/sh -c:

  ```
  RUN apt-get update
  ```
  * 2: Using the exec method, which avoid shell string expansion and allows execution in images that dont have /bin/sh:
  ```
  RUN [ "apt-get", "update" ]
  ```

 * RUN will do the following:
   * Execute a command
   * Record changes to the filesystem.
   * Work great to install libraries, packages and various files.
 * RUN will not do the following
   * Records state of processes
   * Automatically start daemons
   * To start automatically when the container runs, use CMD or ENTRYPOINT.

 * Collapsing Layers
   * It is possible to execute multiple commands in a single step:

        ```
        RUN apt-get update && apt-get install -y wget && apt-get clean
        ```

   * It is also possible to break commands into multiple lines:

        ```
        RUN apt-get update \
            && apt-get install -y wget \
            && apt-get clean
        ```
   * This will avoid creation of multiple layers.
 
 * The `EXPOSE` Instruction
   * The `EXPOSE` instruction tells Docker what ports are to be published in this image.

    ```
    EXPOSE 8080
    EXPOSE 80 443
    EXPOSE 53/tcp 53/udp
    ```
   
   * All ports are private by defualt
   * The Dockerfile doesn't control if a port is publicly available
   * When doing docker run -p <port> .... that port becomes public. Even not declared   
    in `EXPOSE`
   * When doing docker run -P without port number, all ports with `EXPOSE` become public.
   * A public port is reachable from other containers and from outside the host
   * A private port is not reachable from outside.

 * The `COPY` instruction
   * The `COPY` instruction adds file and contents from host to the image
  
    ``` 
    COPY . /src
    ```

   * This will add the contents of the build context i.e. the directory passed as an argument
   * To the directory /src in the container 
   * Only references to the files and directories inside the build context are valid.
   * Following two lines are equivalent:
  
    ```
    COPY . /src
    COPY / /src
    ```

   * Attempts to use out of the build context will be detected and blocked with Docker and build will fail.
  
    ```
    COPY / /src/
    ```
  
   * This will copy recursively all files and folders in src/ 

 * `ADD`
   * `ADD` work almost like COPY 
   * `ADD` can get remote files

    ```
    ADD http://www.example.com/webapp.jar /opt/
    ```

   * ADD will automatically unpack zip files and tar archives:

    ```
    ADD ./assets.zip /var/www/htdocs/assets/
    ```

   * Add will not automatically unpack remote archives.

 * `VOLUME`
   * The `VOLUME` instruction tells Docker that a specific directory should be a volume.
    ```
    VOLUME /var/lib/mysql
    ```
   * Filesystem access in volumes bypasses the copy-on-write layer, offering native performance to I/O done in those direcories.
   * Volumes can be attached to multiple containers allowing to "port" data over from a container to another, e.g. to upgrade a database to newer version.
   * It is posssible to start a container in "read-only" mode. The container filesystem will be made read-only. but volumes can still have read/write access if necessary.
 
 * The `WORKDIR` instruction
   * The `WORKDIR` instruction sets the wokring directory for subsequent instruction
   * It also effects `CMD` and `ENTRYPOINT`, since it sets the working directory used   
     when starting the container.
    
    ```
    WORKDIR /src
    ```
   * Can also specify `WORKDIR` again to change the working directory for further operations.

 * The `ENV` instruction
   * The `ENV` instruction specifies environment variables that should be set in any container launched from the image.
   
    ```
    ENV WEBAPP_PORT 8080
    ```

   * This will result in an environment variables being created in any container created from this image 

    ```
    WEBAPP_PORT=8080
    ```

  * Can also specify environment variables when using docker run

    ```
    > docker run -e WEBAPP_PORT=8080 -e WEBAPP_HOST=www.example.com ...
    ```

 * The `USER` instruction
   * The `USER` instruction sets the user name or UID to use when running the image.
   * It can be used multiple time to change back to root or to another user.

 * The `CMD` instruction
   * The `CMD` instruction is a default command run when a container is launched from the image.

 * `RUN` and `CMD` instruction comes in two forms.
   * This executes in a shell 

    ```
    CMD nginx -g "deamon off;"
    ```
   
   * The second one executes without shell processing:

    ```
    > CMD ["nginx", "-g", "daemon-off;"]
    ```

 * The `ENTRYPOINT` instruction
   * The ENTRYPOINT instruction is like the CMD instruction. But arguments given on the command line are appended to the entry point.
   * This runs "exec" `COMMAND`
   ```
   ENTRYPOINT ["/bin/ls"]
   ```
   * So if we run docker now. It will run /bin/ls -l
   ```
   > docker run training/ls -l
   ```
   * `CMD` and `ENTRYPOINT` interact
   ```
   ENTRYPOINT [ "nginx" ]
   CMD ["-g", "daemon off;"]
   ```
   * The ENTRYPOINT specifies the command to be run and the CMD specifies its options.
   * On the command line we can then potentially override the options when needed.
   ```
   > docker run -d <dockerhubUsername>/web-image -t
   ```
   * This will override the options CMD provded with new flags.

# Docker Images

Build from GIT REPO
```
> docker build https://github.com/cerulean-canvas/nginx.git -t nginx-git
```

Pipe the docker file to docker build command.
```
> docker build - < Dockerfile -t nginx-stin
```

Compressing BuildContext
```
> tar -zcvf nginx.tar.gz Dockerfile
```

This will build the docker image from remote tar.
```
docker build - < https://abc.com/sample.tar.gz 
```

This is useful when image build is required for CI/CD pipeline or build the images in bulk
```
> docker build - < nginx.tar.gz -t nginx-tarball
```

If tar is having more than one Dockerfile, its best to unzip it.
```
> tar -tf nginx.tar.gz 
```

Build KIT, by default it is disabled. It can be enabled in /etc/docker/docker.json file.
```
{ "features" : { "buildkit" : true}}
```
```
> DOCKER_BUILDKIT=1 docker build --progress=plain --no-cache -t nginx-buildkit .
```

## Multi Stage Build
Multi stage build allow more than on `FROM` statement with each one labelled as STAGE.

```
> docker history registry:latest
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
81c944c2288b   3 months ago   /bin/sh -c #(nop)  CMD ["/etc/docker/registr…   0B        
<missing>      3 months ago   /bin/sh -c #(nop)  ENTRYPOINT ["/entrypoint.…   0B        
<missing>      3 months ago   /bin/sh -c #(nop) COPY file:507caa54f88c1f38…   155B      
```
`nop` mean no operation; It means the files or configuration we have added or removed do not perform any computation on them. They don't create any child process from there operations.
```
> docker history registry:latest --no-trunc
> docker history --format "table {{.ID}}\t{{.CreatedBy}}" registry:latest
```

## Docker TAR file
```
> docker save --output busybox-save.tar busybox-save:latest
> git clone https://github.com/cerulean-canvas/docker-save-example.git
> docker load --input busybox-save.tar
```
