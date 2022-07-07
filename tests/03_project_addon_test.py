#!/usr/bin/env python

import pytest
import sys

import os
from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()


def test_project_addon_load():
    template_dirs = [os.path.join(root_dir, 'tests')]

    want = {
        'cmake': {
            'catch3': cproject.ProjectAddon('catch3', os.path.join(root_dir, 'tests/project_addons/cmake/catch3'), 'cmake', 'Download Catch2 (version >= 3.0.0) with FetchContent', set()),
            'test_catch3_cpp': cproject.ProjectAddon('test_catch3_cpp', os.path.join(root_dir, 'tests/project_addons/cmake/test_catch3_cpp'), 'cmake', 'Tests with Catch2 (> 3.0.0, delivered with FetchContent) (C++) (in tests directory of CMake project root, target is a project name)', {'cmake_dep/Catch2_3_FetchContent.cmake'})
        },
    }

    got = cproject.ProjectAddons(template_dirs)

    success = True
    for project_type in want:
        wtemplates = want[project_type]
        for name in wtemplates:
            want_project = wtemplates[name]
            try:
                got_project = got.get(project_type, name)
                assert got_project == want_project
                if want_project != got_project:
                    sys.stderr.write(
                        '- {}: {}: {}\n'.format(project_type, name, str(want_project)))
                    sys.stderr.write(
                        '+ {}: {}: {}\n'.format(project_type, name, str(got_project)))
                    success = False
            except KeyError as e:
                sys.stderr.write(
                    '- {}: {}: {}\n'.format(project_type, name, str(want_project)))
                success = False

    for project_type in got.get_project_types():
        gtemplates = got.get_templates(project_type)
        for name in gtemplates:
            got_project = gtemplates[name]
            try:
                want_project = want[project_type][name]
            except KeyError as e:
                sys.stderr.write(
                    '+ {}: {}: {}\n'.format(project_type, name, str(got_project)))
                success = False

    if not success:
        pytest.fail("project addon templates load failed")
