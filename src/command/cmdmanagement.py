from command.echo import Echo
from command.cmd_func import _Cmd, _Docker
c = _Cmd
d = _Docker

command = {
    "done": c.done,
    "ps": c.ps,
    "echo": Echo,
    "docker ps": d.docker_ps,
}


def cmd_map(get, default=c.cmd_not_found):
    return command.get(get, default)

