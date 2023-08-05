<p align="center">
    <img src="https://www.nearlyhuman.ai/wp-content/uploads/2022/04/virtual-copy.svg" width="200"/>
</p>

# Cortex CLI
A simple CLI that abstracts the Cortex API.  The application should reflect all of the Cortex routes, and provide a way
to interact with models within an approved client.

## Prerequisites
- Mamba
- Create a github token with repo permissions and set the `GH_TOKEN` environment variable

## Build
```
mamba env create -f ./conda.yml

# Build version of Cortex CLI for release
python -m build
```

## Running the CLI
```
mamba activate cortex_cli
python ./cortex_cli/cortex.py [resource] [action] [parameters ...]
```

Resources include configure, clients, models, pipelines, and inferences.
Actions include get, list, and create.
Parameters are action+resource specific.

### Client
*NOTE*: the default client is `demo`.  This can be modified by passing in `-c CLENT_NAME` to all commands, or to set the ENV variable 'CLIENT' to the client key.

*Get a List of Clients*
```
$ python ../cortex-cli/cortex_cli/cortex.py clients list

[{'_id': '6317eceaeef27d972e86b4ff',
  'clientKey': 'demo',
  'createdDate': '2022-09-07T00:59:22.582Z',
  'description': 'The Cortex Demo Client',
  'experimentId': '1',
  'licensePlan': 'enterprise',
  'name': 'Demo',
  'supportEmail': 'karl.haviland@nearlyhuman.ai',
  'supportPhone': '717-111-2222',
  'updatedDate': '2022-09-07T00:59:22.582Z',
  'website': 'https://www.nearlhuman.ai'}]
```

*Get a Client by ID*
```
$ python ../cortex-cli/cortex_cli/cortex.py clients get -i 6317eceaeef27d972e86b4ff

{'_id': '6317eceaeef27d972e86b4ff',
 'clientKey': 'demo',
 'createdDate': '2022-09-07T00:59:22.582Z',
 'description': 'The Cortex Demo Client',
 'experimentId': '1',
 'licensePlan': 'enterprise',
 'name': 'Demo',
 'supportEmail': 'karl.haviland@nearlyhuman.ai',
 'supportPhone': '717-111-2222',
 'updatedDate': '2022-09-07T00:59:22.582Z',
 'website': 'https://www.nearlhuman.ai'}

```

### Models
*Get a List of Models*
```
$ python ../cortex-cli/cortex_cli/cortex.py models list

[{'_id': '632b32731d2faa4ffbade76d',
  'clientKey': 'demo',
  'createdDate': '2022-09-20T15:49:06.882Z',
  'description': 'A model that is initialized through the Cortex CLI.',
  'experimentId': '1',
  'name': 'nmci-chat-2',
  'organization': 'nearlyhuman',
  'repo': 'nmci-chat-2',
  'tags': [],
  'updatedDate': '2022-09-20T15:49:06.882Z'},
 {'_id': '632b43fd1d2faa4ffbade771',
  'clientKey': 'demo',
  'createdDate': '2022-09-21T17:03:57.365Z',
  'description': 'A model that is initialized through the Cortex CLI.',
  'experimentId': '1',
  'name': 'nmci-chat-3',
  'organization': 'nearlyhuman',
  'repo': 'nmci-chat-3',
  'tags': [],
  'updatedDate': '2022-09-21T17:03:57.365Z'},
 ...
 ]
```

*Get a Model By ID*
```
$ python ../cortex-cli/cortex_cli/cortex.py models get -i 632b32731d2faa4ffbade76d
{'_id': '632b32731d2faa4ffbade76d',
 'clientKey': 'demo',
 'createdDate': '2022-09-20T15:49:06.882Z',
 'description': 'A model that is initialized through the Cortex CLI.',
 'experimentId': '1',
 'name': 'nmci-chat-2',
 'organization': 'nearlyhuman',
 'repo': 'nmci-chat-2',
 'tags': [],
 'updatedDate': '2022-09-20T15:49:06.882Z'}
```

*Run a Model's Pipeline*
*NOTE:* First, cd to the model's local directory.  Use the `-t` flag to set tracking against the Cortex server.  Otherwise it will simply train locally.
```
~/workspaces/nh/demo-financialchat$ python ../cortex-cli/cortex_cli/cortex.py models run -t
   + Found the model nearlyhuman/demo-financialchat with id 632b6da8b015504a5d35b0f2
   + Initialized the MLFlow integration
   + Did not find existing pipeline for branch main with status Pending
   + Pipeline Pending with id 6331008ec84419b73954ad03
   + Pipeline Running with id 6331008ec84419b73954ad03
                Loading module base from ./src/financialchat/base.py
                Loading module financialchat from ./src/financialchat/financialchat.py
   + Loaded the Cortex Model into memory
   + Loaded data
   + Ran the fit
   + Completed the evaulation
/home/havkarl/anaconda3/envs/mlflow/lib/python3.8/site-packages/_distutils_hack/__init__.py:33: UserWarning: Setuptools is replacing distutils.
  warnings.warn("Setuptools is replacing distutils.")
   + Saved the model artifact
                Adding models/cortex/6331008ec84419b73954ad03 to artifacts
   + Logged the model artifact into Cortex
   + Pipeline Successful with id 6331008ec84419b73954ad03
   + Completed Cortex Pipeline Run
```

*Initialize a New Model*
*NOTE:* Only needed if you want to both create a brand new Cortex ready model and automatically register it with the server.  Start from the workspace directory where the model repo is going to be created locally.
```
$ python ../cortex-cli/cortex_cli/cortex.py models init -n demo-digits-predictions-karl
```

*Register a Model*
*NOTE:* Only needed if you have an existing Cortex Github repository and you want to register it with the server. First, cd to the model's local directory.
```
$ python ../cortex-cli/cortex_cli/cortex.py models register -n demo-digits-predictions-karl
```

### Pipelines
