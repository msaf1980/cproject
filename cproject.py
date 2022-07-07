#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import shutil
import yaml
import re
# import collections


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
    start_var_regex = re.compile(r'{{([A-Za-z0-9_\-]+)}}')

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
            if end == -1:
                raise ValueError(
                    "unclosed if block: {}".format(substr(s, idx, 50)))
            try:
                add_block = eval(s[idx+5:end])
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


def template_expand(source, dest, vars):
    if len(dest) == 0:
        raise ValueError("destination not set for template {}".format(source))

    with open(source) as ifd:
        slines = ifd.read()
        try:
            olines = Template.render(slines, vars)
        except Exception as e:
            raise ValueError(
                "unable to expand template for {}: {}".format(source, str(e)))
        ofd = open(dest, "w")
        ofd.write(olines)
        ofd.close()


def populate(source_dir, dest_dir, vars, update):
    if update:
        if not os.path.exists(dest_dir):
            raise ValueError("{} not exists".format(dest_dir))
        raise ValueError("update not realized yet")
    elif os.path.exists(dest_dir):
        raise ValueError("{} already exists".format(dest_dir))
    else:
        os.mkdir(dest_dir)

    sfiles = os.listdir(source_dir)

    # if update:
    #     dfiles = set(os.listdir(dest_dir))
    #     for f in sfiles:
    #         if f in dfiles:
    #             raise ValueError("{} already exists".format(
    #                 os.path.join(dest_dir, f)))

    for f in sfiles:
        if f in ('project.yml', 'target.yml', 'addon.yml'):
            continue  # skip config file

        fdest = Template.render(f, vars)

        spath = os.path.join(source_dir, f)
        tpath = os.path.join(dest_dir, fdest)
        if os.path.isfile(spath):
            template_expand(spath, tpath, vars)
            # if spath.endswith('.tpl'):
            #     template_expand(spath, tpath[:-4], vars)
            # else:
            #     shutil.copy(spath, tpath)
        elif os.path.isdir(spath):
            populate(spath, tpath, vars, update)


def project_get_type(project_dir):
    if not os.path.isdir(project_dir):
        raise ValueError("project dir not exist")
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
    def add(project_dir, dir_in_project):
        if dir_in_project is None or dir_in_project.startswith('.'):
            raise ValueError('invalid subdir for project \'{}\' targets: \'{}\''.format(
                project_dir, dir_in_project))

        if not os.path.isfile(os.path.join(project_dir, dir_in_project, 'CMakeLists.txt')):
            return

        current_subdirs = set()
        targets_file = os.path.join(project_dir, CMakeTargets.FILE)
        with open(targets_file, 'r') as fd:
            for s in fd:
                current_subdirs.add(s.strip())
        with open(targets_file, 'a') as fd:
            subdir = 'add_subdirectory({})'.format(dir_in_project)
            if not subdir in current_subdirs:
                sys.stdout.write(
                    "Add {} to {}\n".format(dir_in_project, targets_file))
                fd.write(subdir)
                fd.write(os.linesep)

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

    @staticmethod
    def load(template_dir):
        path = template_dir
        name = os.path.basename(template_dir)
        description = ''
        with open(os.path.join(template_dir, 'project.yml'), 'r') as stream:
            yml = yaml.safe_load(stream)
            description = yml.get('description', '')
        ptype = project_get_type(template_dir)

        return Project(name, path, ptype, description)

    def __init__(self, name, path, project_type, description):
        self.name = name
        self.path = path
        self.project_type = project_type
        self.description = description

    def __str__(self):
        return "{ name : '%s', path : '%s', project_type : '%s', description : '%s' }" % \
            (self.name, self.path, self.project_type, self.description)

    def __eq__(self, other):
        if (isinstance(other, Project)):
            return self.name == other.name and self.path == other.path and self.project_type == other.project_type and \
                self.description == other.description

    def create(self, project_dir, project_name, vars, update=False):
        vars['{{PROJECT}}'] = project_name
        if update:
            sys.stdout.write("Updating project {} in {}\n".format(
                project_name, project_dir))
        else:
            sys.stdout.write("Creating project {} in {}\n".format(
                project_name, project_dir))
        populate(self.path, project_dir, vars, update)


PROJECT_FORMAT = "project_dir[:project_name]"

# split project with PROJECT_FORMAT pattern


def split_project(project):
    vs = project.split(':')
    if len(vs) > 2:
        raise ValueError("project is invalid: '{}', use {} format".format(
            project, PROJECT_FORMAT))
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
                            self.map[f] = Project.load(path)

    def names(self):
        return self.map

    def get(self, key):
        return self.map[key]

# Target
#    name              Template name
#    path              Template path
#    project_type      Template project type
#    description       Project description (from project.yml)
#    options:          optional files and directories in _optional/OPTION_NAME


class Target:
    @staticmethod
    def load(template_dir, project_type):
        name = os.path.basename(template_dir)
        description = ''

        target_config = os.path.join(template_dir, 'target.yml')
        with open(target_config, 'r') as stream:
            yml = yaml.safe_load(stream)
            description = yml.get('description', '')

        return Target(name, template_dir, project_type, description)

    def __init__(self, name, path, project_type, description):
        self.name = name
        self.path = path
        self.project_type = project_type
        self.description = description

    def __str__(self):
        return "{ name : '%s', path : '%s', project_type : '%s', description : '%s' }" % \
            (self.name, self.path, self.project_type, self.description)

    def __eq__(self, other):
        if (isinstance(other, Target)):
            return self.name == other.name and self.path == other.path and self.project_type == other.project_type and \
                self.description == other.description

        return False

    def create(self, project_dir, target_name, dir_in_project, vars, update=False):
        vars['{{TARGET}}'] = target_name
        tdir = os.path.join(project_dir, dir_in_project)
        basedir = os.path.dirname(tdir)
        if basedir != project_dir and not os.path.isdir(basedir):
            os.makedirs(basedir)
        if update:
            sys.stdout.write("Updating target {} ({}) in project {}\n".format(
                target_name, self.name, project_dir))
        else:
            sys.stdout.write("Creating target {} ({}) in project {}\n".format(
                target_name, self.name, project_dir))
        populate(self.path, tdir, vars, update)
        if self.project_type == 'cmake':
            CMakeTargets.add(project_dir, dir_in_project)


TARGET_FORMAT = "target_template:target_name:dir_in_project"

# split target with TARGET_FORMAT pattern


def split_target(target):
    vs = target.split(':')
    if len(vs) != 3:
        raise ValueError(
            "target is invalid: '{}', use {} format".format(target, TARGET_FORMAT))
    elif vs[2] == '' or vs[2].startswith('.'):
        raise ValueError(
            "target dir_in_project is invalid: '{}'".format(target))
    return vs[0], vs[1], vs[2]


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
                                self.map[ftype] = Target.load(
                                    path, project_type)

    def names(self):
        return self.map

    def get(self, key):
        return self.map[key]

    def get_by_type(self, project_type, name):
        return self.map[project_type + ':' + name]


def parse_cmdline(template_dirs):
    parser = argparse.ArgumentParser(
        description='C/C++ project generator (not only for CMake)', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-V', '--version', dest='version',
                        action='store', default='0.1', help='project version')
    parser.add_argument('-s', '--templates', type=str, dest='template_dir', action='store', default=None,
                        help='template dir (default in %s)' % str(template_dirs))
    parser.add_argument('-C', '--cxx-std', dest='cxx_std',
                        action='store', type=int, help='Pass C++ standart version as CXX_STD variable (for example 11, 17, 20 or 23)')
    parser.add_argument('-c', '--c-std', dest='c_std',
                        action='store', type=int, help='Pass C standart version as C_STD variable (for example 99, 11, 17, 20 or 23)')
    # parser.add_argument('-o', '--option', dest='option', default=None,
    #                     action='append', help='install optional option files (from _optional/OPTIONAL subdirs)')

    subparsers = parser.add_subparsers(help='types of arguments', dest='which')

    list_parser = subparsers.add_parser('list', help='List all templates')
    list_parser.add_argument_group('list')

    new_parser = subparsers.add_parser("new", help='New project')
    new_group = new_parser.add_argument_group('new')
    new_group.add_argument('-t', '--template', dest='template',
                           action='store', required=True, help='create project from template')
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

    if args.which == 'new':  # new project
        p = project_templates.get(args.template)
        for project in args.project:
            vars = dict()
            vars['{{VERSION}}'] = args.version
            if not args.cxx_std is None:
                vars['{{CXX_STD}}'] = str(args.cxx_std)
            if not args.c_std is None:
                vars['{{C_STD}}'] = str(args.c_std)
            project_dir, project_name = split_project(project)
            p.create(project_dir, project_name, vars)
            if hasattr(args, 'target') and not args.target is None:
                ptype = project_get_type(project_dir)
                for target in args.target:
                    target_template, target_name, dir_in_project = split_target(
                        target)
                    t = target_templates.get_by_type(ptype, target_template)
                    t.create(project_dir, target_name,
                             dir_in_project, vars)
    elif args.which == 'add':  # Add target to project
        vars = dict()
        vars['{{VERSION}}'] = args.version
        if not args.cxx_std is None:
            vars['{{CXX_STD}}'] = str(args.cxx_std)
        if not args.c_std is None:
            vars['{{C_STD}}'] = str(args.c_std)
        ptype = project_get_type(args.dir)
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
                '{:<10} | {:<30} | {:<50} | {}\n'.format(v.project_type, v.name, v.path, v.description))
        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')

        sys.stdout.write('\n')
        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')
        sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
            'Proj. type',  'Target template', 'Path', 'Description'))
        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')
        for target in target_templates.names():
            v = target_templates.get(target)
            sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                v.project_type, v.name, v.path, v.description))
        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')


if __name__ == "__main__":
    main()
