# from flask import Flask
# from flask.helpers import find_package
import decimal
import os
import sys
import pkgutil
import uuid
from datetime import datetime, timedelta


def _matching_loader_thinks_module_is_package(loader, mod_name):
    """Given the loader that loaded a module and the module this function
    attempts to figure out if the given module is actually a package.
    """
    # If the loader can tell us if something is a package, we can
    # directly ask the loader.
    if hasattr(loader, 'is_package'):
        return loader.is_package(mod_name)
    # importlib's namespace loaders do not have this functionality but
    # all the modules it loads are packages, so we can take advantage of
    # this information.
    elif (loader.__class__.__module__ == '_frozen_importlib' and
          loader.__class__.__name__ == 'NamespaceLoader'):
        return True
    # Otherwise we need to fail with an error that explains what went
    # wrong.
    raise AttributeError(
        ('%s.is_package() method is missing but is required by Flask of '
         'PEP 302 import hooks.  If you do not use import hooks and '
         'you encounter this error please file a bug against Flask.') %
        loader.__class__.__name__)


def _find_package_path(root_mod_name):
    """Find the path where the module's root exists in"""
    if sys.version_info >= (3, 4):
        import importlib.util

        try:
            spec = importlib.util.find_spec(root_mod_name)
            if spec is None:
                raise ValueError("not found")
        # ImportError: the machinery told us it does not exist
        # ValueError:
        #    - the module name was invalid
        #    - the module name is __main__
        #    - *we* raised `ValueError` due to `spec` being `None`
        except (ImportError, ValueError):
            pass  # handled below
        else:
            # namespace package
            if spec.origin in {"namespace", None}:
                return os.path.dirname(next(iter(spec.submodule_search_locations)))
            # a package (with __init__.py)
            elif spec.submodule_search_locations:
                return os.path.dirname(os.path.dirname(spec.origin))
            # just a normal module
            else:
                return os.path.dirname(spec.origin)

    # we were unable to find the `package_path` using PEP 451 loaders
    loader = pkgutil.get_loader(root_mod_name)
    if loader is None or root_mod_name == '__main__':
        # import name is not found, or interactive/main module
        return os.getcwd()
    else:
        # For .egg, zipimporter does not have get_filename until Python 2.7.
        if hasattr(loader, 'get_filename'):
            filename = loader.get_filename(root_mod_name)
        elif hasattr(loader, 'archive'):
            # zipimporter's loader.archive points to the .egg or .zip
            # archive filename is dropped in call to dirname below.
            filename = loader.archive
        else:
            # At least one loader is missing both get_filename and archive:
            # Google App Engine's HardenedModulesHook
            #
            # Fall back to imports.
            __import__(root_mod_name)
            filename = sys.modules[root_mod_name].__file__
        package_path = os.path.abspath(os.path.dirname(filename))

        # In case the root module is a package we need to chop of the
        # rightmost part.  This needs to go through a helper function
        # because of python 3.3 namespace packages.
        if _matching_loader_thinks_module_is_package(loader, root_mod_name):
            package_path = os.path.dirname(package_path)

    return package_path


def find_package(import_name):
    """Finds a package and returns the prefix (or None if the package is
    not installed) as well as the folder that contains the package or
    module as a tuple.  The package path returned is the module that would
    have to be added to the pythonpath in order to make it possible to
    import the module.  The prefix is the path below which a UNIX like
    folder structure exists (lib, share etc.).
    """
    root_mod_name, _, _ = import_name.partition('.')
    package_path = _find_package_path(root_mod_name)
    site_parent, site_folder = os.path.split(package_path)
    py_prefix = os.path.abspath(sys.prefix)
    if package_path.startswith(py_prefix):
        return py_prefix, package_path
    elif site_folder.lower() == 'site-packages':
        parent, folder = os.path.split(site_parent)
        # Windows like installations
        if folder.lower() == 'lib':
            base_dir = parent
        # UNIX like installations
        elif os.path.basename(parent).lower() == 'lib':
            base_dir = os.path.dirname(parent)
        else:
            base_dir = site_parent
        return base_dir, package_path
    return None, package_path


class C:
    def __init__(self):
        self.name = 'kevin'

    def __get__(self, instance, owner):
        print(instance, owner)
        return '__get__'

    def __getattr__(self, item):
        return '__getattr__'

    # def __getattribute__(self, item):
    #     return '__getattribute__'


def decorate(callback):
    def _mid(func):
        def _in(*args, **kws):  # -> 任意船餐
            print('=== before ===')
            result = callback(func(*args, **kws))  # -> aaa
            print('=== after ===')
            return result
        return _in
    return _mid


def aaa():
    print('== AAA ==')
    return 0


def iteritems(x):
    return iter(x.items())


aaa2 = decorate(callback='Jojo')(aaa)


if __name__ == '__main__':
    d = {'name': 'kevin', 'number': 123, 'class': 'A'}
    for i in iteritems(d):
        print(i)
    dd = {'name': ''}
    print('>>>', dd.get('name', 'kevin'))
    count = 10
    per_page = 3
    pages = count // per_page
    pages += 1 if count % per_page else 0
    print(pages)


a = {
    'success': True,
    'message': 'SUCCESS',
    'data':
        [
            {
                'id': '796117028644585534',
                'userId': '87870',
                'merchantId': '1596048917620125698',
                'merchantUserId': '1596048917620125698yl82944',
                'currency': 1,
                'exchangeRate': '1',
                'seriesType': 0,
                'betType': '1x1*1',
                'allUp': 1,
                'allUpAlive': 1,
                'stakeAmount': '50',
                'settleAmount': '0',
                'orderStatus': 4,
                'payStatus': 1,
                'oddsChange': 1,
                'device': 'pc',
                'ip': '18.166.200.86',
                'createTime': '1670488220011',
                'modifyTime': '1670488225255',
                'maxWinAmount': '210',
                'loseAmount': '260',
                'rollBackCount': 0,
                'itemCount': 1,
                'seriesValue': 1,
                'betNum': 1,
                'unitStake': '50',
                'betList': [
                    {
                        'id': '796117028644585790',
                        'orderId': '796117028644585534',
                        'sportId': 13,
                        'matchId': '617165',
                        'matchName': '意大利 vs. 韩国',
                        'period': 13002,
                        'marketId': '1829742',
                        'marketType': 13003,
                        'optionType': 5,
                        'optionName': '小 39.5',
                        'marketName': '总分大小-第一局',
                        'tournamentId': '15686',
                        'tournamentName': '世界女排联赛',
                        'odds': '5.2',
                        'oddsFormat': 1,
                        'betOdds': '5.20',
                        'settleStatus': 3,
                        'isInplay': True,
                        'p1': 39.5,
                        'betScore': 'SET: 1-0',
                        'matchType': 2,
                        'matchTime': '1668157920000'
                    }
                ],
                'maxStake': '230',
                'validSettleStakeAmount': '0',
                'validSettleAmount': '0',
                'cashOutCancelStake': '0',
                'walletType': 1,
                'version': 4
            }
        ],
    'code': 0
}

b = [
    {
        'id': '796145633126776894',
        'userId': '87870',
        'merchantId': '1596048917620125698',
        'merchantUserId': '1596048917620125698yl82944',
        'currency': 1,
        'exchangeRate': '1',
        'seriesType': 0,
        'betType': '1x1*1',
        'allUp': 1,
        'allUpAlive': 1,
        'stakeAmount': '10',
        'settleAmount': '0',
        'orderStatus': 4,
        'payStatus': 1,
        'oddsChange': 1,
        'device': 'pc',
        'ip': '18.166.200.86',
        'createTime': '1670491550962',
        'modifyTime': '1670491551470',
        'maxWinAmount': '6.4',
        'loseAmount': '16.4',
        'rollBackCount': 0,
        'itemCount': 1,
        'seriesValue': 1,
        'betNum': 1,
        'unitStake': '10',
        'betList': [
            {
                'id': '796145633126777150',
                'orderId': '796145633126776894',
                'sportId': 1,
                'matchId': '719355',
                'matchName': '帕尔马 vs. 贝内文托',
                'period': 1001,
                'marketId': '2752857',
                'marketType': 1005,
                'optionType': 1,
                'optionName': '帕尔马',
                'marketName': '独赢',
                'tournamentId': '11006',
                'tournamentName': '意大利乙级联赛',
                'odds': '1.64',
                'oddsFormat': 1,
                'betOdds': '1.64',
                'settleStatus': 3,
                'isInplay': False,
                'matchType': 2,
                'matchTime': '1670499000000'
            }
        ],
        'maxStake': '10000',
        'validSettleStakeAmount': '0',
        'validSettleAmount': '0',
        'cashOutCancelStake': '0',
        'walletType': 1, 'version': 4
    },
    {
        'id': '796145701846253630',
        'userId': '87870',
        'merchantId': '1596048917620125698',
        'merchantUserId': '1596048917620125698yl82944',
        'currency': 1,
        'exchangeRate': '1',
        'seriesType': 0,
        'betType': '1x1*1',
        'allUp': 1,
        'allUpAlive': 1,
        'stakeAmount': '20',
        'settleAmount': '0',
        'orderStatus': 4,
        'payStatus': 1,
        'oddsChange': 1,
        'device': 'pc',
        'ip': '18.166.200.86',
        'createTime': '1670491558726',
        'modifyTime': '1670491559334',
        'maxWinAmount': '54.2',
        'loseAmount': '74.2',
        'rollBackCount': 0,
        'itemCount': 1,
        'seriesValue': 1,
        'betNum': 1,
        'unitStake': '20',
        'betList': [
            {
                'id': '796145701846253886',
                'orderId': '796145701846253630',
                'sportId': 1,
                'matchId': '719355',
                'matchName': '帕尔马 vs. 贝内文托',
                'period': 1001,
                'marketId': '2752857',
                'marketType': 1005,
                'optionType': 2,
                'optionName': '贝内文托',
                'marketName': '独赢',
                'tournamentId': '11006',
                'tournamentName': '意大利乙级联赛',
                'odds': '3.71',
                'oddsFormat': 1,
                'betOdds': '3.71',
                'settleStatus': 3,
                'isInplay': False,
                'matchType': 2,
                'matchTime': '1670499000000'
            }
        ],
        'maxStake': '3600',
        'validSettleStakeAmount': '0',
        'validSettleAmount': '0',
        'cashOutCancelStake': '0',
        'walletType': 1,
        'version': 4
    },
    {
        'id': '796145797073731646',
        'userId': '87870',
        'merchantId': '1596048917620125698',
        'merchantUserId': '1596048917620125698yl82944',
        'currency': 1,
        'exchangeRate': '1',
        'seriesType': 0,
        'betType': '1x1*1',
        'allUp': 1,
        'allUpAlive': 1,
        'stakeAmount': '15',
        'settleAmount': '0',
        'orderStatus': 4,
        'payStatus': 1,
        'oddsChange': 1,
        'device': 'pc',
        'ip': '18.166.200.86',
        'createTime': '1670491569350',
        'modifyTime': '1670491569776',
        'maxWinAmount': '27.6',
        'loseAmount': '42.6',
        'rollBackCount': 0,
        'itemCount': 1,
        'seriesValue': 1,
        'betNum': 1,
        'unitStake': '15',
        'betList': [
            {
                'id': '796145797073731902',
                'orderId': '796145797073731646',
                'sportId': 1,
                'matchId': '719256',
                'matchName': '科森扎 vs. 布雷西亚',
                'period': 1001,
                'marketId': '2753353',
                'marketType': 1005,
                'optionType': 1,
                'optionName': '科森扎',
                'marketName': '独赢',
                'tournamentId': '11006',
                'tournamentName': '意大利乙级联赛',
                'odds': '2.84',
                'oddsFormat': 1,
                'betOdds': '2.84',
                'settleStatus': 3,
                'isInplay': False,
                'matchType': 2,
                'matchTime': '1670508000000'
            }
        ],
        'maxStake': '5400',
        'validSettleStakeAmount': '0',
        'validSettleAmount': '0',
        'cashOutCancelStake': '0',
        'walletType': 1,
        'version': 4
    },
    {
        'id': '796146054771769406', 'userId': '87870', 'merchantId': '1596048917620125698', 'merchantUserId': '1596048917620125698yl82944', 'currency': 1, 'exchangeRate': '1', 'seriesType': 0, 'betType': '1x1*1', 'allUp': 1, 'allUpAlive': 1, 'stakeAmount': '25', 'settleAmount': '0', 'orderStatus': 4, 'payStatus': 1, 'oddsChange': 1, 'device': 'pc', 'ip': '18.166.200.86', 'createTime': '1670491599061', 'modifyTime': '1670491609419', 'maxWinAmount': '44.75', 'loseAmount': '69.75', 'rollBackCount': 0, 'itemCount': 1, 'seriesValue': 1, 'betNum': 1, 'unitStake': '25', 'betList': [{'id': '796146054771769662', 'orderId': '796146054771769406', 'sportId': 1, 'matchId': '618206', 'matchName': '突尼斯 vs. 澳大利亚', 'period': 1001, 'marketId': '2473667', 'marketType': 1005, 'optionType': 3, 'optionName': '和', 'marketName': '独赢', 'tournamentId': '10583', 'tournamentName': '*卡塔尔世界杯', 'odds': '2.79', 'oddsFormat': 1, 'betOdds': '2.79', 'settleStatus': 3, 'isInplay': False, 'matchType': 2, 'matchTime': '1669456800000'}], 'maxStake': '5500', 'validSettleStakeAmount': '0', 'validSettleAmount': '0', 'cashOutCancelStake': '0', 'walletType': 1, 'version': 4}
]
