#!/usr/bin/env python

import pytest
import os
import sys
import time
import platform
import subprocess
import tempfile
import shutil

from importlib.machinery import SourceFileLoader

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject = SourceFileLoader('module.name', os.path.join(
    root_dir, 'cproject.py')).load_module()

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cproject_script = os.path.join(root_dir, 'cproject.py')
template_dir = os.path.join(root_dir, 'cproject')

build_subdir = '_build'

cmake = os.environ.get('CPROJECT_CMAKE', 'cmake')


def test_list():
    subprocess.run([cproject_script, '-s',  template_dir, 'list'], check=True)


def test_cmake_new_project_and_add_addons():
    project_name = 'test_proj'

    temp_dir = tempfile.mkdtemp(prefix='cproject_')

    project_dir = os.path.join(temp_dir, project_name)
    build_dir = os.path.join(project_dir, build_subdir)

    # create cmake project without targets
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'new', '-t', 'cmake', project_dir]
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        pytest.fail(str(e))

    vars = cproject.CMake.load_vars(
        os.path.join(project_dir, cproject.CMake.SETTINGS))
    want_project_name = os.path.basename(
        project_dir).replace('-', '_').replace(' ', '_')

    assert vars['{{PROJECT}}'] == want_project_name
    assert vars['{{VERSION}}'] == '0.1'

    os.mkdir(build_dir)
    os.chdir(build_dir)

    # try to build
    subprocess.run([cmake, '-DCMAKE_BUILD_TYPE=Release',  '..'],
                   stderr=subprocess.STDOUT, check=True)
    subprocess.run([cmake, '--build',  '.'], check=True)

    # add binary target
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'addon', '-p', project_dir, 'bin_cpp']
    try:
        subprocess.run(cmd, stderr=subprocess.STDOUT, check=True)
    except Exception as e:
        pytest.fail(str(e))

    dirs = ['src', 'include']
    for d in dirs:
        dir = os.path.join(project_dir, d)
        if not os.path.exists(dir):
            pytest.fail('addon directory \'{}\' not exists'.format(dir))

    subprocess.run([cmake, '-DCMAKE_BUILD_TYPE=Release',  '..'],
                   stderr=subprocess.STDOUT, check=True)
    subprocess.run([cmake, '--build',  '.'],
                   stderr=subprocess.STDOUT, check=True)

    target = os.path.join(build_dir, 'src', project_name)
    if platform.system() == 'Windows':
        target += '.exe'
    if not os.path.exists(target):
        pytest.fail('target \'{}\' not exists'.format(target))

    subprocess.run([target], stderr=subprocess.STDOUT, check=True)

    # add test target, mus fail (dependency not resolved)
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'addon', '-p', project_dir, 'test_catch3_cpp']
    try:
        subprocess.run(cmd, stderr=subprocess.STDOUT, check=True)
        pytest.fail("add addon must fail (dependecies not resolved)")
    except subprocess.CalledProcessError:
        pass

    # add test target
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'addon', '-p', project_dir, 'test_catch3_cpp', 'catch3']
    try:
        subprocess.run(cmd, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError:
        pytest.fail(str(e))

    tests_dir = os.path.join(project_dir, 'tests')
    if not os.path.exists(tests_dir):
        pytest.fail('addon directory \'{}\' not exists'.format(tests_dir))

    subprocess.run([cmake, '-DCMAKE_BUILD_TYPE=Release',  '..'],
                   stderr=subprocess.STDOUT, check=True)
    subprocess.run([cmake, '--build',  '.'],
                   stderr=subprocess.STDOUT, check=True)

    test_target = os.path.join(build_dir, 'tests', 'test_' + project_name)
    if platform.system() == 'Windows':
        test_target += '.exe'
    if not os.path.exists(test_target):
        pytest.fail('target \'{}\' not exists'.format(test_target))

    subprocess.run([test_target], stderr=subprocess.STDOUT, check=True)

    shutil.rmtree(temp_dir)


def test_cmake_new_project_with_addons():
    project_name = 'test_proj'

    temp_dir = tempfile.mkdtemp(prefix='cproject_')

    project_dir = os.path.join(temp_dir, project_name)
    build_dir = os.path.join(project_dir, build_subdir)

    # create project must fail (addon dependecies not resolved)
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'new', '-t', 'cmake', project_dir, '-a', 'bin_cpp', '-a', 'test_catch3_cpp']
    try:
        subprocess.run(cmd, stderr=subprocess.STDOUT, check=True)
        pytest.fail("create project must fail (addon dependecies not resolved)")
    except subprocess.CalledProcessError:
        pass

    # create cmake project target
    cmd = [cproject_script, '-q', '-s',  template_dir,
           'new', '-t', 'cmake', project_dir, '-a', 'bin_cpp']
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        pytest.fail(str(e))

    vars = cproject.CMake.load_vars(
        os.path.join(project_dir, cproject.CMake.SETTINGS))
    want_project_name = os.path.basename(
        project_dir).replace('-', '_').replace(' ', '_')

    assert vars['{{PROJECT}}'] == want_project_name
    assert vars['{{VERSION}}'] == '0.1'

    dirs = ['src', 'include']
    for d in dirs:
        dir = os.path.join(project_dir, d)
        if not os.path.exists(dir):
            pytest.fail('addon directory \'{}\' not exists'.format(dir))

    os.mkdir(build_dir)
    os.chdir(build_dir)

    # try to build
    subprocess.run([cmake, '-DCMAKE_BUILD_TYPE=Release',  '..'],
                   stderr=subprocess.STDOUT, check=True)
    subprocess.run([cmake, '--build',  '.'], check=True)

    subprocess.run([cmake, '-DCMAKE_BUILD_TYPE=Release',  '..'],
                   stderr=subprocess.STDOUT, check=True)
    subprocess.run([cmake, '--build',  '.'],
                   stderr=subprocess.STDOUT, check=True)

    target = os.path.join(build_dir, 'src', project_name)
    if platform.system() == 'Windows':
        target += '.exe'
    if not os.path.exists(target):
        pytest.fail('target \'{}\' not exists'.format(target))

    subprocess.run([target], stderr=subprocess.STDOUT, check=True)
