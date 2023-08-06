#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2023- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

"""

# Imports from Standard Library
import os
import argparse
import json
from yamlconf import Config
from jinja2 import Environment, FileSystemLoader, meta

# Imports from Third Party Modules

# Imports from Django

# Local Imports


# Setup
class PopulateException(Exception):
    pass


class PopulateConfig(Config):
    def __init__(self, config_file, config_dir, *args, **kwargs):
        super().__init__(
            config_file=config_file, config_dir=config_dir,
            env_prefix='POPULATE_CONF'
        )


# Constants

# Data Structure Definitions

# Private Functions


# Public Classes and Functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-y', '--yaml',
        help='Full path to yaml config file containing template parameters'
    )
    parser.add_argument(
        '-j', '--json',
        help='Json file containing template parameters'
    )
    parser.add_argument(
        '-f', '--filepath',
        help='Filepath to Jinja2 template'
    )
    parser.add_argument(
        '-s', '--section',
        help='Subsection of config containing needed params'
    )
    return parser.parse_args()


def validate_filepath(filepath, filetype):
    if not os.path.exists(filepath):
        raise PopulateException(
            f'{filetype} filepath does not exist: {filepath}'
        )
    if not os.path.isfile(filepath):
        raise PopulateException(
            f'{filetype} filepath is not a file: {filepath}'
        )


def update_compiled_params(update_to, update_from):
    for k, v in update_from.items():
        if isinstance(v, dict) and k in update_to:
            update_to[k].update(v)
        else:
            update_to[k] = v


def compile_defaults(params, section=None):
    defaults = params.get('defaults', params.get('DEFAULTS')) or {}
    if section:
        section_defaults = defaults.get(section) or {}
        update_compiled_params(defaults, section_defaults)
    return defaults


def compile_secrets(params, section=None):
    secrets = params.get('secrets', params.get('SECRETS')) or {}
    defaults = secrets.get('defaults', secrets.get('DEFAULTS')) or {}
    if section:
        section_secrets = secrets.get(section) or {}
        update_compiled_params(defaults, section_secrets)
    secrets.update(defaults)
    return secrets


def compile_params(params, section=None):
    defaults = compile_defaults(params, section=section)
    secrets = compile_secrets(params, section=section)
    defaults.update(secrets)
    update_compiled_params(defaults, secrets)
    if section:
        section_params = params.get(section)
        if not section_params:
            raise PopulateException(f'{section} not a valid section name')
        update_compiled_params(defaults, section_params)
    else:
        update_compiled_params(defaults, params)
    return defaults


def get_jinja_vars(template_dir, template):
    """Returns list of jinja vars in template"""
    env = Environment(loader=FileSystemLoader(template_dir))
    template_source = env.loader.get_source(env, template)
    parsed = env.parse(template_source)
    undeclared = meta.find_undeclared_variables(parsed)
    return env, undeclared


def verified_jinja_vars(template_dir, template, kwargs):
    """
    Raises an error if the variables used in the template are not
    in kwargs. Only applies to the top level
    e.g. if a template uses foo.bar an error will be raised if foo
    is not present, but foo.bar(foo['bar']) can't be checked.
    """
    undefined = []
    jenv, undeclared = get_jinja_vars(template_dir, template)
    for var in undeclared:
        if var not in kwargs.keys():
            undefined.append(var)
    if undefined:
        msg = f"Variables not supplied: {', '.join(undefined)}"
        raise PopulateException(msg)
    return jenv


def populate_jinja2_template(template_file, params):
    template_dir, template = os.path.split(template_file)
    jenv = verified_jinja_vars(template_dir, template, params)
    text = jenv.get_template(template).render(**params)
    with open(template_file, 'w') as pop_template:
        pop_template.write(text)


def main():
    args = get_args()
    template_path = args.filepath
    validate_filepath(template_path, 'Jinja2 Template')
    json_file = args.json
    config_file = args.yaml
    section = args.section
    if config_file:
        validate_filepath(config_file, 'Yaml Config')
        path, file = os.path.split(config_file)
        config = PopulateConfig(file, path)
        params = config.config
    elif json_file:
        validate_filepath(json_file, 'JSON params')
        with open(json_file, 'r') as file:
            params = json.load(file)
    else:
        params = os.environ
        for k, v in params.items():
            params[k.lower()] = v
    params = compile_params(params, section)
    populate_jinja2_template(template_path, params)


if __name__ == '__main__':
    main()
