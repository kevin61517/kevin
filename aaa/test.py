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
