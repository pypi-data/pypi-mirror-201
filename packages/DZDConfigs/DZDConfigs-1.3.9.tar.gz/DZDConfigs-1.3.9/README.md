# Configs

Configs is a helper class to manage config and .env files over different environments,instances,test scenarios and so on

## Install

pip3 install DZDConfigs

### Dev

pip3 install git+https://git.connect.dzd-ev.de/dzdpythonmodules/configs.git

## How to use


| **tl;tr**: You can see a full working example in [Configs/smoketest](Configs/smoketest) |
| --- |
 
In short you will use Configs like this:

```python
from Configs import getConfig
config = getConfig()
print(config.MY_CONFIG_VALUE)
```

There are three possibilites to provide Configs with data.

* [In python code "config.py"](#1-a-configpy-file)
* [In one or more .env files](#2-env-files)
* [In Environment variables](#3-os-environment-variables)

In future version there will be yaml and json files supported as well

### 1 : A config.py file

Here you can register values that are controlling your business logic

./config.py:
```python
from Configs import ConfigBase

#define different classes per environment

class DEFAULT(ConfigBase):
    # Always create a DEFAULT class and use it as the base class for other environments classes

    # DEFAULT must have all config variables / class attributes that are used in the other classes
    MY_CONFIG_VALUE=1
    MY_CONFIG_VALUE_B=1

# All following config classes inherit from DEFAULT
class PRODUCTION(DEFAULT):
    MY_CONFIG_VALUE=2

class DEVELOPMENT(DEFAULT):
    MY_CONFIG_VALUE=2
```

### 2 : .env files

Here you can register values you dont want to have in a repo (like passwords) or describe connections to external systems (like database hostnames)

⚠ Environment variables need to have the prefix "**CONFIGS_**" in order to be parsed by Configs

./env/DEFAULT.env:
```
CONFIGS_MYDB_HOST='LOCALHOST'
```

./env/PRODUCTION.env:
```
CONFIGS_MYDB_HOST='THE_PROD_DBHOSTMACHINE.NETWORK.INTERNAL'
```

⚠ These values will be set as OS environment variable after the getConfig was called.

### 3 : OS environment variables

Similar like option 2 you can set OS environment variables that do not belong in your repo (like credentials, hostnames etc)

⚠ Environment variables need to have the prefix "**CONFIGS_**" in order to be parsed by Configs

This is convenient for use with docker (see https://docs.docker.com/compose/environment-variables/ and https://docs.docker.com/engine/reference/commandline/run/ see "--env , -e")

e.g.

`>>> docker run -e CONFIGS_APP_PATH="/mypath/isstrong" me/mypythonapp` 

Will populate the variable `APP_PATH` in your python code running in your container

```python
from Configs import getConfig
config = getConfig()
print(config.APP_PATH)
```

This will output `/mypath/isstrong`

## How to use the config instance

./main.py:
```python
import os
# For examples purposes we set an OS environment variables from python
os.environ["CONFIGS_ANOTHER_ENV_VAR"] = "ANOTHER_VALUE"

from Configs import getConfig

# get the config instance
config = getConfig()

# the config variables declared in the classes
print(config.MY_CONFIG_VALUE)
# a config variable from the .env-file vars
print(config.MYDB_HOST)
# a config value from the environment variable we set above
print(config.ANOTHER_ENV_VAR)
# prints: ANOTHER_VALUE
```

### Switch between configurations

To switch the environment set the envrionemt variable `ENV`. In this example we switch to `PRODUCTION`

**Docker**

`docker run -e ENV="PRODUCTION"`

**Linux**

`export ENV="PRODUCTION"`

**Windows**

`setx ENV="PRODUCTION"`

**Python**

For testing purposes you can switch the environemt also from python itself

```python
import os
os.environ["ENV"] = "PRODUCTION"
```

### Keep my envs out of the repo!

Register following pattern in your .gitignore file to prevent you hostnames and passwords landing in git repository

./gitignore:
```
[...]
.env
!*/env/DEFAULT.env
[...]
```

### ⚠️ What else to notice?

**Types**

Every variable in config.py can have more complex types like custom classes, functions, instances

.env files and environmet variables can only contain following types

* int
* string
* boolean
* json (which will be represent as python dicts)


**Who is overriding who**

What happens when multiple sources have the same variable name?

For example in your DEFAULT.env:
```
CONFIGS_MY_HAPPY_OVERRIDE="ENVFILEVAL"
```
and in your config.py is the same var

```
class DEFAULT(ConfigBase):
    MY_HAPPY_OVERRIDE = "CONFFILEVAL"
``` 

```python
from Configs import getConfig
config = getConfig()
print(config.MY_HAPPY_OVERRIDE)
```
This will output `ENVFILEVAL`

Env file values will always override config.py values.

And OS env values will override env file values

If you want env file vars to override allready existing system environment variables you can set the `getConfig()` parameter `env_file_vars_override_system_env_var` to `True`


```python
getConfig(env_file_vars_override_system_env_vars=True)
```

This is helpfull for testing purposes, when switching the environment on the fly (see [Configs/smoketest/main.py](Configs/smoketest/main.py))


## What is planned for the future

**Short term**

* Support yaml and json config files
* Support set, update variables from code
* Get meta data on variables (source, overwritten-by)

**Long term**

* Server-client architecure, making central configuration servers possible