from cookiecutter.main import cookiecutter
import plumbum.cli
from plumbum import local
import requests
from collections import ChainMap, namedtuple
import cortex_cli.cli.api.github_api as gh

import conda_pack
import traceback
import os
import os.path
import mlflow
import yaml
import sys
import os, shutil
import importlib
from datetime import datetime
from mlflow.models.signature import infer_signature
from os import walk

from cortex_cli.cli.cli_api_base import CliApiBase

import cortex_cli.core.mlflow.mlflow_cortex as mlflow_cortex
from cortex_cli.core.ethics_checks import EthicsResult
from cortex_cli.core.drift_checks import DriftResult


class ModelsCli(plumbum.cli.Application):
    NAME = 'models'


@ModelsCli.subcommand('init')
class InitModel(CliApiBase):
    ML_MODEL_TEMPLATE_PATH = 'ml_model_template'


    _name = plumbum.cli.SwitchAttr(
        names=['-n', '--name'],
        argtype=str,
        help='The name of the model. Should use a readable format, ie. Digits Model',
        default=None
    )

    _repo = plumbum.cli.SwitchAttr(
        names=['-r', '--repo'],
        argtype=str,
        help='The name of the repository. Should use dash case, ie. digits-model',
        mandatory=True
    )

    _description = plumbum.cli.SwitchAttr(
        names=['-d', '--description'],
        argtype=str,
        default='A model that is initialized through the Cortex CLI.',
        help='A description of the model'
    )

    _token = plumbum.cli.SwitchAttr(
        names=['--github-token'],
        argtype=str,
        envname='GH_TOKEN'
    )

    _org = plumbum.cli.SwitchAttr(
        names=['--github-org'],
        argtype=str,
        envname='GH_ORG',
        default='nearlyhuman',
    )

    _path = plumbum.cli.SwitchAttr(
        names=['-p', '--path'],
        argtype=str,
        envname='MODEL_PATH',
        default='.',
    )

    _register = plumbum.cli.Flag(
        names=["--register"]
    )

    # Properties

    @property
    def _template_location(self):
        current = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(os.path.dirname(current), self.ML_MODEL_TEMPLATE_PATH)

    @property
    def _model_path(self):
        return os.path.join(self._path, self._repo)


    def main(self, *args):
        self._error_message = None

        # Instantiate the model name if it hasn't been set.
        if not self._name:
            self._name = self._repo.replace('-', ' ').title()

        github = gh.Github(
            self._repo,
            self._description,
            # TODO: Need to separate out this organization because the GH account can be from anywhere.
            self._org,
            self._token
        )

        try:
            self._validate_repo()
            self._generate_template_repo()

            # If the user has specified a GH token, then we can create the repo in github and automatically register with Cortex.
            if self._token:
                self._create_repo(github)

                if self._register:
                    self._register_model()
        except Exception as e:
            self._fail(e)
            self._error_message = e
        finally:
            if not self._error_message:
                self._pass(f'Successfully generated the model repository at "{self._model_path}"')
        return


    def _validate_repo(self):
        if os.path.exists(self._model_path):
            raise Exception(f'The directory "{self._model_path}" already exists. Either rename the directory or register the repository directly.')


    def _generate_template_repo(self):
        cookiecutter(
            self._template_location,
            no_input=True,
            output_dir=self._path,
            extra_context={
                'model_name':  self._name,
                'description': self._description
            }
        )


    def _create_repo(self, github):
        # create the repository in github
        response = self._handle_api_response(gh.create_repo(github))

        # commit and push to the new repo in github
        repo = gh.Repo(path=self._model_path)
        repo.init() \
            .set_remote(github.owner, github.repo_name) \
            .add() \
            .commit('Initial commit. Generated from Cortex CLI using the model template.') \
            .push()

        self._pass(
            f'Created the GitHub repository "{self._org}/{self._repo}"')
        return response


    def _register_model(self, model_name: str):
        if self._register:
            response = requests.post(
                url=self.endpoint,
                headers=self.headers,
                json={
                    'name': model_name,
                    'repo': model_name
                }
            )
            self._handle_api_response(
                response, f'Registered the model repository {response["_id"]}')
        else:
            self._fail(
                'Skipping Cortex registration. Please register the repository with Cortex before training in the cloud')


@ModelsCli.subcommand('register')
class RegisterModel(CliApiBase):
    _repo = plumbum.cli.SwitchAttr(
        names=['-r', '--repo'],
        argtype=str,
        mandatory=True
    )

    _name = plumbum.cli.SwitchAttr(
        names=['-n', '--name'],
        argtype=str,
        mandatory=True
    )


    def main(self, *args):
        try:
            response = self._register_model()
            self._print(response)
        except Exception as e:
            self._fail(e)


    def _register_model(self):
        return self._handle_api_response(requests.post(
            url=self._endpoint,
            headers=self._headers,
            json={
                'name': self._name,
                'repo': self._repo
            }
        ))


@ModelsCli.subcommand('run')
class RunModelPipeline(CliApiBase):
    _path = plumbum.cli.SwitchAttr(
        names=['-p', '--path'],
        argtype=str,
        envname='MODEL_PATH',
        default='.',
    )

    _tracking = plumbum.cli.Flag(
        names=['-t', '--tracking']
    )

    # Properties

    @property
    def _model_id(self):
        return self._model_json['_id'] if self._model_json else None

    @property
    def _pipeline_id(self):
        return self._pipeline_json['_id'] if self._pipeline_json else None

    modules = {}
    @property
    def _modules(self):
        if self.modules:
            return self.modules
        for (root, dir_names, file_names) in walk(self._config['module_path']):
            file_names[:] = [
                f for f in file_names 
                if f.endswith('.py') and f not in ['__init__.py', '{}.py'.format(self._config['model_module'])] 
            ]
            # TODO: Set map of file path locations to module name
            for f in file_names:
                self.modules['{}/{}'.format(root, f)] = f.replace('.py', '')
        return self.modules

    @property
    def _model_module(self):
        return '{}/{}.py'.format(self._config['module_path'], self._config['model_module'])
    
    @property
    def _model_dir(self):
        return self._config['module_path']
    
    @property
    def _artifacts_dir(self):
        location = 'cortex' if self._tracking else 'local'
        id = self._pipeline_id if self._tracking and self._pipeline_id else self._now
        return f'models/{location}/{id}'
    
    @property
    def _pipeline_steps(self):
        Step = namedtuple('Step', 'name type')
        return [Step(dict[list(dict.keys())[0]], list(dict.keys())[0]) for dict in self._config['pipeline_steps']]

    _now = datetime.now().strftime('%m%d%Y-%H%M%S')

    @property
    def _config(self):
        return self._read_yaml('cortex.yml')

    # Helpers

    def _load_module(self, module_path, module_name):
        print('\t\tLoading module {} from {}'.format(module_name, module_path))
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


    def _read_yaml(self, file: str) -> dict:
        if not os.path.exists(file):
            self._fail(f'Error! No "{file}" found in this Model project.')

        with open(file, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

# -------------------------------------------------------------------------------

    def main(self, *args):
        # Change to working directory
        os.chdir(self._path)

        model = None
        self._error_message = None
        self._success = False
        self._model_json = None
        self._pipeline_json = None
        try:
            self._model_json = self._get_model()
            # Step 1 - Get live model data
            if self._tracking:
                self._mlflow_client = self._setup_mlflow()
                self._setup_pipeline()

            # Step 2 - Load the Model Class
            model = self._instantiate_model(self._config)

            # Step 3 - Initialize the pipeline steps
            self._initialize_steps()

            # Step 4 - Run the pipeline
            if self._tracking:
                self._pipeline_json = self._run_pipeline()

            # Step 5 - Run the pipeline steps
            self._run_pipeline_steps(model)

            # Step 6 - Save the pipeline artifacts
            self._save_pipeline(model)

            # Step 7 - Save the conda environment
            # if self._tracking:
            self._save_environment()

            # Step 8 - Upload the pipeline artifacts
            if self._tracking:
                self._upload_pipeline()
        except Exception as e:
            if not self._error_message:
                self._error_message = traceback.format_exc()
        finally:
            # Step 9 - Contact callback route to update currentStage of model pipeline
            if self._tracking and self._pipeline_json and self._model_json:
                status = 'Failed' if self._error_message or not self._success else 'Successful'
                self._complete_callback(
                    status,
                    self._error_message
                )

            if self._error_message:
                self._fail(self._error_message)
            else:
                self._pass('Completed Cortex Pipeline Run')

# -------------------------------------------------------------------------------

    def _initialize_steps(self):
        # Convert yaml steps to ml-api format
        _steps = []
        for step in self._pipeline_steps:
            _steps.append({
                'name':   step.name,
                'type':   step.type,
                'config': {}
            })
        
        if self._tracking:
            # Set cortex steps
            self._steps = self._create_steps(_steps)
        else:
            # Set normal steps
            self._steps = _steps

        self._pass('Loaded pipeline steps')


    def _create_steps(self, _steps):
        response = requests.post(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/steps',
            headers=self._headers,
            json={
                'stepsConfig': _steps
            }
        ).json()

        if len(response) == 0:
            raise Exception('Error! Failed to load the pipeline steps.')
        
        return response


    def _complete_step(self, step, step_status, step_result, step_risk):
        json_value = None

        # Setup json value depending on if we have risk or not
        json_value = {
            'pipelineId':    step['pipelineId'],
            'name':          step['name'],
            'type':          step['type'],
            'order':         step['order'],
            'status':        step_status,
            'statusMessage': '' if step_result is None else str(step_result)
        }

        if step_risk != '':
            json_value['risk'] = step_risk

        return requests.put(
            url=f'{self._api_url}/steps/{step["_id"]}/complete',
            headers=self._headers,
            json=json_value
        ).json()


    def _get_drift_inferences(self):
        response = requests.get(
            url=f'{self._api_url}/inferences?modelId={self._model_id}&hasTags[]=Drift Detection',
            headers=self._headers
        ).json()

        inferences = []
        if response and len(response['documents']) > 0:
            for inference in response['documents']:
                if inference['successful']:
                    inferences.append((inference['_id'], [inference['inputs']['ndarray'][0]], [inference['outputs']['ndarray'][0]]))

        return inferences

# -------------------------------------------------------------------------------

    def _get_pipeline(self, git_branch, model_id):
        query = {
            'gitBranch': git_branch,
            'local':     False
        }

        response = requests.get(
            url=f'{self._api_url}/pipelines',
            params=query,
            headers=self._headers,
            json={'modelId': model_id}
        )

        # This is definitely wrong and it's weird how we check here
        # We should probably just catch a 404 and handle it?
        pipeline = response.json()['documents']
        if len(pipeline) == 1:
            message = f'Found existing pipeline {pipeline["_id"]} for branch {git_branch} with status {pipeline["currentStage"]}.'

            if pipeline['currentStage'] == 'Running':
                raise Exception(
                    f'{message} The cloud initiated training needs to complete first on this branch before running again.')

            if pipeline['currentStage'] == 'Pending':
                self._pass(message)
                return pipeline

        self._pass(f'Did not find existing pipeline for branch {git_branch}')
        return None


    def _create_pipeline(self, model_id, git_branch, git_hash):
        response = requests.post(
            url=f'{self._api_url}/pipelines',
            headers=self._headers,
            json={
                'modelId':   model_id,
                'gitBranch': git_branch,
                'gitHash':   git_hash,
                'local':     True
            }
        ).json()
        
        return response


    def _run_pipeline(self):
        return requests.put(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/run',
            headers=self._headers,
            json={
                'modelId': self._model_id
            }
        ).json()


    def _run_pipeline_steps(self, model):
        current_step = None
        try:
            for step in self._steps:
                current_step = step['type']
                step_func = getattr(model, current_step)
                step_result = None

                # Handle special case for passing testing inferences to test_predict function
                if current_step == 'detect_drift':
                    step_result = step_func(self._get_drift_inferences())
                else:
                    step_result = step_func()

                if self._tracking:
                    step_risk = ''

                    # Get ethics check results (if it exists)
                    if type(step_result) is EthicsResult:
                        # Parse out risk level
                        step_risk = step_result.risk.value

                        # Parse out result
                        step_result = step_result.result_str
                    elif type(step_result) is DriftResult:
                        # Parse out result
                        step_result = step_result.result_str

                    self._complete_step(step, 'Successful',
                                        step_result, step_risk)
                self._pass(
                    f'{step["name"]} completed successfully')
            self._success = True
        except Exception as e:
            if self._tracking:
                self._complete_step(step, 'Failed', str(e), '')
            self._error_message = f'{step["name"]} completed with an error.\n{traceback.format_exc()}'
            raise Exception


    def _setup_pipeline(self):
        # Get the local branch
        git_branch = gh.Repo().branch
        git_hash = gh.Repo().hash

        if git_hash is None or git_hash is '':
            self._fail('Could not get git commit hash. Please initialize the git repository and commit your code before running the pipeline.')

        # Look for an existing 'Pending' pipeline for this branch
        pipeline_response = self._get_pipeline(
            git_branch,
            self._model_id
        )

        if pipeline_response:
            self._pipeline_json = self._handle_api_response(pipeline_response)
            return

        # If not found, create the locally sourced pipeline
        self._pipeline_json = self._create_pipeline(
            self._model_id,
            git_branch,
            git_hash
        )

        self._pass(f'Pipeline {self._pipeline_json["currentStage"]} with id: {self._pipeline_id}')

# -------------------------------------------------------------------------------

    def _get_model(self):
        query = {
            'repo': gh.Repo().repo
        }

        response = requests.get(
            url=self._endpoint,
            params=query,
            headers=self._headers
        )

        model = response.json()['documents']

        if response.status_code != 200 or len(model) != 1:
            raise Exception('Error! This model could not be found')

        self._pass(
            f'Found the model {gh.Repo().repo}')

        return model[0]


    def _complete_callback(self, status, error_message=None):
        body = {
            'modelId':      self._model_id,
            'currentStage': status,
        }

        if error_message:
            body['message']: error_message

        requests.put(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/run/complete',
            headers=self._headers,
            json=body
        )


    def _save_pipeline(self, model):
        self._info('Saving pipeline artifacts...')
        # TODO: How to generalize this infer signature call
        signature = infer_signature(model.input_example, model.output_example)

        # Save model
        modules = list(self._modules.keys())
        modules.append(self._model_module)
        if model.model_type == 'cortex':
            mlflow_cortex.save_model(
                python_model=model, 
                path=self._artifacts_dir,                   # Where artifacts are stored locally
                code_path=list(modules),                    # Local code paths not on
                conda_env='conda.yml',
                artifacts={},
                custom_objects=model.custom_objects,
                signature=signature
            )
        else:
            self._error_message = f"An error occurred while detecting the Cortex model type. \
            Found '{model.model_type}', but only ['cortex'] are acceptable values"
            raise Exception

        self._pass(f'Saved the pipeline artifacts to disk: ({self._artifacts_dir})')


    def _save_environment(self):
        self._info('Packing conda environment...')

        conda_pack.pack(
            output=f'{self._artifacts_dir}/environment.tar.gz',
            force=True,
            verbose=True,
            ignore_editable_packages=False,
            ignore_missing_files=True)

        self._pass(f'Packed conda environment to disk: ({self._artifacts_dir})')


    def _upload_pipeline(self):
        self._info('Uploading pipeline artifacts to Cortex...')

        file_names = []
        file_paths = []

        # Get files from pipeline run
        for root, dirs, files in os.walk(self._artifacts_dir):
            for file in files:
                file_names.append(file)
                file_paths.append(os.path.join(root, file))

        body = {
            'fileNames': file_names
        }
        
        # Obtain individual file upload urls
        upload_urls = requests.post(
            f'{self._api_url}/pipelines/{self._pipeline_id}/files/upload',
            headers=self._headers,
            json=body
        ).json()

        # Upload each file individually
        for i in range(len(file_names)):
            with open(file_paths[i], 'rb') as f:
                requests.put(
                    upload_urls[i],
                    data=f
                )
        
        self._pass(f'Uploaded the pipeline artifacts to Cortex')


    def _instantiate_model(self, config):
        # LOAD DEPENDENCY MODULES (except model)
        for path, module in self._modules.items():
            self._load_module(path, module)

        # LOAD MODEL MODULE
        model_module = self._load_module(
            '{}/{}.py'.format(config['module_path'], config['model_module']),
            config['model_module']
        )

        # return getattr(model_module, config['model_class'])(config['params'], 'demo', gh.Repo())
        model_params = ChainMap(config['params']) if config['params'] else {}
        return getattr(model_module, config['model_class'])(model_params, self._model_id, self._api_url, self._headers)


    def _setup_mlflow(self):
        # Create a client to make API calls to the tracking server
        return mlflow.tracking.MlflowClient()
