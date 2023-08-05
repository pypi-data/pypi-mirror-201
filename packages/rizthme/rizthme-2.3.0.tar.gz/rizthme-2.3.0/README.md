# Rizthme

## Requierement

First step is to add in your environments variables,
a variables named "TOKEN" with in value, your discord application token.

do this with:

```console
foo@bar:~$ export TOKEN=<your token>
```

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
foo@bar:~$ python3 client.py
```

### Automatical script launching

#### For Linux user

For use automatically your virtual environment. (The virtual environment name need to be "venv/")

```console
foo@bar:~$ source entrypoint.sh
```

if you don't want to use a virtual environment. juste use the script like this:

```console
foo@bar:~$ bash entrypoint.sh
```
or 

```console
foo@bar:~$ sh entrypoint.sh
```

#### For Windows user

> Not sure yet

you can do like this if you realy want to use that in Windows system

```
C:RizThme\> entrypoint.bat
```
