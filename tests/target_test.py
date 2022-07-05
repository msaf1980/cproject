#!/usr/bin/env python

import pytest
import sys

import os
from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()


#   name            basename(target_template_dir)
#   path            Target template dir
#   project_type    Project type
#   description     Description
class TTarget:
    @staticmethod
    def fromTarget(target):
        return TTarget(target.name, target.path, target.project_type, target.description)

    def __init__(self, name, path, project_type, description):
        self.name = name
        self.path = path
        self.project_type = project_type
        self.description = description

    def __str__(self):
        return "{ name : '%s', path : '%s', project_type : '%s', description : '%s' }" % \
            (self.name, self.path, self.project_type, self.description)

    def __eq__(self, other):
        if (isinstance(other, TTarget)):
            return self.name == other.name and self.path == other.path and self.project_type == other.project_type and self.description == other.description

        return False


def test_targets_load():
    template_dirs = [os.path.join(root_dir, 'tests')]

    want = {
        # 'cmake': TTarget('cmake', os.path.join(root_dir, 'tests/projects/cmake'), 'cmake', 'CMake project (without targets)'),
        # 'make': TTarget('make', os.path.join(root_dir, 'tests/projects/make'), 'make', 'Make project')
        'cmake:exe_cpp': TTarget('exe_cpp', os.path.join(root_dir, 'tests/targets/cmake/exe_cpp'), 'cmake', 'Executable target for CMake project (C++)'),
        'cmake:headerlib_cpp': TTarget('headerlib_cpp', os.path.join(root_dir, 'tests/targets/cmake/headerlib_cpp'), 'cmake', 'Header-only library target for CMake project (C++)'),
        'make:headerlib_c': TTarget('headerlib_c', os.path.join(root_dir, 'tests/targets/make/headerlib_c'), 'make', 'Header-only library target for Make project (C)')
    }

    got = cproject.Targets(template_dirs)

    success = True
    for name in want:
        want_project = want[name]
        try:
            got_project = TTarget.fromTarget(got.get(name))
            if want_project != got_project:
                sys.stderr.write('- {}: {}\n'.format(name, str(want_project)))
                sys.stderr.write('+ {}: {}\n'.format(name, str(got_project)))
                success = False
        except KeyError as e:
            sys.stderr.write('- {}: {}\n'.format(name, str(want_project)))
            success = False

    for name in got.names():
        got_project = TTarget.fromTarget(got.get(name))
        try:
            want_project = want[name]

        except KeyError as e:
            sys.stderr.write('+ {}: {}\n'.format(name, str(got_project)))
            success = False

    if not success:
        pytest.fail("project templates load failed")
