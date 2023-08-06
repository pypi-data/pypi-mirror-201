# pysch - Python-made SSH Connection Manager

`pysch` (spelled in Russian as пыщ, just for fun), **Py**thon-made **S**SH **C**onnection **H**elper, is an SSH Client based on [paramiko](https://github.com/paramiko/paramiko) for Mac and Linux. It uses keepass to securely store remote hosts credentials and YAML to maintain inventory tree. It also supports session logging to a file.

## Installation 
Just use `pip` to install `pysch`: 
```
python -m venv venv
cd venv
source bin/activate
pip3 install pysch
```

## Usage
Here is the avaiable commands:
```
(venv) % pysch
Usage: pysch [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config PATH               Path to configuration file
  -l, --loglevel [CRITICAL|ERROR|WARNING|INFO|DEBUG]
  --help                          Show this message and exit.

Commands:
  add-credentials   Add new credendials
  connect           Connect to the host
  init              Create initial config and inventoty
  list-credentials  Get list of credendials
  list-hosts        Get list of hosts
  ```

First, init the configuration. That creates sample configuration and inventory files with empty keepass file protected with key in `~/.config/pysch/` directory:
  ```
  (venv) % pysch init
  Default configuration has been saved at ~/.config/pysch/
  ```
Then add your hosts to the `~/.config/pysch/inventory.yaml` using the text editor of your choise and credentials for it using any keepass software or the `add-credentials` command:
```
(venv) % pysch add-credentials  
Title: my_credentials
Username: root      
Password: 
Repeat for confirmation: 
"my_credentials" entry has been added to the keepass db
```
Use `--help` to show arguments and available options for a command:
```
(venv) % pysch connect --help
Usage: pysch connect [OPTIONS] HOST

  Connect to the host

Options:
  --session-log PATH  Session log file location
  --help              Show this message and exit.
```
Connection process is pretty simple:
```
(venv) % pysch connect srv
Connecting to srv
root@my-shiny-server.example.com:~# 
```
