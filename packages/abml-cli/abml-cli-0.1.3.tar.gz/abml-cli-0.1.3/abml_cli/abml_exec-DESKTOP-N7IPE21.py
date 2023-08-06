import subprocess
import os
import atexit
import yaml
import itertools
from rich.console import Console
from datetime import datetime
import json
from copy import deepcopy
from collections import OrderedDict
from typing import Any, IO
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined

from importlib.util import module_from_spec, spec_from_file_location
import re
from inspect import getmembers, isfunction
from pandas import DataFrame, concat

from abml_cli import abml_filters
from abml_cli.abml_subroutines import Abml_Subroutine
import click
import sys


class Loader(yaml.SafeLoader):
    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def construct_yaml_types(self, node):
    seq = self.construct_sequence(node)
    if seq and isinstance(seq[0], (list, tuple)):
        return seq
    return tuple(seq)


def construct_float(loader, node):
    value = loader.construct_scalar(node)
    if not re.match(
        """^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$""",
        value,
        re.X,
    ):
        raise yaml.YAMLError("Invalid float value: %r" % value)
    return float(value.replace("_", ""))


yaml.add_constructor("tag:yaml.org,2002:seq", construct_yaml_types)
yaml.add_constructor("tag:yaml.org,2002:float", construct_float, Loader=yaml.SafeLoader)

path = os.path.dirname(os.path.abspath(__file__))

cmd_site = 'abaqus python -c "import site; print(site.getsitepackages()[0])"'
path_site = subprocess.check_output(cmd_site, encoding="utf-8", shell=True).replace("\n", "")
path_regex = r"\b[A-Z]:\\(?:[^\\\s]+\\)*[^\\\s]+\\?"
match = re.search(path_regex, path_site)
if match:
    path_site = match.group()
else:
    raise TypeError("no path found")

#!! parser = os.path.join(path_site, "lib", "site-packages", "abml", "abml_parser.py")
parser = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abml_parser.py")

console = Console()


def extract_kwargs(kwargs_str):
    # match = re.search(r"((?:\w+\=[\"\'].*?[\"\']|\w+\=-?[\d\.]+)\s*)+", kwargs_str)
    match = re.search(r"((?:\w+\=[\"\'].*?[\"\']|\w+\=-?[\d\.]+(?:[eE][-+]?[\d]+)?)\s*)+", kwargs_str)
    if match:
        kwargs_str = match.group().strip()
        kwargs = {}
        # Split the keyword argument string into individual arguments
        for kwarg in kwargs_str.split():
            key, value = kwarg.split("=")
            # Try to convert the value to a float or int, if possible
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                value = value.strip("\"'")
            kwargs[key] = value

        return kwargs
    return {}


def add_include_jinja(env, **parameters):
    def construct_include(loader: Loader, node: yaml.Node) -> Any:
        match = re.match(r"(\S+)(?:\s+\S+=\S+)*", node.value)
        file = match.group(1)
        kwargs = extract_kwargs(node.value)
        template = env.get_template(file)
        params = deepcopy(parameters)
        params.update(**kwargs)
        rendered = template.render(**params)
        extension = os.path.splitext(file)[1].lstrip(".")
        if extension in ("abml"):
            return yaml.load(rendered, Loader)
        if extension in ("json",):
            return json.load(rendered)
        return "".join(rendered)

    def construct_module(loader: Loader, node: yaml.Node):
        kwargs = loader.construct_mapping(node)
        file = kwargs.pop("file")
        template = env.get_template(file)
        params = deepcopy(parameters)
        params.update(**kwargs)
        rendered = template.render(**params)
        return yaml.load(rendered, Loader)

    yaml.add_constructor("!include", construct_include, Loader)
    yaml.add_constructor("!module", construct_module, Loader)


def render_subroutines(data, cwd=None):
    # with open(filename_render, mode="r", encoding="utf-8") as f:
    subs_dict = data.get("subroutines")

    if subs_dict is not None:
        Abml_Subroutine(subs_dict, cwd=cwd)


def abml_file_mode(file: str, parameters: dict, env: Environment, cwd=None, name=None, config={}):
    if name is None:
        filename_render = f"_{file}"
        name = file.split(".")[0]
    else:
        filename_render = f"_{name}.abml"

    parameters["abml_name"] = name

    add_include_jinja(env, **parameters)
    template = env.get_template(file)

    data = yaml.load(template.render(**parameters), Loader=Loader)

    if cwd is not None:
        render_path = os.path.abspath(os.path.join(cwd, filename_render))
        input_folder = os.path.abspath(
            os.path.join(cwd, "..", config.get("build", {}).get("inputs", {}).get("folder", "inputs"))
        )
    else:
        render_path = os.path.abspath(os.path.join(filename_render))
        input_folder = config.get("build", {}).get("inputs", {}).get("folder", "inputs")

    render_subroutines(data, cwd=cwd)

    with open(render_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=NoAliasDumper)

    params = {
        "file": render_path,
        "name": name,
        "input_type": config.get("build", {}).get("inputs", {}).get("type", "copy"),
        "input_folder": input_folder,
    }

    params_string = " ".join([f'--{key} "{val}"' for key, val in params.items()])
    cmd = f'abaqus cae noGui="{parser}" -- {params_string}'
    subprocess.call(cmd, shell=True, cwd=cwd)

    return True


def generate_param_grid(param_grid):
    if not isinstance(param_grid, dict):
        return param_grid

    keys = list(param_grid.keys())
    values = [generate_param_grid(param_grid[k]) for k in keys]
    param_combinations = itertools.product(*values)
    param_grid_list = []
    for combination in param_combinations:
        param_grid_dict = {}
        for i, key in enumerate(keys):
            param_grid_dict[key] = combination[i]
        param_grid_list.append(param_grid_dict)
    return param_grid_list


def update_nested_dict(nested_dict, update_dict):
    nested_dict = deepcopy(nested_dict)
    for key, value in update_dict.items():
        if isinstance(value, dict):
            nested_dict[key] = update_nested_dict(nested_dict.get(key, {}), value)
        else:
            nested_dict[key] = value
    return nested_dict


class Env(Environment):
    def load_filters(self, module):
        for filter_func in getmembers(module, isfunction):
            self.filters[filter_func[0]] = filter_func[1]

    def load_filters_local(self, module_path):
        console.print(module_path)
        console.print(os.listdir("."))
        spec = spec_from_file_location("custom_filters", module_path)
        if spec is not None:
            module = module_from_spec(spec)
            for filter_func in getmembers(module, isfunction):
                self.filters[filter_func[0]] = filter_func[1]


def flatten_dict(nested_dict, parent_key="", sep="_"):
    items = []
    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


@click.command()
@click.option("--files", "-f", help="abml-files", required=False, multiple=True)
def run(files=None):
    env = Env(loader=FileSystemLoader(os.getcwd()), autoescape=select_autoescape())
    env.load_filters(abml_filters)

    try:
        sys.path.append(os.getcwd())
        import _filters

        env.load_filters(_filters)
    except ImportError as e:
        console.print(e)

    listdir = os.listdir(".")
    config_yaml = filter(re.compile("_config.abml").match, listdir)

    config = {}
    for config in config_yaml:
        with open(os.path.basename("_config.abml"), mode="r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=Loader)

    parameters_yaml = filter(re.compile("_parameters.abml").match, listdir)
    parameters = {}
    for param_file in parameters_yaml:
        with open(param_file, mode="r", encoding="utf-8") as f:
            parameters.update(yaml.load(f, Loader=Loader))

    cae_reg = {
        "abml": abml_file_mode,
    }

    grid_yaml = list(filter(re.compile("_grids.abml").match, listdir))

    processed = False
    if len(grid_yaml) != 0:
        grids = {}
        for grid_file in grid_yaml:
            with open(grid_file, mode="r", encoding="utf-8") as f:
                template = env.get_template(grid_file)
                grids.update(yaml.load(template.render(**parameters), Loader=Loader))

        if files is None or files == ():
            pattern = re.compile("^(?!_).*.abml$")
            files = list(filter(pattern.match, listdir))

        for grid_name, grid in grids.items():
            parameters_list = []
            grid = generate_param_grid(grid)
            for set_ in grid:
                parameters_list.append(update_nested_dict(parameters, set_))
            grid_name = f'{grid_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            if not os.path.isdir(grid_name):
                os.mkdir(grid_name)

            indices = []
            df = DataFrame()
            for parameters_ in parameters_list:
                filename = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
                df = concat([df, DataFrame(flatten_dict(parameters_), index=[0])])
                # df = concat([df, DataFrame(flatten_dict(parameters_))], ignore_index=True)
                indices.append(filename)
                cwd = os.path.join(grid_name, filename)
                os.mkdir(cwd)
                for file in files:
                    file = os.path.basename(file)
                    extension = file.split(".")[-1]
                    processed = cae_reg.get(extension, abml_file_mode)(file, parameters_, env, cwd=cwd, name=filename)
            df.index = indices
            df.to_csv(os.path.join(grid_name, f"{grid_name}.csv"), sep=";")
    else:  # todo: cleanup
        if files is None or files == ():
            pattern = re.compile("^(?!_).*.abml$")
            files = list(filter(pattern.match, listdir))
        for file in files:
            file = os.path.basename(file)
            extension = file.split(".")[-1]
            processed = cae_reg.get(extension, abml_file_mode)(file, parameters, env, config=config)

    if processed is False:
        console.print("no abml File found!", style="bold red")


def exit_handler():
    for file in os.listdir("."):
        if ".rpy" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass
        if ".rec" in file:
            try:
                os.remove(file)
            except WindowsError:
                pass


atexit.register(exit_handler)
