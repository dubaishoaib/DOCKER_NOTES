Docker Capabilities and no-new-privileges
=========================================

[Reference](https://raesene.github.io/blog/2019/06/01/docker-capabilities-and-no-new-privs/)

Capabilities and Docker
-----------------------
First a little background. Docker makes use of [capabilities](http://man7.org/linux/man-pages/man7/capabilities.7.html) as one of the layers of security that it applies to all new containers. Capabilities are essentially pieces of the privileges that the `root` user gets on a Linux system. They enable processes to perform some privileged operations without having the full power of that user, and are very useful to get away from the use of `setuid` binaries. Docker applies a restriction that when a new container is started, even if the root user is used, it won’t get all the capabilities of root, just a subset.

An important point to note is that, if your process doesn’t need any “root-like” privileges, it shouldn’t need any capabilities, and processes started by ordinary users don’t generally get granted any capabilities.


no-new-privileges
-----------------

So where does no-new-privileges come into all this? Well this is an option that can be passed as part of a `docker run` statement as a security option. The Docker documentation on it says you can use it

    If you want to prevent your container processes from gaining additional privileges
    

Basically if your container runs as a non-root user (as all good containers should) this can be used to stop processes inside the container from getting additional privileges.

Here’s a practical example. Say we have a Dockerfile that looks like this

    FROM ubuntu:18.04
    
    RUN cp /bin/bash /bin/setuidbash && chmod 4755 /bin/setuidbash
    
    RUN useradd -ms /bin/bash newuser
    
    USER newuser
    
    CMD ["/bin/bash"]
    

We’ve got another bash shell which we’ve made setuid root, meaning that it can be used to get root level privileges (albeit still constrained by Docker’s default capability set).

If we build this Dockerfile as `nonewpriv` then run

    docker run -it nonewpriv
    

we get landed into a bash shell as the `newuser` user. Running `/bin/setuidbash -p` at this point will make us root demonstrating that we’ve effectively escalated our privileges inside the container.

Now if we try launching the same container, but add the no-new-privileges flag

    docker run -it --security-opt=no-new-privileges:true nonewpriv
    

when we run `/bin/setuidbash -p` our escalation to root doesn’t work and our new bash shell stays running as the `newuser` user, foiling our privilege escalation attempt :)

So, this option is one worth considering if you’ve got containers being launched as a non-root user and you want to reduce the risk of malicious processes in the container trying to get additional rights.

 If you want to run your container as a non-root user, by doing `cap-drop=all` as part of the run statement. This has a similar effect in stopping the contained processes from gaining any Linux capabilities, and if your workloads support it, is a great idea for hardening your containers.


# Restrictions 

## Cgroups
 How much resource container can use. CPU, Memory, DISK I/O

## Namespaces
 Namespaces limit, what the container can see. So when we are using the host network name space, it could see more because it was in the host network name space, when we used shared networking namespace, it could see and interact with the other container because they shared the same interface. 
 And this is how when you're in a container and do PS and lists all the processes. 
 It doesn't lift anything because they're in separate namespaces. 
 And so, this is the Linux kernel protecting and isolating stuff.

## Capabilities
 capabilities are given this process, what am I allowed to do? How much restrictions, or how much access do I have? And can I mount file systems? Can I create new devices, can install kernel drivers and stuff like this.

## Seccomp
 basically limiting what a container can call at a system core level.

## AppArmor
 It's like a profile and you can you define that. You've got nginx and this is what nginx, which hasn't been exploited, its normal behavior should or shouldn't be allowed to do.

And so, these are restrictions which we have in place and on top of this Docker, have 
added additional functionality, 

## This will take CPU utilization sky rocket.
```
> :(){ :|: &};:
```
> 1 defining a function called colon :

> 2	Content of function is to call itself and then pipe the result of itself to itself. 
	And then release control &. { :|: &};

> 3	At the end execute it self.

To avoid this in docker there is --pids-limit option. It protects resources and system from extra process executions.

## Cgroup Settings
-Limit a container to a share of the resources
 How much a container should have 10% 50% of what else is available. What CPUs should be this container be allowed to run on. If you are concerned that a container, maybe a hundred percent and utilizing maximum, it doesn't interfere with other things happening.
 So you can spread and allocate different containers to different CPUs. 
 And so we are only will have max out one or two of  CPUs on a 32 box core, it just restric them. 

 Same for memory it's just limiting so you can only use one gig of an available 160.
 Block I/O and block performance levels and so this all helps you strict and limit what contain container can and cannot do. And how much impact it can have another thing for running on the system and there's a lot of other security settings as well.
 
 ```
 > --cpu-shares
 > --cpuset--cpus
 > --memory-reserveation
 > --kernet-memory
 > --blkio-weight (block IO)
 > --device-read-iops
 > --device-write-iops
```

## SECCOMP
This is basically a way to list which system calls are allowed or not allowed to execute.
In linux all applications interact with kernal via System calls.
```
> strace outputs all calls
```