#!/usr/bin/env python

import pytest
import sys

import os
from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()


def test_cmake_load_vars():
    template_dir = os.path.join(root_dir, 'tests')

    want = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1'
    }

    got = cproject.CMake.load_vars(
        os.path.join(template_dir, 'settings.cmake'))

    success = True
    for name in want:
        want_val = want[name]
        try:
            got_val = got[name]
            if want_val != got_val:
                sys.stderr.write('- {} = \'{}\'\n'.format(name, want_val))
                sys.stderr.write('+ {} = \'{}\'\n'.format(name, got_val))
                success = False
        except KeyError:
            sys.stderr.write('- {} = \'{}\'\n'.format(name, want_val))
            success = False

    for name in got:
        got_val = got[name]
        try:
            want_val = want[name]
        except KeyError as e:
            sys.stderr.write('+ {} = \'{}\'\n'.format(name, got_val))
            success = False

    if not success:
        pytest.fail("cmake variables load failed")
