# Dockysh
A "wrapper" shell written in Python over **Docker Shell**. 
**Dockysh** try to speedup the typing of commands for Docker shell reducing the verbosity of command and in some cases providing a little of interactivity.

# Disclaimer
Dockysh does not replace Docker Shell but it's based on it. Dockysh use the **Python library** **[cmd](https://docs.python.org/3/library/cmd.html 'Python Cmd Library')** and little of **Bash** scripting to make easier and more user friendly some commands.

# Why this shell
For people that make an intense and interactive use of Docker shell **Dockysh** permit you to avoid to repeat some keywords like *docker container*, *docker images* and so on. For istance instead of type *docker container ls* you can type 
```
you@Dokysh$ lsc
```

and if you want filter the results you can type the command 

```
you@Dokysh$ lsc your_string_filter
```

# What you need to run this shell
To run this shell you need:
1. Bash shell
2. Docker installed
3. Python installed

For who want use this shell in *Windows* you can activate the *[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10 'Install WSL')*

# How this shell works
The shell is provided with a set of commands. Each command is just an alias to a specific **Docker Shell** command. Each alias command is translated and sent to **Docker Shell**. In case of command not mapped the shell try to run the command in **Docker shell**, so if you type the wrong command *command_not_mapped with_args* the shell try to run **docker command_not_mapped with_args**. As logical consequence you can run  each **Docker shell command** without the prefix *docker*.

# How to run the shell
Just run the following command: `python dockysh.py` and then type *?* or *help* for help:`you@Dokysh$ help`

# Examples

Following some examples of **Dockysh** commands.

Finding an image: `you@Dokysh$ lsi alpine` where *alpine* is a filter and return all Alpine images like shown following

```
you@Dokysh$ lsi alpine
REPOSITORY                                  TAG                              IMAGE ID       CREATED         SIZE
alpine                                      latest                           d4ff818577bc   6 weeks ago     6.4MB
```

Remove one or more images: `you@Dokysh$ rmi alpine` where *alpine* is a filter. 
In this case each image corresponding the filter provided will be removed after confirmation by the user:

```
you@Dokysh$ rmi alpine

Found 1 images in base your filter 'alpine'. Please confirm the deletion of the images found.

Do you want eliminate the image with id "d4ff818577bc" with tag "latest" of size "6.4MB" from repository "alpine"" ?
([Y]=> yes/ [N]=>no / [E]=> exit from this operation):Y

```

Finding container stopped: `you@Dokysh$ lsc down` where *down* is a filter on container status

Finding container running: `you@Dokysh$ lsc up` where *up* is a filter on container status

Finding container running: `you@Dokysh$ lsc b33526d46134` where *b33526d46134* is a filter on image of the container.

Finding containers by image id: `you@Dokysh$ lsc b33526d46134` where *b33526d46134* is a filter on image of the container.

Removing a container: `you@Dokysh$ rmc 192294a228b7` where *192294a228b7* is a filter representing the id of the container.

In this case each contianer corresponding the filter provided (one because we've used the id of container) will be removed after confirmation by the user:
```
Found 1 containers in base your filter '192294a228b7'. Please confirm the deletion of the containers found.

Do you want eliminate the container with id "192294a228b7" based on image with ID "b33526d46134" ?
([Y]=> yes/ [N]=>no / [E]=> exit from this operation): Y
```


