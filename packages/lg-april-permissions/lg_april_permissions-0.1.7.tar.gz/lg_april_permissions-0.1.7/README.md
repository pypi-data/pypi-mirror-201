# buditool
Das Tool dient hauptsächlich zum synchronisieren von Berechtigungen: es schaut in die Postgres-DB (April_Permissions) und schickt API calls an Budibase, um die Berechtigungen zu setzten. Bitte auch die KNOWN ISSUES in tests/bb_test.py lesen!

### Features 
```bash
kmille@linbox:lg-april-permissions ~/.local/bin/buditool -h
usage: buditool [-h] [-u USER] [--list-apps] [--list-users] [-a ADD_PERMISSIONS] [-r REMOVE_PERMISSIONS] [-s] [-c CONFIG] [--version]

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  show user (needs bb user id)
  --list-apps           list all bb apps
  --list-users          list all bb users
  -a ADD_PERMISSIONS, --add-permissions ADD_PERMISSIONS
                        add permissions for user (needs bb user id)
  -r REMOVE_PERMISSIONS, --remove-permissions REMOVE_PERMISSIONS
                        remove permissions for user (needs bb user id)
  -s, --sync            synchronize permissions with db
  -c CONFIG, --config CONFIG
                        config file
  --version             show version
```

### Configuration (settings.yaml.template)
```yaml
---
bb_base_api_url: "https://bb-test.itsnow.biz/api/public/v1/"
bb_api_key: ""
permissions:
  "app_dev_908c8e8aad04477183ee858c3c29f0d5": "BASIC" # Protestbuffet
db_connection: "dbname=aa user=aa host=127.0.0.1 password= port=10002"
```


### Run tests
```bash
kmille@linbox:lg-april-permissions poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: lg-april-permissions (0.1.0)
kmille@linbox:lg-april-permissions poetry run pytest  -x -v -s
============================================================================================================= test session starts =============================================================================================================
platform linux -- Python 3.10.10, pytest-7.2.2, pluggy-1.0.0 -- /home/kmille/.cache/pypoetry/virtualenvs/lg-april-permissions-bzz6vhyK-py3.10/bin/python
cachedir: .pytest_cache
rootdir: /home/kmille/projects/letzte-generation/lg-april-permissions
collected 1 item

tests/bb_test.py::TestAPI::test_roles {}
{}
{'app_908c8e8aad04477183ee858c3c29f0d5': 'BASIC'}
{}
{'app_908c8e8aad04477183ee858c3c29f0d5': 'BASIC'}
{'app_908c8e8aad04477183ee858c3c29f0d5': 'POWER'}
{}
PASSED

============================================================================================================== 1 passed in 3.25s ==============================================================================================================
kmille@linbox:lg-april-permissions
```

### Build and installation
```bash
kmille@linbox:lg-april-permissions poetry build
Building lg-april-permissions (0.1.0)
  - Building sdist
  - Built lg_april_permissions-0.1.0.tar.gz
  - Building wheel
  - Built lg_april_permissions-0.1.0-py3-none-any.whl
kmille@linbox:lg-april-permissions pip install --user dist/lg_april_permissions-0.1.0-py3-none-any.whl
Processing ./dist/lg_april_permissions-0.1.0-py3-none-any.whl
Requirement already satisfied: pyyaml<7.0,>=6.0 in /usr/lib/python3.10/site-packages (from lg-april-permissions==0.1.0) (6.0)
Requirement already satisfied: requests<3.0.0,>=2.28.2 in /home/kmille/.local/lib/python3.10/site-packages (from lg-april-permissions==0.1.0) (2.28.2)
Collecting psycopg2-binary<3.0.0,>=2.9.6
  Downloading psycopg2_binary-2.9.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 7.4 MB/s eta 0:00:00
Requirement already satisfied: charset-normalizer<4,>=2 in /home/kmille/.local/lib/python3.10/site-packages (from requests<3.0.0,>=2.28.2->lg-april-permissions==0.1.0) (3.1.0)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /home/kmille/.local/lib/python3.10/site-packages (from requests<3.0.0,>=2.28.2->lg-april-permissions==0.1.0) (1.26.15)
Requirement already satisfied: idna<4,>=2.5 in /home/kmille/.local/lib/python3.10/site-packages (from requests<3.0.0,>=2.28.2->lg-april-permissions==0.1.0) (3.4)
Requirement already satisfied: certifi>=2017.4.17 in /home/kmille/.local/lib/python3.10/site-packages (from requests<3.0.0,>=2.28.2->lg-april-permissions==0.1.0) (2022.12.7)
Installing collected packages: psycopg2-binary, lg-april-permissions
  WARNING: The script buditool is installed in '/home/kmille/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed lg-april-permissions-0.1.0 psycopg2-binary-2.9.6
```


### Walkthrough
```bash
kmille@linbox:lg-april-permissions ~/.local/bin/buditool -u us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
{
    "data": {
        "_id": "us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6",
        "email": "abc@mail.com",
        "status": "active",
        "firstName": "Hans",
        "lastName": "Nani",
        "forceResetPassword": false,
        "roles": {
            "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC"
        }
    }
}


kmille@linbox:lg-april-permissions ~/.local/bin/buditool --sync
Syncing permissions with database
Processing Bikö 159
 Budibase user id: us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6 (Hansi Nani)
Adding permissions for user us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
Rollen vorher:
{
    "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC"
}
Rollen danach:
{
    "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC",
    "app_908c8e8aad04477183ee858c3c29f0d5": "BASIC"
}


kmille@linbox:lg-april-permissions ~/.local/bin/buditool -u us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
{
    "data": {
        "_id": "us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6",
        "email": "abc@mail.com",
        "status": "active",
        "firstName": "Hans",
        "lastName": "Nani",
        "forceResetPassword": false,
        "roles": {
            "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC",
            "app_908c8e8aad04477183ee858c3c29f0d5": "BASIC"
        }
    }
}
kmille@linbox:lg-april-permissions ~/.local/bin/buditool -r us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
Removing permissions for user us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
Rollen vorher:
{
    "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC",
    "app_908c8e8aad04477183ee858c3c29f0d5": "BASIC"
}
Rollen danach:
{
    "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC"
}
kmille@linbox:lg-april-permissions ~/.local/bin/buditool -u us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6
{
    "data": {
        "_id": "us_ee81b34c-f7ea-4bbd-8faf-d8a83889dff6",
        "email": "abc@mail.com",
        "status": "active",
        "firstName": "Hans",
        "lastName": "Nani",
        "forceResetPassword": false,
        "roles": {
            "app_7c5f5f30d8254721bc04e2c98249f31c": "BASIC"
        }
    }
}
```
