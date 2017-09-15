#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import itertools
import os
import re

import pip
import pip.req
from setuptools import find_packages, setup

try:
    import pypandoc
except ImportError:
    pypandoc = None


def main():
    """Run setup"""
    metadata = get_package_metadata()

    # Run setup
    setup(**metadata)


def get_entrypoints(metadata, top_path=None):
    project = metadata['name']
    repo_path = top_path or os.path.realpath(os.path.dirname(__file__))
    permutations = ['__main__.py']
    pattern = '^def (?P<name>[^_]\w+)\('
    entry_points = {}
    for root, folders, files in os.walk(repo_path):
        folders[:] = [_ for _ in folders if not _.startswith('.')]
        files[:] = [_ for _ in files if _ in permutations]
        for filename in files:
            filepath = os.path.join(root, filename)
            base = os.path.splitext(filename)[0]
            with open(filepath, 'r') as stream:
                for line in stream:
                    matched = re.match(pattern, line)
                    if matched:
                        func = matched.groupdict()['name']
                        cli_name = func if func != 'main' else project
                        entry_point = '{cli_name}={project}.{base}:{func}'.format(
                            cli_name=cli_name,
                            func=func,
                            project=project,
                            base=base,
                        )
                        entry_points.setdefault('console_scripts', set()).add(entry_point)
    for ep, vals in entry_points.items():
        entry_points[ep] = list(vals)
    return entry_points


def get_license(top_path=None):
    path = top_path or os.path.realpath(os.path.dirname(__file__))
    files = {f.lower(): f for f in os.listdir(path)}
    permutations = itertools.product(['license'], ['', '.txt'])
    files = [os.path.join(path, f) for l, f in files.items() if l in permutations]
    license = ''
    for filepath in files:
        with open(filepath, 'r') as stream:
            license = stream.read()
            break
    return license


def get_readme(top_path=None):
    """Read the readme for the repo"""
    path = top_path or os.path.realpath(os.path.dirname(__file__))
    files = {f.lower(): f for f in os.listdir(path)}
    permutations = itertools.product(['readme'], ['.md', '.rst', '.txt'])
    files = [os.path.join(path, f) for l, f in files.items() if l in permutations]
    readme = ''
    for filepath in files:
        if pypandoc and filepath.endswith('.md'):
            readme = pypandoc.convert(filepath, 'rst')
            break
        else:
            with open(filepath, 'r') as stream:
                readme = stream.read()
                break
    return readme


def get_package_metadata(top_path=None):
    """Find the __metadata__.py file and read it"""
    repo_path = top_path or os.path.realpath(os.path.dirname(__file__))
    metadata = {}
    for root, folders, files in os.walk(repo_path):
        folders[:] = [_ for _ in folders if not _.startswith('.')]
        files[:] = [_ for _ in files if _ == '__metadata__.py']
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as stream:
                exec(stream.read(), globals(), metadata)
                metadata = metadata.get('package_metadata') or metadata
                break
        if metadata:
            break

    requirements, dependency_links = get_package_requirements(top_path=top_path)

    # Package Properties
    metadata.setdefault('long_description', metadata.get('doc') or get_readme())
    metadata.setdefault('packages', find_packages())
    metadata.setdefault('include_package_data', True)

    # Requirements
    metadata.setdefault('setup_requires', requirements.get('setup') or [])
    metadata.setdefault('install_requires', requirements.get('install') or [])
    metadata.setdefault('tests_require', requirements.get('tests') or requirements.get('test') or [])
    metadata.setdefault('extras_require', requirements.get('extras') or [])
    metadata.setdefault('dependency_links', dependency_links)

    # CLI
    entry_points = get_entrypoints(metadata=metadata, top_path=top_path) or {}
    metadata.setdefault('entry_points', entry_points)

    # Packaging
    metadata.setdefault('platforms', ['any'])
    metadata.setdefault('zip_safe', False)

    year = datetime.datetime.now().year
    license = get_license() or 'Copyright {year} - all rights reserved'.format(year=year)
    metadata.setdefault('license', license)
    return metadata


def get_package_requirements(top_path=None):
    """Find all of the requirements*.txt files and parse them"""
    repo_path = top_path or os.path.realpath(os.path.dirname(__file__))
    requirements = {'extras': {}}
    install_reqs = []
    dependency_links = set()
    max_depth = 1
    for root, folders, files in os.walk(repo_path):
        depth = root[len(repo_path) + len(os.path.sep):].count(os.path.sep)
        if depth > max_depth:
            folders[:] = []
        folders[:] = [_ for _ in folders if _ == 'requirements']
        for filename in files:
            filepath = os.path.join(root, filename)

            # match on:
            #    requirements.txt
            #    requirements-<name>.txt
            #    requirements_<name>.txt
            #    requirements/<name>.txt
            pattern = '.*requirements([-_/](?P<name>.*))?.txt$'
            matched = re.match(pattern, filepath)
            if not matched:
                continue

            name = matched.groupdict().get('name') or ''
            reqs_, deps = parse_requirements(filepath)
            # TODO: Fix install_reqs so it is processed first and
            #       makes this filter meaningful.  Right now this
            #       filter will only work if a requirements.txt file
            #       is present because it is processed first implicitly.
            #       If requirements/install.txt is used instead, then
            #       This logic fails.
            reqs_ = [_ for _ in reqs_ if _ not in install_reqs]
            dependency_links.update(deps)
            # either requirements.txt or requirements/install.txt but
            #  not both
            if (not name or name == 'install') and not install_reqs:
                requirements['install'] = reqs_
                install_reqs = reqs_
            elif name in ['tests', 'test']:
                requirements['tests'] = reqs_
                requirements['extras']['tests'] = reqs_
            elif name in ['setup']:
                requirements['setup'] = reqs_
            else:
                requirements['extras'][name] = reqs_

    all_reqs = set()
    dev_reqs = set()
    for name, req_list in requirements.items():
        if name in ['install']:
            all_reqs.update(req_list)
        elif name in ['extras']:
            for subname, reqs in req_list.items():
                all_reqs.update(reqs)
                dev_reqs.update(reqs)
        else:
            all_reqs.update(req_list)
            dev_reqs.update(req_list)

    requirements['extras']['dev'] = list(sorted(dev_reqs))
    requirements['extras']['all'] = list(sorted(all_reqs))
    return requirements, list(sorted(dependency_links))


def get_readme(top_path=None):
    """Read the readme for the repo"""
    path = top_path or os.path.realpath(os.path.dirname(__file__))
    files = {f.lower(): f for f in os.listdir(path)}
    permutations = itertools.product(['readme'], ['.md', '.rst', '.txt'])
    files = [os.path.join(path, f) for l, f in files.items() if l in permutations]
    readme = ''
    for filepath in files:
        if pypandoc and filepath.endswith('.md'):
            readme = pypandoc.convert(filepath, 'rst')
            break
        else:
            with open(filepath, 'r') as stream:
                readme = stream.read()
                break
    return readme


def parse_requirements(path):
    template = '{name}{spec}'
    requirements = set()
    dependency_links = set()
    for requirement in pip.req.parse_requirements(path, session="somesession"):
        if requirement.markers is not None and not requirement.markers.evaluate():
            continue

        name = requirement.name
        spec = str(requirement.req.specifier) if len(str(requirement.req.specifier)) else ''
        req = template.format(name=name, spec=spec)
        if req:
            requirements.add(req)

        link = str(requirement.link) if requirement.link else ''
        if link:
            dependency_links.add(link)

        # TODO: What do we do with these?
        if requirement.options:
            pass

    return list(sorted(requirements)), list(sorted(dependency_links))


def display(object):
    print('-' * 80)
    for d in dir(object):
        try:
            val = getattr(object, d)
            if hasattr(val, '__call__'):
                continue
            print('{key}: {value}'.format(key=d, value=val))
        except:
            print('{key}: {value}'.format(key=d, value='ERROR: could not display'))
    print('-' * 80)

if __name__ == '__main__':
    main()
