import argparse
import logging
import re
import shlex
import shutil
import subprocess
import sys
import textwrap
from ievv_opensource.utils import ievv_colorize


try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

try:
    from termcolor import colored
except ImportError:
    def colored(text, *args, **kwargs):
        return text


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] %(message)s')
logging.getLogger('sh.command').setLevel(logging.WARNING)


def _find_management_commands():
    commands = []
    shellcommand = f"{shutil.which('python')} manage.py --help"
    try:
        output = subprocess.check_output(
            shellcommand,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
    except subprocess.CalledProcessError:
        pass
    else:
        for line in output.split():
            line = line.strip()
            if line.startswith('ievvtasks_'):
                commands.append(line[len('ievvtasks_'):])
    return commands


def _make_cli_epilog(commands):
    cli_help = """
    Available commands:
      {}
    """.format('\n      '.join(commands))
    return cli_help


class UnknownArgsParser(object):
    short_option_pattern = re.compile(
        '^-(?P<option>[a-zA-Z0-9][a-zA-Z0-9_-]*)=(?P<value>.+)$')
    long_option_pattern = re.compile(
        '^--(?P<option>[a-zA-Z0-9][a-zA-Z0-9_-]*)=(?P<value>.+)$')

    def __init__(self, unknown_args):
        self.unknown_args = unknown_args
        self.fixed_unknown_args = self.__parse()

    def __parse_argument(self, argument):
        long_option_match = self.long_option_pattern.match(argument)
        short_option_match = self.short_option_pattern.match(argument)
        if long_option_match:
            groupdict = long_option_match.groupdict()
            return '--{option}={value}'.format(
                option=groupdict['option'],
                value=cmd_quote(groupdict['value']),
            )
        elif short_option_match:
            groupdict = short_option_match.groupdict()
            return '-{option}={value}'.format(
                option=groupdict['option'],
                value=cmd_quote(groupdict['value']),
            )
        else:
            return cmd_quote(argument)

    def __parse(self):
        fixed_unknown_args = []
        for argument in self.unknown_args:
            fixed_unknown_args.append(self.__parse_argument(argument))
        return fixed_unknown_args

    def resultlist(self):
        return self.fixed_unknown_args

    def resultstring(self):
        return ' '.join(self.fixed_unknown_args)


def cli():
    commands = _find_management_commands()
    commands = list(set(commands))
    commands.sort()

    args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='IEVV command line interface.',
        epilog=textwrap.dedent(_make_cli_epilog(commands)),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Do not include help unless we just run ``ievv --help`` or ``ievv``.
        # If we do not use this, we can not add help for the sub commands.
        add_help=len(args) <= 1)
    parser.add_argument('command', type=str,
                        metavar='command',
                        help='The command to run. Use ``ievv <command> --help`` for '
                             'help with a specific command. The available commands '
                             'is listed in the "Available commands" section below.',
                        choices=commands)
    if len(args) == 0:
        parser.print_help()
    else:
        args, unknown_args = parser.parse_known_args()

        # if args.command == 'createproject':
        #     # parser = argparse.ArgumentParser(
        #     #     description='Initialize a new project')
        #     # parser.add_argument('command', type=str)
        #     # args = parser.parse_args(unknown_args)
        # else:
        parsed_unknown_args = UnknownArgsParser(unknown_args)

        args = [
            sys.executable,
            'manage.py',
            f'ievvtasks_{args.command}',
            *shlex.split(parsed_unknown_args.resultstring())
        ]
        pretty_command = shlex.join(args)
        try:
            process = subprocess.Popen(args)
            exitcode = process.wait()
        except KeyboardInterrupt:
            print(
                colored(f'[KeyboardInterrupt]({pretty_command}) stopped by user', color='yellow', attrs=['bold']),
                flush=True)
            raise SystemExit()
        else:
            color = 'green'
            status = 'DONE'
            if exitcode != 0:
                color = 'red'
                status = 'FAILED'
            print(
                colored(f'[{status}]({pretty_command}) with exitcode: {exitcode}', color=color, attrs=['bold']),
                flush=True)
            sys.exit(exitcode)
