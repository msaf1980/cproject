#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import yaml
import re


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
            raise ValueError('unable to expand vars: {}, replacement map is {}'.format(
                str(set(m)), vars_map))

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


def check_files(source, dest, vars, dir_can_exist=False):
    for f in os.listdir(source):
        if f in (Project.DESCRIPTION, ProjectAddon.DESCRIPTION, Target.DESCRIPTION):
            continue  # skip config file
        spath = os.path.join(source, f)
        df = Template.render(f, vars)
        dpath = os.path.join(dest, df)
        if os.path.isdir(spath):
            if os.path.isdir(dpath):
                if dir_can_exist:
                    check_files(spath, dpath, vars, dir_can_exist)
                else:
                    raise ValueError('Dir already exist: {}'.format(dpath))
            elif os.path.exists(dpath):
                raise ValueError(
                    'File already exist, but want dir: {}'.format(dpath))
        elif os.path.exists(dpath):
            raise ValueError('File already exist: {}'.format(dpath))


def populate(source_dir, dest_dir, vars, update, dir_can_exist=False):
    if update:
        if not os.path.exists(dest_dir):
            raise ValueError("{} not exists".format(dest_dir))
        raise ValueError("update not realized yet")
    elif os.path.exists(dest_dir):
        if not dir_can_exist:
            raise ValueError("{} already exists".format(dest_dir))
    else:
        os.mkdir(dest_dir)

    sfiles = os.listdir(source_dir)

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
            populate(spath, tpath, vars, update, dir_can_exist)


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


class CMake:
    TARGETS = 'targets.cmake'
    SETTINGS = 'settings.cmake'

    @ staticmethod
    def add_target(project_dir, dir_in_project):
        if dir_in_project is None or dir_in_project.startswith('.'):
            raise ValueError('invalid subdir for project \'{}\' targets: \'{}\''.format(
                project_dir, dir_in_project))

        if not os.path.isfile(os.path.join(project_dir, dir_in_project, 'CMakeLists.txt')):
            return

        current_subdirs = set()
        targets_file = os.path.join(project_dir, CMake.TARGETS)
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

    var_regex = re.compile(r'^set\( *([a-zA-Z0-9_\-]+) +(.+)\)$')

    @ staticmethod
    def load_vars(path):
        vars = dict()

        if_block = 0
        with open(path, 'r') as fd:
            for s in fd:
                s = s.strip()
                if s.startswith('if'):
                    if_block += 1
                elif s.startswith('endif') and if_block > 0:
                    if_block -= 1
                elif if_block == 0:
                    m = CMake.var_regex.findall(s)
                    if len(m) > 0:
                        vars['{{'+m[0][0]+'}}'] = m[0][1]

        return vars

#  Project
#    name          Template name
#    path          Template path
#    project_type  Template project type (from TYPES, by required file list)
#    description   Project description (from project.yml)


class Project:
    # map with project_type: required files in project root
    TYPES = {
        'cmake': {'CMakeLists.txt', CMake.TARGETS, CMake.SETTINGS},
        'make': {'Makefile'}
    }
    DESCRIPTION = 'project.yml'

    @staticmethod
    def load(template_dir):
        path = template_dir
        name = os.path.basename(template_dir)
        description = ''
        with open(os.path.join(template_dir, Project.DESCRIPTION), 'r') as stream:
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

    def exists(self, path):
        return os.path.exists(os.path.join(self.path, path))

    def create(self, project_dir, project_name, vars, update=False):
        pname = project_name.lower().replace(
            '-', '_').replace(' ', '_')
        vars['{{PROJECT}}'] = pname
        vars['{{UC_PROJECT}}'] = pname.upper()
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
                            try:
                                self.map[f] = Project.load(path)
                            except Exception as e:
                                sys.stderr.write(
                                    "WARN: project load '{}' {}\n".format(path, str(e)))

    def names(self):
        return self.map

    def projects(self):
        return self.map.values()

    def get(self, key):
        try:
            return self.map[key]
        except KeyError:
            raise KeyError('target not found: \'{}\''.format(key))


#  ProjectAddon
#    name          Template name
#    path          Template path
#    project_type  Template project type (from TYPES, by required file list)
#    description   Project description (from project.yml)


class ProjectAddon:
    DESCRIPTION = 'addon.yml'

    @staticmethod
    def load(template_dir):
        path = template_dir
        name = os.path.basename(template_dir)
        description = ''
        require = []
        with open(os.path.join(template_dir, ProjectAddon.DESCRIPTION), 'r') as stream:
            yml = yaml.safe_load(stream)
            description = yml.get('description', '')
            require = yml.get('require', [])
        ptype = os.path.basename(os.path.dirname(template_dir))

        return ProjectAddon(name, path, ptype, description, set(require))

    def __init__(self, name, path, project_type, description, require):
        self.name = name
        self.path = path
        self.project_type = project_type
        self.description = description
        self.require = require

    def __str__(self):
        return "{ name : '%s', path : '%s', project_type : '%s', require: %s, description : '%s' }" % \
            (self.name, self.path, self.project_type,
             str(self.require), self.description)

    def __eq__(self, other):
        if (isinstance(other, ProjectAddon)):
            return self.name == other.name and self.path == other.path and self.project_type == other.project_type and \
                self.description == other.description and self.require == other.require

    def exists(self, path):
        return os.path.exists(os.path.join(self.path, path))

    def create(self, project_dir, project_name, vars, update=False):
        u = project_name.lower().replace(' ', '_').replace('-', '_')
        vars['{{PROJECT}}'] = u
        if update:
            sys.stdout.write("Updating project addon {} in {}\n".format(
                self.name, project_dir))
        else:
            sys.stdout.write("Creating project addon {} in {}\n".format(
                self.name, project_dir))
            check_files(self.path, project_dir, vars, True)
        populate(self.path, project_dir, vars, update, True)


class ProjectAddons:
    def __init__(self, template_dirs):
        self.map = dict()

        for dir in template_dirs:
            for project_type in Project.TYPES:
                tdir = os.path.join(dir, 'project_addons', project_type)
                if os.path.isdir(tdir):
                    t = self.map.get(project_type)
                    if t is None:
                        t = dict()
                        self.map[project_type] = t
                    for f in os.listdir(tdir):
                        if f in t:  # avoid duplicate
                            sys.stderr.write(
                                "WARN: project addon template {} is duplicate in '{}'\n".format(f, tdir))
                        else:
                            path = os.path.join(tdir, f)
                            if os.path.isdir(path):
                                try:
                                    t[f] = ProjectAddon.load(path)
                                except Exception as e:
                                    sys.stderr.write(
                                        "WARN: project addon load '{}' {}\n".format(path, str(e)))

    def __len__(self):
        return len(self.map)

    def get_project_types(self):
        return self.map.keys()

    def get_templates(self, project_type):
        return self.map[project_type]

    def get(self, project_type, name):
        try:
            return self.map[project_type][name]
        except KeyError as e:
            raise KeyError('project addon not found by \'{}\': [\'{}\'][\'{}\']'.format(
                str(e), project_type, name))


# projecty_path
# addons         ProjectAddon iterator
# require        Required file (relative)


def require_not_found(project_path, addons):
    not_found = []
    required = set()
    for addon in addons:
        if len(addon.require) > 0:
            for require in addon.require:
                if not os.path.exists(os.path.join(project_path, require)):
                    required.add(require)

    for require in required:
        exist = False
        for addon in addons:
            if addon.exists(require):
                exist = True
                break
        if not exist:
            not_found.append(require)

    return not_found


# Target
#    name              Template name
#    path              Template path
#    project_type      Template project type
#    description       Project description (from project.yml)
#    options:          optional files and directories in _optional/OPTION_NAME


class Target:
    DESCRIPTION = 'target.yml'

    @staticmethod
    def load(template_dir, project_type):
        name = os.path.basename(template_dir)
        description = ''

        target_config = os.path.join(template_dir, Target.DESCRIPTION)
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
        tname = target_name.upper().replace(
            '-', '_').replace(' ', '_')
        vars['{{TARGET}}'] = tname
        vars['{{UC_TARGET}}'] = tname.upper()
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
            CMake.add_target(project_dir, dir_in_project)


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
                    t = self.map.get(project_type)
                    if t is None:
                        t = dict()
                        self.map[project_type] = t
                    for f in os.listdir(tdir):
                        if f in t:  # avoid duplicate
                            sys.stderr.write(
                                "WARN: target template {} is duplicate in '{}'\n".format(f, tdir))
                        else:
                            path = os.path.join(tdir, f)
                            if os.path.isdir(path):
                                try:
                                    t[f] = Target.load(
                                        path, project_type)
                                except Exception as e:
                                    sys.stderr.write(
                                        "WARN: project target load '{}' {}\n".format(path, str(e)))

    def get_project_types(self):
        return self.map.keys()

    def get_templates(self, project_type):
        return self.map[project_type]

    def get(self, project_type, name):
        try:
            return self.map[project_type][name]
        except KeyError as e:
            raise KeyError('target not found by \'{}\': [\'{}\'][\'{}\']'.format(
                str(e), project_type, name))


def projects_print(project_templates, project_types=None):
    for project in project_templates.names():
        v = project_templates.get(project)

        if not project_types is None and not v.project_type in project_types:
            continue

        sys.stdout.write(
            '-----------------------------------------------------------------------------------------------------------------------------------------\n')
        sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
            'Proj. type', 'Project template', 'Path', 'Description'))
        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')
        sys.stdout.write(
            '{:<10} | {:<30} | {:<50} | {}\n'.format(v.project_type, v.name, v.path, v.description))

        sys.stdout.write(
            '----------------------------------------------------------------------------------------------------------------------------\n')


def project_addons_print(project_type, project_addon_templates):
    try:
        ts = project_addon_templates.get_templates(project_type)
        if len(ts) > 0:
            sys.stdout.write('\n')
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
            sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                'Proj. type', 'Project addons template', 'Path', 'Description'))
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
            for target in ts:
                v = ts[target]
                sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                    v.project_type, v.name, v.path, v.description))
                if len(v.require) > 0:
                    sys.stdout.write(
                        ' {:>42} : {}\n'.format('Require', v.require))
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
    except KeyError:
        pass


def project_addon_with_files_print(project_type, project_addon_templates, required_files):
    addons = project_addon_templates.get_templates(project_type)
    if len(addons) == 0:
        return

    sys.stdout.write(
        '--------------------------------------------------------------\n')
    sys.stdout.write('{:<10} | {:<30} | {}\n'.format(
        'Proj. type',  'Proj. addon', 'Provide files'))
    sys.stdout.write(
        '--------------------------------------------------------------\n')

    for addon in addons.values():
        files = []
        for f in required_files:
            if addon.exists(f):
                files.append(f)
        if len(files) > 0:
            sys.stdout.write('{:<10} | {:<30} | {}\n'.format(
                project_type, addon.name,  str(files)))


def project_targets_print(project_type, target_templates):
    try:
        ts = target_templates.get_templates(project_type)
        if len(ts) > 0:
            sys.stdout.write('\n')
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
            sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                'Proj. type',  'Target template', 'Path', 'Description'))
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
            for target in ts:
                vt = ts[target]
                sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                    vt.project_type, vt.name, vt.path, vt.description))
    except KeyError:
        pass

    sys.stdout.write(
        '-----------------------------------------------------------------------------------------------------------------------------------------\n')


def project_print(project, project_addon_templates, target_templates):
    sys.stdout.write(
        '-----------------------------------------------------------------------------------------------------------------------------------------\n')
    sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
        'Proj. type', 'Project template', 'Path', 'Description'))
    sys.stdout.write(
        '----------------------------------------------------------------------------------------------------------------------------\n')
    sys.stdout.write(
        '{:<10} | {:<30} | {:<50} | {}\n'.format(project.project_type, project.name, project.path, project.description))

    sys.stdout.write(
        '----------------------------------------------------------------------------------------------------------------------------\n')

    project_addons_print(project.project_type, project_addon_templates)
    project_targets_print(project.project_type, target_templates)


def projects_by_types_print(project_types,  project_templates, project_addon_templates, target_templates):
    for project in project_templates.names():
        v = project_templates.get(project)
        if v.project_type in project_types:
            sys.stdout.write(
                '-----------------------------------------------------------------------------------------------------------------------------------------\n')
            sys.stdout.write('{:<10} | {:<30} | {:<50} | {}\n'.format(
                'Proj. type', 'Project template', 'Path', 'Description'))
            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')
            sys.stdout.write(
                '{:<10} | {:<30} | {:<50} | {}\n'.format(v.project_type, v.name, v.path, v.description))

            sys.stdout.write(
                '----------------------------------------------------------------------------------------------------------------------------\n')

            project_addons_print(v.project_type, project_addon_templates)
            project_targets_print(v.project_type, target_templates)


def parse_cmdline(template_dirs):
    parser = argparse.ArgumentParser(
        description='C/C++ project generator (not only for CMake)', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-V', '--version', dest='version',
                        action='store', default='0.1.0', help='project version')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False,
                        help='non-interactive mode')
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
    list_parser.add_argument('project_type', nargs="*", help='Project type')

    new_parser = subparsers.add_parser("new", help='New project')
    new_group = new_parser.add_argument_group('new')
    new_group.add_argument('-t', '--template', dest='template',
                           action='store', default=None, help='create project from template')
    new_group.add_argument(
        'project', nargs=1, help='{} (if project_name not set, dir basename with striped - is used)'.format(PROJECT_FORMAT))
    new_group.add_argument('-T', '--target', dest='target',
                           action='append', help=TARGET_FORMAT)
    new_group.add_argument('-a', '--addon', dest='addon', default=None,
                           action='append', help='install optional addons')

    addon_parser = subparsers.add_parser("addon", help='Add addon to project')
    addon_group = addon_parser.add_argument_group('addon')
    addon_group.add_argument('-p', '--project', dest='dir',
                             action='store', default='.', help='project dir')
    addon_group.add_argument('addon', nargs="*", help='Project addon')

    target_parser = subparsers.add_parser(
        "target", help='Add target to project')
    target_group = target_parser.add_argument_group('target')
    target_group.add_argument('-p', '--project', dest='dir',
                              action='store', default='.', help='project dir')
    target_group.add_argument('target', nargs="+", help=TARGET_FORMAT)

    return parser.parse_args()


def main():
    home = os.path.expanduser("~")
    template_dirs = [os.path.join(
        home, ".local/share/cproject"), "/usr/local/share/cproject", "/usr/share/cproject"]

    args = parse_cmdline(template_dirs)

    if not args.template_dir is None:
        template_dirs.insert(0, args.template_dir)

    project_templates = Projects(template_dirs)
    project_addon_templates = ProjectAddons(template_dirs)
    target_templates = Targets(template_dirs)

    if args.which == 'new':  # new project
        vars = dict()
        vars['{{VERSION}}'] = args.version
        if not args.cxx_std is None:
            vars['{{CXX_STD}}'] = str(args.cxx_std)
        if not args.c_std is None:
            vars['{{C_STD}}'] = str(args.c_std)

        if args.template is None:
            projects_print(project_templates)
            args.template = input('Enter project template  {}: ')

        if args.template == '':
            sys.exit('Canceled')

        p = project_templates.get(args.template)

        addons = dict()
        if not hasattr(args, 'addon') or args.addon is None or len(args.addon) == 0:
            if not args.quiet:
                project_addons_print(p.project_type, project_addon_templates)
                addons_in = input(
                    'Enter project addon templates (separate by spaces): ').strip().split(' ')

                for addon in addons_in:
                    if len(addon) > 0:
                        addons[addon] = project_addon_templates.get(
                            p.project_type, addon)
        else:
            for addon in args.addon:
                if len(addon) > 0:
                    addons[addon] = project_addon_templates.get(
                        p.project_type, addon)

        notFound = require_not_found(p.path, addons.values())
        if len(notFound) > 0:
            sys.stdout.write(
                "Some requirements not found in selected project/addons\n")
            project_addon_with_files_print(
                p.project_type, project_addon_templates, notFound)
            sys.exit(1)

        project_dir, project_name = split_project(args.project[0])
        p.create(project_dir, project_name, vars)

        for t in addons.values():
            t.create(project_dir,
                     project_name, vars)

        if hasattr(args, 'target') and not args.target is None:
            for target in args.target:
                target_template, target_name, dir_in_project = split_target(
                    target)
                t = target_templates.get_by_type(ptype, target_template)
                t.create(project_dir, target_name,
                         dir_in_project, vars)

    elif args.which == 'addon':  # Add addon to project
        ptype = project_get_type(args.dir)

        addons = dict()
        if not hasattr(args, 'addon') or args.addon is None or len(args.addon) == 0:
            if not args.quiet:
                project_addons_print(ptype, project_addon_templates)
                addons_in = input(
                    'Enter project addon templates (separate by spaces): ').strip().split(' ')

                for addon in addons_in:
                    if len(addon) > 0:
                        addons[addon] = project_addon_templates.get(
                            ptype, addon)
        else:
            for addon in args.addon:
                if len(addon) > 0:
                    addons[addon] = project_addon_templates.get(
                        ptype, addon)

        notFound = require_not_found(args.dir, addons.values())
        if len(notFound) > 0:
            sys.stdout.write(
                "Some requirements not found in selected project/addons, choose one of addons, which provide them\n")
            project_addon_with_files_print(
                ptype, project_addon_templates, notFound)
            sys.exit(1)

        vars = CMake.load_vars(os.path.join(args.dir, CMake.SETTINGS))
        project_name = vars['{{PROJECT}}']

        for t in addons.values():
            t.create(args.dir, project_name, vars)

    elif args.which == 'target':  # Add target to project
        ptype = project_get_type(args.dir)
        for target in args.target:
            target_template, target_name, dir_in_project = split_target(target)
            t = target_templates.get_by_type(ptype, target_template)
            t.create(args.dir, target_name,
                     dir_in_project, vars)

    elif hasattr(args, 'project_type') and not args.project_type is None and len(args.project_type) > 0:
        projects_by_types_print(set(
            args.project_type),  project_templates, project_addon_templates, target_templates)
    else:
        for project in project_templates.projects():
            project_print(project,
                          project_addon_templates, target_templates)


if __name__ == "__main__":
    main()
