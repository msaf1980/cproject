#!/usr/bin/env python

import pytest
import sys

import os
from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()


def test_template_simple():
    s = r'set(PROJECT {{PROJECT}})\nset(VERSION {{VERSION}})\nset(PROJECT_COMPILE_FEATURES cxx_std_{{CXX_STD}} c_std_{{C_STD}})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        '{{CXX_STD}}': '17',
        '{{C_STD}}': '11',
    }

    want = r'set(PROJECT test)\nset(VERSION 0.1)\nset(PROJECT_COMPILE_FEATURES cxx_std_17 c_std_11)\n'

    got = cproject.Template.render(s, vars)
    assert got == want


def test_template_if():
    s = r'set(PROJECT_COMPILE_FEATURES{%if {{CXX}} %} cxx_std_{{CXX_STD}}{%endif%}{%if {{C_STD}} %} c_std_{{C_STD}}{%endif%})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        # '{{CXX}}': 'True',
        # '{{CXX_STD}}': '17',
        # '{{C}}': 'True',
        '{{C_STD}}': '11',
    }

    want = r'set(PROJECT_COMPILE_FEATURES c_std_11)\n'

    got = cproject.Template.render(s, vars)
    assert got == want


def test_template_if_error_if_unlosed():
    # unclosed {%if {{CXX}} }
    s = r'set(PROJECT_COMPILE_FEATURES{%if {{CXX}} } cxx_std_{{CXX_STD}}{%endif%})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        '{{CXX_STD}}': '17',
        '{{C_STD}}': '11',
    }

    got = ''
    try:
        got = cproject.Template.render(s, vars)
    except ValueError:
        return

    pytest.fail('must fail, but got \'{}\''.format(got))


def test_template_if_error_noendif():
    # mistake: {%end%} instead of {%endif%}
    s = r'set(PROJECT_COMPILE_FEATURES{%if {{CXX}} %} cxx_std_{{CXX_STD}}{%end%})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        '{{CXX_STD}}': '17',
        '{{C_STD}}': '11',
    }

    got = ''
    try:
        got = cproject.Template.render(s, vars)
    except ValueError:
        return

    pytest.fail('must fail, but got \'{}\''.format(got))


def test_template_if_error_var_unexpanded():
    # mistake: {%end%} instead of {%endif%}
    s = r'set(PROJECT_COMPILE_FEATURES cxx_std_{{CXX_STD}})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        # '{{CXX_STD}}': '17',
        '{{C_STD}}': '11',
    }

    got = ''
    try:
        got = cproject.Template.render(s, vars)
    except ValueError:
        return

    pytest.fail('must fail, but got \'{}\''.format(got))



def test_template_if_error_unexpected():
    # mistake: {%end%} instead of {%endif%}
    s = r'set(PROJECT_COMPILE_FEATURES{% 11 {%endif%})\n'
    vars = {
        '{{PROJECT}}': 'test',
        '{{VERSION}}': '0.1',
        # '{{CXX_STD}}': '17',
        '{{C_STD}}': '11',
    }

    got = ''
    try:
        got = cproject.Template.render(s, vars)
    except ValueError:
        return

    pytest.fail('must fail, but got \'{}\''.format(got))    