# How To Remove Docker Images, Containers, and Volumes
-------------------------------------------------------

## Purging All Unused or Dangling Images, Containers, Volumes, and Networks

clean up any resources — images, containers, volumes, and networks — that are dangling (not tagged or associated with a container):

```
> docker system prune
```

To additionally remove any stopped containers and all unused images (not just dangling images), add the -a flag to the command:
```
> docker system prune -a
```

Removing Docker Images
```
> docker rmi Image Image
```

### Remove dangling images
Docker images consist of multiple layers. Dangling images are layers that have no relationship to any tagged images. They no longer serve a purpose and consume disk space. They can be located by adding the filter flag -f with a value of dangling=true to the docker images command. 

* LIST:
```
> docker images -f dangling=true
```

* REMOVE:
```
> docker image prune
```

### Removing images according to a pattern
* LIST:
```
> docker images -a |  grep "pattern"
```

* REMOVE:
```
> docker images -a | grep "pattern" | awk '{print $3}' | xargs docker rmi
```

### Remove all images

* LIST:
```
> docker images -a
```

* REMOVE:
add the -q flag to pass the image ID to docker rmi
```
> docker rmi $(docker images -a -q)
```

### Removing Containers
```
> docker rm ID_or_Name ID_or_Name
```

### Remove a container upon exiting
```
> docker run --rm image_name
```

### Remove all exited containers
You can locate containers using docker ps -a and filter them by their **status: created, restarting, running, paused, or exited.** To review the list of exited containers, use the -f flag to filter based on status. When you’ve verified you want to remove those containers, use -q to pass the IDs to the docker rm command:

* List:
```
> docker ps -a -f status=exited
```

* Remove:
```
> docker rm $(docker ps -a -f status=exited -q)
```

#### Remove containers using more than one filter
* List:
```
> docker ps -a -f status=exited -f status=created
```

* Remove:
```
> docker rm $(docker ps -a -f status=exited -f status=created -q)
```

### Remove containers according to a pattern
You can find all the containers that match a pattern using a combination of docker ps and grep. When you’re satisfied that you have the list you want to delete, you can use awk and xargs to supply the ID to docker rm.

* List:
```
> docker ps -a |  grep "pattern”
```

* Remove:
```
> docker ps -a | grep "pattern" | awk '{print $1}' | xargs docker rm
```

### Stop and remove all containers
```
> docker stop $(docker ps -a -q)
> docker rm $(docker ps -a -q)
```

## Removing Volumes

* List:
```
> docker volume ls
```

* Remove:
```
> docker volume rm volume_name volume_name
```

### Remove dangling volumes - Docker 1.9 and later
Since the point of volumes is to exist independent from containers, when a container is removed, a volume is not automatically removed at the same time. When a volume exists and is no longer connected to any containers, it’s called a dangling volume. To locate them to confirm you want to remove them, you can use the docker volume ls command with a filter to limit the results to dangling volumes. When you’re satisfied with the list, you can remove them all with docker volume prune:

* List:
```
> docker volume ls -f dangling=true
```

* Remove:
```
> docker volume prune
```

### Remove a container and its volume
If you created an unnamed volume, it can be deleted at the same time as the container with the -v flag. Note that this only works with unnamed volumes. When the container is successfully removed, its ID is displayed. Note that no reference is made to the removal of the volume. If it is unnamed, it is silently removed from the system. If it is named, it silently stays present.

* Remove:
```
> docker rm -v container_name
```

### Reference [link](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes)

