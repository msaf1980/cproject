#!/usr/bin/env python

import pytest
import sys

import os
from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()


def test_projects_load():
    template_dirs = [os.path.join(root_dir, 'tests')]

    want = {
        'cmake': cproject.Project('cmake', os.path.join(root_dir, 'tests/projects/cmake'), 'cmake', 'CMake project (without targets)'),
        'make': cproject.Project('make', os.path.join(root_dir, 'tests/projects/make'), 'make', 'Make project')
    }

    got = cproject.Projects(template_dirs)

    success = True
    for name in want:
        want_project = want[name]
        try:
            got_project = got.get(name)
            if want_project != got_project:
                sys.stderr.write('- {}\n'.format(str(want_project)))
                sys.stderr.write('+ {}\n'.format(str(got_project)))
                success = False
        except KeyError as e:
            sys.stderr.write('- {}\n'.format(str(want_project)))
            success = False

    for name in got.names():
        got_project = got.get(name)
        try:
            want_project = want[name]
        except KeyError as e:
            sys.stderr.write('+ {}\n'.format(str(got_project)))
            success = False

    if not success:
        pytest.fail("project templates load failed")
