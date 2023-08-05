#! /usr/bin/env python
# Copyright 2016-2021 Cisco Systems, Inc
import os
import sys
import json
import itertools
from multiprocessing import Process
from six import string_types

from django.db.models.deletion import ProtectedError
from yangsuite import get_logger
from ysyangtree.ymodels import (
    YSYangModels,
    DEFAULT_INCLUDED_NODETYPES,
    ALL_NODETYPES
)
from ysyangtree.context import YSContext
from ysyangtree.models import YangSetTree, YangSetJSON
from ysfilemanager import merge_user_set, YSYangSet

log = get_logger(__name__)


class TreeUserError(Exception):
    pass


class TreeCacheError(Exception):
    pass


class TreeContextError(Exception):
    pass


class YangSetError(Exception):
    pass


class BackwardCompatibleYSmodel:
    """TODO: Major design flaw. When multiple modules are loaded
    the "nodeid" is contiuned for each model instead of starting
    at 1 and loading a different tree in the UI.  Just one main
    tree and each module is a branch instead of having a different
    tree for each module.
    """
    def __init__(self, models):
        self.nodeid = itertools.count(0)
        self.jstree = models

    @property
    def jstree(self):
        return self._jstree

    @jstree.setter
    def jstree(self, trees):
        if len(trees.get('data', [])) > 1:
            if 'id' not in trees['data'][0]:
                raise TreeCacheError('No ID for root node.')
            rootid = trees['data'][0]['id']
            for tree in trees['data'][1:]:
                # IDs are not in sequence between trees
                if tree.get('id') == rootid:
                    self._fixup_ids(trees)
                    break
        self._jstree = trees

    def _fixup_tree_ids(self, tree, cnt=0):
        tree['id'] = next(cnt)
        if 'children' in tree:
            for ch in tree.get('children'):
                self._fixup_tree_ids(ch, cnt)

    def _fixup_ids(self, trees):
        for tree in trees['data']:
            self._fixup_tree_ids(tree, self.nodeid)


def generate_key(owner, setname, module, ref, plugin, nodes='default'):
    """Common function to get key to database entry."""
    ntype = 'default'
    if nodes == ALL_NODETYPES:
        ntype = 'all'

    for i in [owner, setname, module, ref, plugin, ntype]:
        if not isinstance(i, string_types):
            raise TypeError('{0} must be str type'.format(str(i)))

    return owner+'-'+setname+'-'+module+'-'+ref+'-'+plugin+'-'+ntype


def get_one_yangset_tree(owner, setname, module, ref='',
                         plugin_name='yangsuite-yangtree',
                         nodes=DEFAULT_INCLUDED_NODETYPES):
    """Fetch yangset JsTree from cache.
    Args:
        owner (str): User name
        setname (str): Name of YANGSet
        modules (str): A module to be included in the Yang Set Tree
        ref (str): Reference
        plugin_name (str): Name of plugin

    Returns:
        dict: JsTree dictionary.
    """
    tree = {}
    supported_tree = {}
    key = generate_key(owner, setname, module, ref, plugin_name, nodes)
    try:
        tree = YangSetTree.objects.filter(key=key).get().tree
        support = YangSetTree.objects.filter(key=key).get().supports
        if support:
            supported_tree = YangSetTree.objects.filter(key=support).get().tree
    except Exception as exc:
        log.info('Failed to retreive tree "{0}": {1}'.format(key, str(exc)))
        return (None, None)
    try:
        tree = json.loads(tree.data)
    except Exception as exc:
        log.error('Entry has invalid tree: "{0}" {1}'.format(key, str(exc)))
        clear_tree_entry(key)
        return (None, None)
    try:
        if supported_tree:
            supported_tree = json.loads(supported_tree.data)
    except Exception as exc:
        log.error('Supported tree invalid: "{0}" {1}'.format(key, str(exc)))
        clear_tree_entry(support)
        return (None, None)
    return (tree, supported_tree)


def get_yangset_tree(owner, setname, modules, ref='',
                     plugin_name='yangsuite-yangtree',
                     nodes=DEFAULT_INCLUDED_NODETYPES):
    """Fetch yangset JsTree from cache.
    Args:
        owner (str): User name
        setname (str): Name of YANGSet
        modules (str): A module to be included in the Yang Set Tree
        ref (str): Reference
        plugin_name (str): Name of plugin

    Returns:
        dict: JsTree dictionary.
    """
    models = None
    try:
        ys = YSYangSet.load(owner, setname)
    except FileNotFoundError:
        raise YangSetError('No such yangset')

    if not ys.is_stale:
        trees = {'data': []}
        for mod in modules:
            tree, supported_tree = get_one_yangset_tree(
                owner, setname, mod, ref, plugin_name, nodes
            )
            if not tree:
                break
            else:
                trees['data'].append(tree)
                if supported_tree:
                    trees['data'].append(supported_tree)
        else:
            models = BackwardCompatibleYSmodel(trees)

    return models


def clear_tree_entry(key):
    """Clear out tree entry and tree from database.

    Args:
      key (str): Key to database entry
    """
    tree_entry = tree = None
    try:
        tree_entry = YangSetTree.objects.filter(key=key)
    except Exception as exc:
        log.error('Failed to get tree entry: "{0}".'.format(
            str(exc)
        ))
        return
    if not tree_entry:
        log.error(
            'Trying to remove tree entry "{0}" that does not exist.'.format(
                key
            )
        )
        return
    try:
        tree = YangSetTree.objects.get(key=key).tree
    except Exception as exc:
        log.error('Failed to get tree from entry: "{0}".'.format(
            str(exc)
        ))
        tree = None
    try:
        tree_entry.delete()
        log.info('Removed tree entry "{0}".'.format(key))
    except Exception as exc:
        log.error(
            'Failed to delete tree entry "{0}": {1}'.format(
                key, str(exc)
            )
        )
        return
    if not tree:
        log.error(
            'Tree entry does not have tree data "{0}"'.format(
                key,
            )
        )
        return
    try:
        tree.delete()
    except ProtectedError:
        log.info('Tree reference removed "{0}"'.format(key))
        return
    except Exception as exc:
        log.error(
            'Failed to delete tree "{0}": {1}'.format(
                key, str(exc)
            )
        )
        return

    log.info('Removed tree referenced by "{0}".'.format(key))


def remove_yangset_tree(owner, setname, module, ref='',
                        plugin_name='yangsuite-yangtree',
                        nodes=DEFAULT_INCLUDED_NODETYPES):
    """Remove yangset JsTree from the cache.

    Args:
        owner (str): User name
        setname (str): Name of YANGSet
        modules (list): A list of modules to be included
                            in the Yang Set Tree
        ref (str): Reference
        plugin_name (str): Name of plugin

    Returns:
        dict: JsTree dictionary.
    """
    key = generate_key(owner, setname, module, ref, plugin_name, nodes)
    clear_tree_entry(key)


def save_tree_to_database(ys, data):
    """Save a single JStree to database

    Args:
      ys (yangset.YSYangSet): YANG set object.
      data (dict): Tree data and key.
    """
    if ys.is_stale:
        # Remove stale entry from database
        clear_tree_entry(data['key'])
    # Add tree to database
    treedata = json.dumps(data['tree'])
    ysjson = YangSetJSON(data=treedata)
    ysjson.save()
    mod_key = data.get('key')
    support_key = data.get('supports')
    if support_key:
        # Add link to supported tree and support module info
        ysettree = YangSetTree(
            key=mod_key, supports=support_key, tree=ysjson
        )
        ysettree.save()
    else:
        ysettree = YangSetTree(
            key=mod_key, tree=ysjson
        )
        ysettree.save()


def create_tree_process(owner, setname, modules, repo,
                        ref='',
                        nodes=DEFAULT_INCLUDED_NODETYPES,
                        plugin_name='yangsuite-yangtree',
                        node_callback=None,
                        child_class=None,
                        queue=None):
    """Create tree in separate process for quick release of memory.

    Args:
        owner (str): User name
        setname(str): Name of setname
        modules (dict): A dictionary of modules
        repo(str): User repository
        ref (str): Reference
        nodes (frozenset): Nodes included in tree
        plugin_name (str): Name of plugin
        node_callback (function): Function to call for each node in the tree
            in order to populate additional data into the tree. Must accept
            kwargs ``stmt``, ``node``, and ``parent_data``
            (which may be ``None``), and return ``node``.
        child_class (Object): Custom pyang parser.
        queue (str): JSON file name for temporary storage.
    """
    if modules and queue:
        # Need valid cache entries
        try:
            log.info('Creating new tree for {0}'.format(
                ', '.join([n for n in modules])
            ))
            # YSContext memory gets released after this process ends.
            ctx = YSContext.get_instance(ref, merge_user_set(
                owner, setname
            ))
        except RuntimeError:
            raise TreeUserError("No such user")
        except KeyError:
            raise TreeCacheError('Bad cache reference')
        if ctx is None:
            raise TreeContextError("User context not found")
        models = YSYangModels(ctx, modules, child_class=child_class,
                              included_nodetypes=nodes,
                              node_callback=node_callback)
        supports = {}
        main = {}
        for modtree in models.jstree['data']:
            mod = modtree['text']
            key = generate_key(
                owner, setname, mod, ref, plugin_name, nodes
            )
            if 'children' not in modtree:
                supports[mod] = {'tree': modtree, 'key': key, 'supports': ''}
            else:
                main[mod] = {'tree': modtree, 'key': key}

        for mod, data in supports.items():
            info = data['tree'].get('data')
            if info:
                includes = info.get('belongs-to', [])
                includes += info.get('imports', [])
                for inc in includes:
                    if inc in main:
                        supports[mod]['supports'] = main[inc]['key']

        supports.update(main)
        main = supports

        with open(queue, 'w') as fd:
            json.dump(main, fd)


def create_yangset_tree(owner, setname, modules, repo,
                        ref='',
                        nodes=DEFAULT_INCLUDED_NODETYPES,
                        plugin_name='yangsuite-yangtree',
                        node_callback=None,
                        child_class=None):
    """Retreive or create a YANG set JsTree.

    Calling this API directly allows caller to create a custom JsTree
    according to the plugin needs using node_callback and child_class.
    This allows plugin to take advantage of builtin caching and storage.

    Args:
        owner (str): User name
        setname(str): Name of setname
        modules (dict): A dictionary of modules
        repo(str): User repository
        ref (str): Reference
        nodes (frozenset): Nodes included in tree
        plugin_name (str): Name of plugin
        node_callback (function): Function to call for each node in the tree
            in order to populate additional data into the tree. Must accept
            kwargs ``stmt``, ``node``, and ``parent_data``
            (which may be ``None``), and return ``node``.
        child_class (Object): Custom class with knowledge of pyang structures
            and capable of creating a custom JStree.
    Returns:
        BackwardCompatibleYSmodel: Created database tree for UI
    """
    models = None
    trees = {'data': []}
    build_modules = []

    try:
        ys = YSYangSet.load(owner, setname)
    except FileNotFoundError:
        raise YangSetError('No such yangset')

    if not ys.is_stale:
        for mod in modules:
            tree, supported_tree = get_one_yangset_tree(
                owner, setname, mod, ref, plugin_name, nodes
            )
            if not tree:
                build_modules.append(mod)
            else:
                trees['data'].append(tree)
                if supported_tree:
                    trees['data'].append(supported_tree)
    else:
        build_modules = modules

    if build_modules:
        queue = '-'.join(modules)+'.json'

        p = Process(
            target=create_tree_process,
            args=(
                owner,
                setname,
                build_modules,
                repo,
                ref,
                nodes,
                plugin_name,
                node_callback,
                child_class,
                queue
            )
        )
        p.start()
        p.join()
        if not os.path.isfile(queue):
            if sys.version_info[1] > 7 and 'Clang' in sys.version:
                # TODO: need to switch to subprocess
                log.error('MAC Python 3.8 cannot build tree in process')
            elif sys.platform == "win32":
                log.error('Windows Python 3.8 cannot build tree in process')
                log.error('Should use Windows Linux Subsystem')
            create_tree_process(
                owner,
                setname,
                build_modules,
                repo,
                ref,
                nodes,
                plugin_name,
                node_callback,
                child_class,
                queue
            )
        if os.path.isfile(queue):
            treedata = json.load(open(queue))
            os.remove(queue)
            for mod, data in treedata.items():
                # Add tree with module info to return
                trees['data'].append(data['tree'])
                save_tree_to_database(ys, data)
            models = BackwardCompatibleYSmodel(trees)
    else:
        models = BackwardCompatibleYSmodel(trees)
    return models
