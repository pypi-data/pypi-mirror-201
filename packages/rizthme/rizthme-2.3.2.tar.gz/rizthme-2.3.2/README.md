# Rizthme

## Requierement

First step is to add in your environments variables,
a variables named "TOKEN" with in value, your discord application token.

do this with:

```console
foo@bar:~$ export TOKEN=<your token>
```

or

> Write a .env file at project root 

next, check that the ffmpeg module is installed on your device.

```console
foo@bar:~$ ffmpeg -version
```

if not

```console
foo@bar:~$ sudo apt install ffmpeg 
# or equivalent depending on your system
```

## To launch the discord client

```console
foo@bar:~$ python3 run.py
```

### Automatically script launching

#### For Linux user

For use automatically your virtual environment. (The virtual environment name need to be "venv/")

```console
foo@bar:~$ make run
```

if you want to use rizthme on docker container you can use make script for this

```console
foo@bar:~$ make build docker-run
```

And to delete stop or restart him check Makefile possibilities