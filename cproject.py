#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import shutil
import yaml
import re
import collections


def exit_error(msg):
    if msg:
        sys.stderr.write(msg + "\n")
        sys.exit(1)


def substr(s, start, length=0):
    if start >= len(s):
        raise ""
    elif start < 0:
        start = 0
    l = len(s) - start
    if length > l or length < 1:
        length = l
    pref = ''
    suf = ''
    if start > 0:
        pref = '..'
    if length + start < len(s) - 1:
        suf = '..'
    return pref + s[start:start+length] + suf


class Template:
    start_var_regex = re.compile(r'{{ ([A-Za-z0-9_\-]+) }}')

    @staticmethod
    def __iter_with_eval__(s):
        result = []
        pos = 0
        idx = s.find('{%if ', pos)
        if idx == -1:
            return s
        while idx >= 0:
            result.append(s[pos:idx])
            end = s.find(' %}', idx+5)
            # end = s.find('{%endif%}', idx+5)
            if end == -1:
                raise ValueError(
                    "unclosed if block: {}".format(substr(s, idx, 50)))
            # sys.stderr.write(s[idx+5:end]+'\n')
            # sys.stderr.write(str(result)+'\n')
            try:
                # sys.stderr.write(s[idx+5:end])
                add_block = eval(s[idx+5:end])
                # sys.stderr.write(', expand = ' + str(add_block) + '\n')
            except Exception:
                if s[idx+5:end].find('{{') == -1:
                    raise ValueError(
                        "unable to eval if block: {}".format(substr(s, idx, end+3)))
                else:
                    add_block = False
            pos = end + 3
            end = s.find('{%endif%}', pos)
            if end == -1:
                raise ValueError(
                    "no endif block: {}".format(substr(s, idx, 100)))
            if add_block:
                result.append(s[pos:end])
            pos = end + 9
            if pos >= len(s):
                break
            idx = s.find('{%if ', pos)

        if pos < len(s):
            result.append(s[pos:])

        return ''.join(result)

    @ staticmethod
    def render(s, vars_map):
        # replace variables
        for k, v in vars_map.items():
            s = s.replace(k, v)

        s = Template.__iter_with_eval__(s)

        m = Template.start_var_regex.findall(s)
        if m:
            raise ValueError('unable to expand vars: {}'.format(str(m)))

        idx = s.find('{%')
        if idx != -1:
            raise ValueError('unexpected: {}'.format(substr(s, idx, 50)))

        return s


def template(s, vars):
    return Template.render(s, vars)


def populate(source_dir, dest_dir, vars, root_exist=False):
    if root_exist:
        if not os.path.exists(dest_dir):
            raise ValueError("{} not exists".format(dest_dir))
    elif os.path.exists(dest_dir):
        raise ValueError("{} already exists".format(dest_dir))
    else:
        os.mkdir(dest_dir)

    sfiles = os.listdir(source_dir)

    if root_exist:
        dfiles = set(os.listdir(dest_dir))
        for f in sfiles:
            if f in dfiles:
                raise ValueError("{} already exists".format(
                    os.path.join(dest_dir, f)))

    for f in sfiles:
        if f in ('project.yml', 'target.yml'):
            continue  # skip description

        spath = os.path.join(source_dir, f)
        tpath = os.path.join(dest_dir, f)
        if os.path.isfile(spath):
            template_expand(spath, tpath, vars)
            # if spath.endswith('.tpl'):
            #     template_expand(spath, tpath[:-4], vars)
            # else:
            #     shutil.copy(spath, tpath)
        elif os.path.isdir(spath):
            populate(spath, tpath, vars)


def project_type(project_dir):
    for ptype in Project.TYPES:
        project_files = Project.TYPES[ptype]
        for f in project_files:
            found = True
            path = os.path.join(project_dir, f)
            if not os.path.isfile(path):
                found = False
                break
            if found:
                return ptype

    raise ValueError("unknown project type")


class CMakeTargets:
    FILE = 'targets.cmake'

    @ staticmethod
    def add(project_dir, dirs):
        if not dirs is None and len(dirs) > 0:
            current_subdirs = set()
            with open(os.path.join(project_dir, CMakeTargets.FILE), 'r') as fd:
                for s in fd:
                    current_subdirs.add(s)
            with open(os.path.join(project_dir, CMakeTargets.FILE), 'a') as fd:
                for d in dirs:
                    subdir = 'add_subdirectory({})\n'.format(d)
                    if not subdir in current_subdirs:
                        fd.write(subdir)

#  Project
#    name         Template name
#    path          Template path
#    type         Template project type (from TYPES, by required file list)
#    description  Project description (from project.yml)


class Project:
    # map with project_type: required files in project root
    TYPES = {
        'cmake': {'CMakeLists.txt', CMakeTargets.FILE},
        'make': {'Makefile'}
    }

    def __init__(self, template_dir):
        self.path = template_dir
        self.name = os.path.basename(template_dir)
        with open(os.path.join(template_dir, 'project.yml'), 'r') as stream:
            yml = yaml.safe_load(stream)
            self.description = yml.get('description', '')
        self.type = project_type(template_dir)

    def create(self, project_dir, project_name, vars):
        vars['{{ PROJECT }}'] = project_name
        sys.stdout.write("Creating project {} in {}\n".format(
            project_name, project_dir))
        populate(self.path, project_dir, vars)


PROJECT_FORMAT = "project_dir[:project_name]"

# split project with PROJECT_FORMAT pattern


def split_project(project):
    vs = project.split(':')
    if len(vs) > 2:
        raise ValueError("project is invalid: '{}', use {} format".format(project, PROJECT_FORMAT))
    elif len(vs) == 2:
        return vs[0], vs[1]
    else:
        return vs[0], os.path.basename(vs[0])


class Projects:
    def __init__(self, template_dirs):
        self.map = dict()

        for dir in template_dirs:
            pdir = os.path.join(dir, 'projects')
            if os.path.isdir(pdir):
                for f in os.listdir(pdir):
                    if f in self.map:  # avoid duplicate
                        sys.stderr.write(
                            "WARN: project template {} is duplicate in '{}'\n".format(f, pdir))
                    else:
                        path = os.path.join(pdir, f)
                        if os.path.isdir(path):
                            self.map[f] = Project(path)

    def names(self):
        return self.map

    def get(self, key):
        return self.map[key]

# Target
#    name              Template name
#    path              Template path
#    project_type      Template project type
#    description  Project description (from project.yml)


class Target:
    def __init__(self, template_dir, project_type):
        self.name = os.path.basename(template_dir)
        self.path = template_dir
        self.project_type = project_type
        target_config = os.path.join(template_dir, 'target.yml')
        with open(target_config, 'r') as stream:
            yml = yaml.safe_load(stream)
            self.description = yml.get('description', '')
            if self.project_type == 'cmake':
                self.cmake = yml.get('cmake')

    def create(self, project_dir, target_name, dir_in_project, vars):
        vars['{{ TARGET }}'] = target_name
        if dir_in_project is None:
            tdir = project_dir
            in_root = True
        else:
            tdir = os.path.join(project_dir, dir_in_project)
            in_root = False
        sys.stdout.write("Creating target {} ({}) in project {}\n".format(
            target_name, self.name, project_dir))
        populate(self.path, tdir, vars, in_root)
        if self.project_type == 'cmake':
            CMakeTargets.add(project_dir, self.cmake)


TARGET_FORMAT = "target_template:target_name[:dir_in_project]"

# split target with TARGET_FORMAT pattern


def split_target(target):
    vs = target.split(':')
    if len(vs) != 3 and len(vs) != 2:
        raise ValueError("target is invalid: '{}', use {} format".format(target, TARGET_FORMAT))
    elif len(vs) == 3:
        return vs[0], vs[1], vs[2]
    else:
        return vs[0], vs[1], None


class Targets:
    def __init__(self, template_dirs):
        self.map = dict()

        for dir in template_dirs:
            for project_type in Project.TYPES:
                tdir = os.path.join(dir, 'targets', project_type)
                if os.path.isdir(tdir):
                    for f in os.listdir(tdir):
                        ftype = project_type + ':' + f
                        if ftype in self.map:  # avoid duplicate
                            sys.stderr.write(
                                "WARN: target template {} is duplicate in '{}'\n".format(ftype, tdir))
                        else:
                            path = os.path.join(tdir, f)
                            if os.path.isdir(path):
                                self.map[ftype] = Target(path, project_type)

    def names(self):
        return self.map

    def get(self, key):
        return self.map[key]

    def get_by_type(self, project_type, name):
        return self.map[project_type + ':' + name]


def template_expand(source, dest, vars):
    if len(dest) == 0:
        raise ValueError("destination not set for template {}".format(source))

    with open(source) as ifd:
        slines = ifd.read()
        try:
            olines = template(slines, vars)
        except Exception as e:
            raise ValueError(
                "unable to expand template for {}: {}".format(source, str(e)))
        ofd = open(dest, "w")
        ofd.write(olines)
        ofd.close()


def parse_cmdline(template_dirs):
    parser = argparse.ArgumentParser(
        description='C/C++ project generator (not only for CMake)', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-V', '--version', dest='version',
                        action='store', default='0.1', help='project version')
    parser.add_argument('-s', '--templates', type=str, dest='template_dir', action='store', default=None,
                        help='template dir (default in %s)' % str(template_dirs))

    subparsers = parser.add_subparsers(help='types of arguments')

    list_parser = subparsers.add_parser('list', help='List all templates')
    list_parser.add_argument_group('list')

    new_parser = subparsers.add_parser("new", help='New project')
    new_group = new_parser.add_argument_group('new')
    new_group.add_argument('-t', '--template', dest='template',
                           action='store', required=True, help='create project from template')
    new_group.add_argument('-C', '--cxx-std', dest='cxx_std',
                           action='store', type=int, default=0, help='C++ standart version (for example 11, 17, 20 or 23)')
    new_group.add_argument('-c', '--c-std', dest='c_std',
                           action='store', type=int, default=0, help='C standart version (for example 99, 11, 17, 20 or 23)')
    new_group.add_argument('project', nargs="+", help=PROJECT_FORMAT)
    new_group.add_argument('-T', '--target', dest='target',
                           action='append', help=TARGET_FORMAT)

    add_parser = subparsers.add_parser("add", help='Add target to project')
    add_group = add_parser.add_argument_group('add')
    add_group.add_argument('-p', '--project', dest='dir',
                           action='store', default='.', help='project dir')
    add_group.add_argument('target', nargs="+", help=TARGET_FORMAT)

    return parser.parse_args()


def main():
    home = os.path.expanduser("~")
    template_dirs = ['cproject', os.path.join(home, ".local/cproject"), os.path.join(
        home, ".local/share/cproject"), "/usr/local/share/cproject", "/usr/share/cproject"]

    args = parse_cmdline(template_dirs)

    if not args.template_dir is None:
        template_dirs.insert(0, args.template_dir)

    project_templates = Projects(template_dirs)
    target_templates = Targets(template_dirs)

    if hasattr(args, 'project'):
        p = project_templates.get(args.template)
        for project in args.project:
            vars = dict()
            vars['{{ VERSION }}'] = args.version
            if args.cxx_std > 0:
                vars['{{ CXX_STD }}'] = str(args.cxx_std)
            if args.c_std > 0:
                vars['{{ C_STD }}'] = str(args.c_std)
            project_dir, project_name = split_project(project)
            p.create(project_dir, project_name, vars)
            if hasattr(args, 'target'):
                ptype = project_type(project_dir)
                for target in args.target:
                    target_template, target_name, dir_in_project = split_target(
                        target)
                    t = target_templates.get_by_type(ptype, target_template)
                    t.create(project_dir, target_name, dir_in_project, vars)
    elif hasattr(args, 'target'):
        vars = dict()
        vars['{{ VERSION }}'] = args.version
        if args.cxx_std > 0:
            vars['{{ CXX_STD }}'] = str(args.cxx_std)
        if args.c_std > 0:
            vars['{{ C_STD }}'] = str(args.c_std)
        ptype = project_type(args.dir)
        for target in args.target:
            target_template, target_name, dir_in_project = split_target(target)
            t = target_templates.get_by_type(ptype, target_template)
            t.create(args.dir, target_name, dir_in_project, vars)
    else:
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')
        sys.stdout.write('| {:<10} | {:<30} | {:<50} | {}\n'.format(
            'Proj. type', 'Project template', 'Path', 'Description'))
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')
        for project in project_templates.names():
            v = project_templates.get(project)
            sys.stdout.write(
                '| {:<10} | {:<30} | {:<50} | {}\n'.format(v.type, v.name, v.path, v.description))
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')

        sys.stdout.write('\n')
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')
        sys.stdout.write('| {:<10} | {:<30} | {:<50} | {}\n'.format(
            'Proj. type',  'Target template', 'Path', 'Description'))
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')
        for target in target_templates.names():
            v = target_templates.get(target)
            sys.stdout.write('| {:<10} | {:<30} | {:<50} | {}\n'.format(
                v.project_type, v.name, v.path, v.description))
        sys.stdout.write(
            '------------------------------------------------------------------------------------------------------------------\n')


if __name__ == "__main__":
    main()
