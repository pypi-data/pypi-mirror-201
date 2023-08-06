import os
import shlex
import shutil
import subprocess
import sys
import typing


def _parse_command_kwargs(**kwargs):
    args = []
    for key, value in kwargs.items():
        if len(key) == 1:
            argkey = f'-{key}'
        else:
            argkey = f'--{key.replace("_", "-")}'
        if value not in (False, None):
            args.append(argkey)
            if value != True:
                args.append(f'{value}')
    return args


def _default_out_handler(line):
    print(line, flush=True)


def _default_failure_output_checker(line):
    return False


def prettyformat_popen_kwargs(popen_kwargs: dict):
    kwargs = {**popen_kwargs}
    args = kwargs.pop('args')
    command = shlex.join(args)
    return f'{command}  ({kwargs!r})'


class RunExecutableError(Exception):
    def __init__(self, popen_kwargs: dict, failed_lines: typing.Optional[list] = None):
        self.popen_kwargs = popen_kwargs
        self.failed_lines = failed_lines
        message = f'FAILED TO EXECUTE: {prettyformat_popen_kwargs(self.popen_kwargs)}'
        if self.failed_lines:
            message = f'{message} (lines failed error checker: {self.failed_lines!r})'
        super().__init__(message)


def run_executable(
        executable: str,
        args: typing.Optional[list] = None,
        kwargs: typing.Optional[dict] = None,
        env: typing.Optional[dict] = None,
        cwd: typing.Optional[str] = None,
        output_handler = _default_out_handler,
        failure_output_checker = None,
        background:bool = False):
    """
    Run executable.

    This is made to make transitioning from https://amoffat.github.io/sh/ easier,
    so the kwargs are fairly compatible.
    """
    failure_output_checker = failure_output_checker or _default_failure_output_checker
    args = args or []
    kwargs = kwargs or {}
    full_args = [
        shutil.which(executable),
        *args,
        *_parse_command_kwargs(**kwargs)
    ]
    popen_kwargs = {
        'args': full_args,
        'shell': False,
        'env': env,
        'cwd': cwd
    }
    if background:
        process = subprocess.Popen(**popen_kwargs)
        return process
    else:
        popen_kwargs.update({
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
        })
        process = subprocess.Popen(**popen_kwargs)
        failure_checker_matched_lines = []
        while True:
            if process.poll() is not None:
                break
            output_line = process.stdout.readline().decode(sys.getfilesystemencoding(), 'replace').rstrip()
            if failure_output_checker(output_line):
                failure_checker_matched_lines.append(output_line)
            output_handler(output_line)
        returncode = process.poll()
        if returncode != 0:
            raise RunExecutableError(popen_kwargs=popen_kwargs)
        elif failure_checker_matched_lines:
            raise RunExecutableError(popen_kwargs=popen_kwargs)
        else:
            print(f'SUCCESS: {prettyformat_popen_kwargs(popen_kwargs)}')
