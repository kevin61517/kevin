import subprocess


class _Cmd:
    @staticmethod
    def cmd_not_found(): print("command not found")

    @staticmethod
    def done(): print("=== server close ===")

    @staticmethod
    def ps(): return subprocess.Popen("ps", shell=True)


class _Docker:
    @staticmethod
    def docker_ps():
        return subprocess.Popen("docker ps", shell=True)


def _(): ...