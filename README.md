# borg_interface

This application provides an interface to borg backup. At a later point it might 
as well work with restic.

### Installation
To install the application either "git clone" it in the folder you want with:

```
git clone https://git.2li.ch/Nebucatnetzer/borg_interface.git
```

or simply download it and extract the zip to your prefered location.:
* https://git.2li.ch/Nebucatnetzer/borg_interface/archive/master.zip

### Starting
Before starting the application make sure that you have configured it properly.
See the section [Configuration](https://git.2li.ch/Nebucatnetzer/borg_interface#configuration) for more details.
To start the application simply execute the borg_interface file.
You will then see a list of options which are fairly self explanatory.

### Configuration
To configure borg_interface please edit the borg_interface.cfg file.
All the options have to be placed under the [DEFAULT] section.
The proper syntax is:

```
option: value
```

or

```
option=value
```

Possible values as of now are:

##### server
define a server on which the archive reside.

##### user
defines the user which has permission to connect to the server.

##### repository_path
defines the path where the repository is set up.
This is needed for both a remote and a local repository.

##### password
defines the repository password

### Example Config
```
[DEFAULT]
server: testserver.local
user: borg
repository_path: /home/borg/backup/repository
password: foo
```
