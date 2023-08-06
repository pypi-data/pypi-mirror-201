import os
from configparser import ConfigParser
import plumbum.cli


class ConfigureCli(plumbum.cli.Application):
    """
    Create a configuration file, storing commonly used information in a profile.
    """

    def main(self, *args):
        config = ConfigParser(default_section=None)

        profile = plumbum.cli.terminal.prompt('Profile:', type=str, default='default')
        api_url = plumbum.cli.terminal.prompt('API Url:', type=str, default='https://api.nearlyhuman.ai')
        api_key = plumbum.cli.terminal.prompt('API Key:', type=str, default='')

        config[profile] = {
            'api_url': api_url,
            'api_key': api_key
        }

        path = os.path.expanduser('~/.nearlyhuman/config')
        with open(path, 'w') as file:
            config.write(file)
