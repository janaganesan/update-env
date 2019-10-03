# Update env setting

If you are looking to have your aliases, variables, commands across all Linux VMs then this is for you.

## Getting Started

This project uses your private key that can access the host without password. We use Pramaiko SSH client to verify the access and then use the Linux rsync utility to sync files.

### Prerequisites

Python 2.6 or higher

paramiko module

### Configuring

Create a config.json file at the root directory. To begin with you can copy config.sample included.

```
private-key-file: This will be the private key used for login and syncing files remotely.

hosts: This can either be a comma separated list of hosts or a file that contains list of hostnames. For now this can resolve only Glados hosts.

files: Contains the source and the destination to be synced
```

### Running

Simply run the python file below. You may wish to setup a cron that can sync your host(s) regularly.

```
python ssh-client.py
```

### Updating your environment

By default Linux PATH variable points to your *$HOME/bin*. While your commands are picked directly from this directory, for aliases and environment variables you may have to run the below command after logging into your destination VM.

```
update-env
```

What it does is it sources your aliases and variables from the below files

*$HOME/.myenv/aliases.sh*

*$HOME/.myenv/variables.sh*



