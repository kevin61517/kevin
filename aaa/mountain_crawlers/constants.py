import os

PROXY_USER = ''
PROXY_PASSWORD = ''

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
def root(x): return os.path.join(basedir, x)
