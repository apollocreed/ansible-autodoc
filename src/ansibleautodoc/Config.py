#!/usr/bin/env python3
import os
import yaml
from ansibleautodoc.Utils import Singleton


class Config:
    sample_config = """---
# autodoc.conf.yaml

# base directoy to scan, relative dir to configuration file 
# base_dir: "./" 

# documentation output directory, relative dir to configuration file.
output_dir: "./generated_doc" 

# directory containing templates, relative dir to configuration file, 
# comment to use default build in ones
template_dir: "./template" 

# template directory name within template_dir
# build in "doc_and_readme" and "minimal_readme"
template: "doc_and_readme" 

# Overwrite documentation pages if already exist
# this is equal to -y
# template_overwrite : False

# set the debug level: trace | debug | info | warn
# see -v | -vv | -vvv
# debug_level: "warn"

# when searching for yaml files in playbook projects, 
# excluded this paths (dir and files) from analysis 
# default values
excluded_playbook_dirs:
    - "host_vars"
    - "group_vars"
    - "host_secrets"
    - "plugins"
    - "autodoc.conf.yaml"
    
# when searching for yaml files in roles projects, 
# excluded this paths (dir and files) from analysis 
# default values
excluded_roles_dirs: []

"""
    # path to the documentation output dir
    output_dir = ""
    # name of the default folder for documentation out
    default_output_dir = "generated_doc"

    # project base directory
    base_dir = ""

    # current directory of this object,
    # used to get the default template directory
    script_base_dir = ""

    # path to the directory that contains the templates
    template_dir = ""
    # default template name
    default_template = "doc_and_readme"
    # template to use
    template = ""
    # flag to ask if files can be overwritten
    template_overwrite = False
    # flag to use the cli print template
    use_print_template = False

    # don't modify any file
    dry_run = False

    # default debug level
    debug_level = "warn"

    # internal flag
    is_role = None
    # internal when is_rote is True
    role_name = ""

    # name of the config file to search for
    config_file_name = "autodoc.conf.yaml"
    # if config file is not in root of project,
    # used to make output relative to config file
    _config_file_dir = ""

    #
    excluded_playbook_dirs = [
        "host_vars",
        "group_vars",
        "host_secrets",
        "plugins",
        "autodoc.config.yaml"
    ]

    excluded_roles_dirs = []

    # special Ansible tags to be removed from the tag list
    excluded_tags= [
        "always",
        "untagged",
        "never",
        "untagged",
    ]

    # annotation search patterns

    # for any pattern like ' # @annotation: [annotation_key] # description '
    # name = annotation ( without "@" )
    # allow_multiple = True allow to repeat the same annotation, i.e. @todo
    annotations = {
        "tag": {
            "name": "tag",
        },
        "author": {
            "name": "author",
        },
        "description": {
            "name": "description",
        },
        "todo":{
            "name": "todo",
            "allow_multiple":True,
        },
        "var":{
            "name": "var",
        },
        "example":{
            "name": "example",
            "regex": "(\#\ *\@example\ *\: *.*)"
        },
        "block_end":{
            "name": "block_end",
            "regex": "(\#\ *\@end\ *)"
        }
    }

    # some of the annotations defined above dont require extra code for working,
    # this is a list of them
    automatic_annotations = [
        "author",
        "description",
        "todo",
        "var",
    ]



    def __init__(self):
        self.script_base_dir = os.path.dirname(os.path.realpath(__file__))

    def get_output_dir(self):
        if self.use_print_template:
            return ""
        if self.output_dir == "":
            return os.path.realpath(self.base_dir+"/"+self.default_output_dir)
        elif os.path.isabs(self.output_dir):
            return os.path.realpath(self.output_dir)
        elif not os.path.isabs(self.output_dir):
            return os.path.realpath(self._config_file_dir+"/"+self.output_dir)

    def get_template_base_dir(self):
        if self.use_print_template:
            return os.path.realpath(self.script_base_dir+"/../templates/cliprint")

        if self.template == "":
            template = self.default_template
        else:
            template = self.template

        if self.template_dir == "":
            return os.path.realpath(self.script_base_dir+"/../templates/"+template)
        elif os.path.isabs(self.template_dir):
            return os.path.realpath(self.template_dir+"/"+template)
        elif not os.path.isabs(self.template_dir):
            return os.path.realpath(self._config_file_dir+"/"+self.template_dir+"/"+template)

    def load_config_file(self, file):

        allow_to_overwrite = [
            "base_dir",
            "output_dir",
            "template_dir",
            "template",
            "template_overwrite",
            "debug_level",
            "excluded_playbook_dirs",
            "excluded_roles_dirs",

        ]
        with open(file, 'r') as yaml_file:

            try:
                self._config_file_dir = os.path.dirname(os.path.realpath(file))
                data = yaml.load(yaml_file)
                for item_to_configure in allow_to_overwrite:
                    if item_to_configure in data.keys():
                        self.__setattr__(item_to_configure,data[item_to_configure])

            except yaml.YAMLError as exc:
                print(exc)


class SingleConfig(Config, metaclass=Singleton):
    pass

