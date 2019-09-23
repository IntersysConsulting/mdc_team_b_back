import argparse
import os
import re
import subprocess
import sys

import yaml


'''
This works as an wrapper for starting the flask server. It uses the 
Unix like command-line options, use --help to see what it can do.
'''


def extract_yaml_config(path):
    config = None
    with open(path) as filed:
        try:
            config = yaml.safe_load(filed)
        except yaml.YAMLError as err:
            print(err)
            sys.exit(-1)
    return config


def replace_run(args, filed):
    with open(filed, 'r') as read:
        text = read.readlines()
    with open(filed, 'w') as write:
        for line in text:
            if re.search('app.run', line):
                tmp = ''
                written = False
                for char in line:
                    if written:
                        tmp += ')'
                        line = tmp
                        break
                    if char is '(':
                        tmp += '('
                        tmp += args
                        written = True
                    else:
                        tmp += char
            write.write(line)


def main():
    parser = argparse.ArgumentParser(
        description=
        'Configuration script intent to work for flask. It uses a YAML as configuration file'
    )
    parser.add_argument('--modify',
                        action='store_true',
                        help='Enable the start server file')
    parser.add_argument(
        '--file',
        default='config.yaml',
        help=
        'With --modify option it will specify the file to modify. Default is config.yaml'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Start the server. Takes the file from the run.py')

    argp = parser.parse_args()
    parsed = extract_yaml_config(argp.file)

    tags = {
        'host': 'host',
        'port': 'port',
        'debug': 'debug',
        'dotenv': 'load_dotenv',
        'sslcontext': 'ssl_context'
    }

    config = ''
    startfile = ''
    for element in parsed['server'].items():
        if element[0] == 'startfile':
            startfile = element[1]
            continue

        if element[1] is not None:
            if element[0] == 'debug':
                if element[1].lower() == 'y' or element[0].lower() == 'yes':
                    config += '{}={}, '.format(tags[element[0]], 'True')
                    continue
                else:
                    config += '{}={}, '.format(tags[element[0]], 'False')
                    continue

            if element[0] == 'host' or element[0] == 'load_dotenv' or element[
                    0] == 'ssl_context':
                if element[1] is None:
                    continue
                config += '{}="{}", '.format(tags[element[0]], element[1])
            else:
                config += '{}={}, '.format(tags[element[0]], element[1])
    config = config[:-2]

    if argp.modify:
        replace_run(config, startfile)

    if argp.execute:
        with subprocess.Popen(['python', startfile]) as process:
            process.communicate()


if __name__ == "__main__":
    main()
