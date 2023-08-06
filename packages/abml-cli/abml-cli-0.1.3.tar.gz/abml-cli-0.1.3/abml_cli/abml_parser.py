from json import loads, dumps
import ast
import argparse
from io import open

from abml.abml_dataclass import Abml_Cae
from abml.abml_helpers import exit_handler, cprint

from yaml import load as yload
from yaml import Loader
import os

import logging

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--cae", type=str, default=None)
group.add_argument("--file", type=str, default=None)
parser.add_argument("--name", type=str, default=None)
parser.add_argument("--input_type", type=str, default="copy")
parser.add_argument("--input_folder", type=str, default="inputs")

args, _ = parser.parse_known_args()

if args.cae is not None:
    args_string = args.cae.replace("'", '"')
    cae = ast.literal_eval(dumps(loads(args.cae.replace("'", '"'), encoding="utf-8")))
elif args.file is not None:
    with open(args.file, mode="r", encoding="utf-8") as f:
        cae = yload(f, Loader=Loader)


if __name__ == "__main__":
    logger = logging.getLogger("abml_logger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(
        filename="{}.abml.log".format(args.name),
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(levelname)s - %(module)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("test")
    logger.debug("test")

    if "cae" in globals():
        cae = Abml_Cae(cae)
        exit_handler()

        cae.save_cae("{}.cae".format(args.name))

        if args.input_type == "copy":
            if not os.path.isdir(args.input_folder):
                os.mkdir(args.input_folder)
            for model in cae.models:
                if hasattr(cae.models[model], "jobs"):
                    for job in cae.models[model].jobs:
                        cae.models[model].jobs[job].write_and_copy_input_to_path(args.input_folder)

        elif args.input_type == "move":
            if not os.path.isdir(args.input_folder):
                os.mkdir(args.input_folder)
            for model in cae.models:
                if hasattr(cae.models[model], "jobs"):
                    for job in cae.models[model].jobs:
                        cae.models[model].jobs[job].write_and_move_input_to_path(args.input_folder)
