#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import sys

import click
import rb_tutorial


@click.command()
@click.option('--version', count=True, help='display version')
@click.option('-v', '--verbose', count=True, help='more spam')
def main(version, verbose):
    if version:
        project_name = rb_tutorial.__name__
        version = rb_tutorial.__version__

        print(f"{project_name} {version}")
        sys.exit()

if __name__ == '__main__':
    main()
