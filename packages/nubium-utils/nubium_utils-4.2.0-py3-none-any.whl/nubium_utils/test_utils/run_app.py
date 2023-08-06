import pty
import select
import subprocess
from multiprocessing import Process
from pathlib import Path
from typing import List
from unittest.mock import patch

from dotenv import load_dotenv
import os


def venv_path():
    return Path(os.environ.get("DUDE_APP_VENV", "./venv"))


def run_command_in_virtual_environment(command: str = "", args: List[str] = None):
    if not args:
        args = []
    run_command_in_pseudo_tty(command=str(venv_path() / "bin" / command), args=args)


def run_command_in_pseudo_tty(
        command: str,
        args: List[str] = None,
        output_handler=lambda data: print(data.decode("utf-8"), end=""),
        buffer_limit=512,
        buffer_timeout_seconds=0.04,
):
    # In order to get colored output from a command, the process is unfortunately quite involved.
    # Constructing a pseudo terminal interface is necessary to fake most commands into thinking they are in an environment that supports colored output
    if not args:
        args = []

    # It's possible to handle stderr separately by adding p.stderr.fileno() to the rlist in select(), and setting stderr=subproccess.PIPE
    # which would enable directing stderr to click.echo(err=True)
    # probably not worth the additional headache
    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen([command] + args, stdin=slave_fd, stdout=slave_fd, stderr=subprocess.STDOUT, close_fds=True)

    def is_proc_still_alive():
        return proc.poll() is not None

    while True:
        ready, _, _ = select.select([master_fd], [], [], buffer_timeout_seconds)
        if ready:
            data = os.read(master_fd, buffer_limit)
            output_handler(data)
        elif is_proc_still_alive():  # select timeout
            assert not select.select([master_fd], [], [], 0)[0]  # detect race condition
            break  # proc exited
    os.close(slave_fd)  # can't do it sooner: it leads to errno.EIO error
    os.close(master_fd)
    proc.wait()


def run_app(runtime_env_overrides=None):
    load_dotenv(Path(f'{os.path.abspath(venv_path())}/.env'), override=True)
    process = Process(target=run_command_in_virtual_environment, args=("python3.8", ['app.py']))
    if not runtime_env_overrides:
        runtime_env_overrides = {}
    with patch.dict('os.environ', runtime_env_overrides):
        process.start()
    return process.pid
