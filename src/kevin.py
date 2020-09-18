import sys
import subprocess
import types, socket
from collections import deque, __loader__
import decimal
import random

PUSH = 'git push'
PULL = 'git pull'


def fantasy_soccer():
    print("=== STARTING PULL FANTASY_SOCCER ===")
    subprocess.Popen(f'cd ~/fantasy_soccer_api ; {PULL} ;'
                     f' cd ~/fantasy_soccer_api/src/fantasy_common ;{PULL}', shell=True)
    print("=== DONE ===")


def fantasy_admin():
    print("=== STARTING PULL FANTASY_ADMIN ===")
    # git -C 路徑 pull = 去到路徑下進行 git pull
    subprocess.Popen('git -C ~/fantasy_admin_api/ pull ;'
                     ' git -C ~/fantasy_admin_api/src/fantasy_common/ pull', shell=True)
    print("=== DONE ===")


def fantasy_service():
    print("=== STARTING PULL FANTASY_SERVICE ===")
    # git -C 路徑 pull = 去到路徑下進行 git pull
    subprocess.Popen('git -C ~/fantasy_service/ pull ;'
                     ' git -C ~/fantasy_service/src/fantasy_common/ pull', shell=True)
    print("=== DONE ===")

#
# if __name__ == '__main__':
#     fantasy_soccer()
#     fantasy_admin()
#     fantasy_service()
