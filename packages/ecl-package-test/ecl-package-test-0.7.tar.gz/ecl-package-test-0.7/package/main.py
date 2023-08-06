import os
import sys
import isort

from .src import add_import, copy_dir, main_cli, replace_code


def generate_example():
    options = main_cli()
    print(options)
    copy_dir_path = options["project_name"]
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"
    )

    copy_dir(template_path, copy_dir_path)

    # logger
    logger_path = os.path.join(copy_dir_path, "main.py")
    replacement = "logger = None"
    if options["mlops"] == "Wandb":
        replacement = "logger = Wandb()"
    else:
        replacement = "logger = Mlflow()"
    print(logger_path)
    replace_code(logger_path, "LOGGER", replacement)
    add_import(logger_path, "import torch")
    isort.file(logger_path)


def main():
    args = sys.argv[1:]
    if not len(args):
        print("Please input the options")
    if args[0] == "run":
        generate_example()
