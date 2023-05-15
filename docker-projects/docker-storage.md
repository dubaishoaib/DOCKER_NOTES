# Docker Graphdrivers
- Overlay
- Aufs
- Btrfs
- Zfs
- Devicemapper
- Vfs

## Overlay
 Overlayfs was added in the 3.18 kernel. This is important to note because if you are running overlay on an older kernel than 3.18 you are either:

 1. Not running the same overlay.
 2. Running a kernel with overlayfs backported onto it, which is what we call a “frankenkernel”. Frankenkernels are not to be trusted. This is not to say it won’t work, it might work great, but it’s not to be trusted.

 Overlay is great but you need a recent kernel. There are also some super obscure kernel bugs with regard to sockets or certain python packages [docker/docker#12080](https://github.com/moby/moby/issues/12080).

## Aufs
 Aufs is another great one. But it is not in the kernel by default which blows. On Ubuntu/Debian distros this is as easy as installing the kernel extras package but other distros it might not be as simple.

 To use the AUFS storage driver with Docker, you will need to install the appropriate kernel modules on your system. On Ubuntu, you can do this by running the following command:
```
> sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
```

Once the kernel modules are installed, you can start the Docker daemon with the 
--storage-driver flag set to aufs, like this:

```
> sudo dockerd --storage-driver=aufs
```

Please note that, again, this is not recommended as AUFS has known performance and reliability issues and it is recommended to use the overlay2 storage driver instead.

You can also remove the package that you installed to enable the AUFS storage driver by running the following command:

```
> sudo apt-get remove linux-image-extra-$(uname -r)
```

## Btrfs
 Btrfs is great too but you need to partition the disk you will use for /var/lib/docker as btrfs first. This is kinda a hurdle to jump that I don’t think a lot of people are willing to do.

## Zfs
 Zfs is another good one, of course, like btrfs it takes some setup and installing the zfs.ko on your system. But this driver might become a whole lot more popular if Ubuntu 16.04 ships with zfs support.

## Devicemapper
 Honestly it makes me super disappointed to say this, but buyer beware. Hey on the plus side…. it’s in the kernel. You must must must have all the devicemapper options set up perfectly or you will find yourself only being able to launch ~2 containers


### [Reference](https://blog.jessfraz.com/post/the-brutally-honest-guide-to-docker-graphdrivers/)


# Volume
Tells docker to map the current directory to /src in the container
```
> docker run -d -v $(pwd):/src -p 80:9292 jpetazzo/namer:master
```
  * docker -d flag indicates that the container should run in detached mode in the background.
  * The -v flag provides volume mounting inside containers.
  * the -p flag maps port 9292 inside the container to port 80 on the host
  * jpetazzo/namer is the name of the image we will run
  * Volumes are special directories in a container.
  * Declared in two different ways. 
  * Dockerfile with VOLUME /var/lib/postgressql
  * On command line with -v flag 
  ```
  > docker run -d -v /var/lib/postgressql training/postgressql
  ```
  * In both cases /var/lib/postgressql, inside the container will be a volume.
  * To list all volumes
  ```
  > docker volume ls
  > docker volume --create myVolume
  > docker run -ti -v myVolume:/volume alpine sh
  > docker run -ti -v myVolume:/something ubuntu
  ```
  * To view the volume, what is it having...
  ```
  > docker run -ti -v 46bac33675727dfb3c55b57715d6bdd2874003c54:/whatisthis ubuntu
  ```

### Mounting volumes inside containers.
  * the -v flag mounts a directory from your host into your Docker container.
  ```
  > [host-path]:[container-path]:[rw][ro]
  ```
  * if [host-path] or [container-path] doesn't exist it is created.
  * write status of the volume is controlled with the ro and rw options.
  * by default it is rw.
  * The main point of volume is to create a direct mapping between a directory on the  host and directory in the container.
  * This can be used to achieve native IO performance. Bcs when container is reading writing on the volume it directly read/write from the host without any overhead.
  * Bypassing copy-on-write to leave some files out of docker commit.
  * Use that to share between host and the container. And share between multiple containers.

# Sharing a single file between the host and a container
The same -v flag is used. One intersting example is to share the Docker control socket.
```
> docker run -it -v  /var/run/docker.sock:/var/run/docker.sock docker sh
```
So we are sharing the docker host `docker.sock` file with the container. When using such mounts, the container gains root-like access to the host.
```
> ls -l /var/run/
```
Docker uses a unix socket to communicate from client to the docker engine. And uses this socket for handshake.

# What happens when container with volumes is removed?
When a Docker container with volumes is removed, the data stored in the volumes is not removed along with the container. The data in the volumes will persist and can be accessed by other containers or the host system. If you wish to remove the data in the volumes along with the container, you can use the --rm or --volumes option with the docker rm command.
List all the docker instances running and not running.
```
> docker ps -qa
> docker ps -qa | xargs docker rm -f 
```
All the volumes are there even we have deleted all the containers.
```
> docker volume ls
```

## How to know which volume is without container?
* Use the docker volume ls command to list all the volumes on your host system,    including those that are not currently in use by any containers. The output will show the volume names and other information such as the driver used, the mount point and the status. 
* Use the docker volume inspect command followed by a volume name to see more detailed information about a specific volume.
* Another alternative is using the docker ps -a command, it will show all the container even if they are not running, you can cross check the container with the volume list and identify the volumes without a container.
* Use the docker volume ls command to list all the volumes on the host system.
* Volumes that are not currently in use by any container will have "local" listed under  the "DRIVER" column.
* Use docker volume ls -f dangling=true command to list the volumes that are not associated with any container.
* Additionally, Use docker ps -a to list all the containers and check the volume column, if it's empty the volume is not associated with any container.
* If you want to see the mapping between the volumes and the containers, you can use docker container inspect command and check the "Mounts" section, it will show you the volumes that are associated with that container.

# STORAGE
* To use the host as a backup, docker uses objects created by native storage drivers  provided by docker. For e.g. Volumes, Volumes are the directories on the host filesystem outside the scope of container and its writeable layer.
* They are storage sandboxes created on the filesystem of the host for the containers.
* The nature of storage will follow the configuration of the host.
* volumes can be located at `/var/lib/docker/volumes`
* Docker never modifies the original pulled image.
* It uses approach called `Copy on Write`, means keeping the original files intact and making changes on a copy When the changes are commited they are saved as a new image.
```
> docker volume ls 
DRIVER    VOLUME NAME
local     4b0740a6b09f654c515b428878ef4b344d28da39a7d6db3905a3247fd5be4edb
local     44801a586a4b58219682772f15f6ee397703532d4431a5dc39e554432734a359
```

* The `DRIVER` value `local` means, volumes are on the same host that runs the container.
* These volumes are directory on host machine, `/var/lib/docker/volumes`.
```
> cd /var/lib/docker/volumes
> docker volume create --name <volume_name>
> docker volume create --name vol-ubuntu
> docker volume inspect  vol-ubuntu
> "Mountpoint": "/var/lib/docker/volumes/vol-ubuntu/_data",
> docker run --rm -itd --name alpha-ubuntu -v vol-ubuntu:/etc ubuntu:latest
> cd /var/lib/docker/volumes/vol-ubuntu/_data
/var/lib/docker/volumes/vol-ubuntu/_data> touch temp.conf
> docker exec -it alpha-ubuntu bash
> ls /etc/
> docker run -itd --name alpha-centos \
  --mount source=vol-centos,destination=/etc,readonly \ 
  centos:latest
```

* --mount source=<volume>, target=<container_dir>, property

## PLUGIN
```
> docker plugin install tiborvass/sample-volume-plugin
```
```
> docker volume create --driver tiborvass/sample-volume-plugin --name vol-plug-busybox
```
```
> docker run -itd --name alpha-busybox \
  --mount type=volume,volume-driver=tiborvass/sample-volume-plugin,source=vol-plug-busybox,
  destination=/tmp \
  busybox
```
```
> docker exec -it alpha-busybox sh
```
```
> echo "This is busybox....." > /tmp/foo.txt
> ls /tmp
> foo.txt
> exit
```

## --volume-from CONTAINER_NAME/ID
```
> docker run -itd --name beta-busybox --volumes-from alpha-busybox:ro busybox
```
* `ro` is for `read-only`.
```
> docker inspect beta-busybox
```
* "RW": false, means read-only.
```
"Mounts": [
    {
        "Type": "volume",
        "Name": "vol-plug-busybox",
        "Source": "/data/vol-plug-busybox",
        "Destination": "/tmp",
        "Driver": "tiborvass/sample-volume-plugin:latest",
        "Mode": "",
        "RW": false,
        "Propagation": ""
    }
],
```
```
> docker volume rm vol-plug-busybox
> docker volume rm vol-plug-busybox --force
> Error response from daemon: remove vol-plug-busybox: volume is in use - [733a.., bde00...]
```
```
> docker rm 733aa5a6 bde009a6fb5f31c5cca --force
> docker volume rm vol-plug-busybox
> docker volume prune
```

## BIND MOUNT
* Use to mount any path on host to any path in the container.
```
> docker run -itd --name bind-nginx -P -v /home/shoaib_soomro/bind-nginx:/tmp nginx
```
```
> docker inspect bind-nginx
"Mounts": [
    {
        "Type": "bind",
        "Source": "/home/shoaib_soomro/bind-nginx",
        "Destination": "/tmp",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```