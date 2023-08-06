from os.path import *

import argcomplete as argcomplete
from lgg import get_logger

from glob import glob

logger = get_logger('AI Manager CLI')
_HERE = dirname(__file__)


def cli():
    import subprocess
    import argparse

    parser = argparse.ArgumentParser(
        description='Python-based CLI to manage the Scailable AI Manager')

    parser.add_argument('actions',
                        help='Actions to take. They executed sequentially in the same order they are specified',
                        nargs='+',
                        choices=['install', 'update', 'start', 'stop', 'restart', 'test', 'delete', 'logs', 'local',
                                 'cache', 'settings'])
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    actions = args.actions

    for action in actions:
        logger.info(f'Current action is "{action}"')
        if action in ['install', 'update']:
            subprocess.run(['bash', f'{join(_HERE, "install.sh")}'])
        elif action in ['start', 'stop', 'restart']:
            subprocess.run(['bash', f'{join(_HERE, "others.sh")}', action])
        elif action == 'delete':
            subprocess.run(['bash', f'{join(_HERE, "delete.sh")}'])
        elif action == 'test':
            subprocess.run(['bash', f'{join(_HERE, "test.sh")}'])
        elif action == 'logs':
            subprocess.run(['cat', '/opt/sclbl/etc/logs'])
        elif action == 'cache':
            subprocess.run(['bash', f'{join(_HERE, "clear_cache.sh")}'])
        elif action == 'settings':
            subprocess.run(['bash', f'{join(_HERE, "settings.sh")}'])
        elif action == 'local':
            try:
                script_path = open(join(_HERE, 'sclbl_ai_manager_folder.txt'), 'r').readlines()
                logger.debug(f'Using cached path for "sclbl-edge-ai-manager" folder')
            except:
                script_path = glob(join('/home', '**', 'sclbl-edge-ai-manager', 'scripts', 'build_local_and_run.sh'),
                                   recursive=True)
            if not script_path:
                logger.error('The "sclbl-edge-ai-manager" folder does not exist!')
            else:
                script_path = script_path[0]
                logger.debug(f'The "sclbl-edge-ai-manager" folder is found at {script_path}')

                # save in a file
                with open(join(_HERE, 'sclbl_ai_manager_folder.txt'), 'w') as f:
                    f.write(script_path)

                # run
                subprocess.run(['bash', script_path])
