import argparse
import os
import re
import subprocess

'''
This works as an wrapper for starting the flask server. It uses the 
Unix like command-line options, use --help to see what it can do.
'''


def str2bool(arg):
    '''
    function(arg) -> bool
    This functions is a helper for argument parsing, return a bool
    if the paremeter is yes, y, true, t, or 1.
    '''
    if isinstance(arg, bool):
        return arg
    elif arg.lower() in ('yes', 'y', 'true', 't', '1'):
        return True
    elif arg.lower() in ('no', 'n', 'false', '0'):
        return False

def replace_run(options):
    with open('flaskr/app/run.py') as read:
        with open('flaskr/app/tmp', 'w') as write:
            for line in read:
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
                            tmp += options
                            written = True
                        else:
                            tmp += char
                write.write(line)
    os.remove('flaskr/app/run.py')
    os.rename('flaskr/app/tmp', 'flaskr/app/run.py')

def main():
    '''
    Wrapper's main function
    '''

    parser = argparse.ArgumentParser(
        description='Wrapper for flask server on Heroku, WARNING: PAST run.py CONFIGURATION WILL BE ERASED')
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help=
        '''The hostname to listen on. Set this to "0.0.0.0" to have the server available externally as well. Use "" for host'''
    )
    parser.add_argument(
        '--port',
        help=
        '''The port of the webserver. Defaults to 5000 or the port defined in the SERVER_NAME config variable if present. Use "" for port'''
    )
    parser.add_argument('--debug',
                        type=str2bool,
                        default=True,
                        help='If given, enable or disable debug mode.')
    parser.add_argument(
        '--load_dotenv',
        help=
        '''Load the nearest .env and .flaskenv files to set environment variables. Will also change the working directory to the directory containing the first file found.'''
    )
    parser.add_argument(
        '--options',
        nargs='*',
        help='''The options to be forwarded to the underlying Werkzeug server.
                        See werkzeug.serving.run_simple() for more information.'''
    )

    parser.add_argument(
        '--development',
        type=str2bool,
        default=False,
        help=
        '''Create a environment variable for port in case of local development that want to match with heroku's way to configure the server'''
    )

    argp = parser.parse_args()

    if argp.development:
        os.environ['PORT'] = '5000'
    del argp.development

    if argp.port is None:
        argp.port = os.environ['PORT']

    options = ''
    for arg in vars(argp):
        if getattr(argp, arg) is not None:
            if arg == 'host' or arg == 'port':
                options += '{}="{}", '.format(arg, getattr(argp, arg))
            else:
                options += '{}={}, '.format(arg, getattr(argp, arg))
    options = options[:-2]
    replace_run(options)

    with subprocess.Popen(['python', 'flaskr/app/run.py'], stdout=subprocess.PIPE) as process:
        process.communicate()

if __name__ == "__main__":
    main()
