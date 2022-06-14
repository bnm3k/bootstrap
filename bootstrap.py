#!/usr/bin/env python3
import sys
import os
import argparse
import re
import shutil


class InvalidArgError(Exception):
    pass


class BootstrapArgs:
    def __init__(self, template: str, project_name: str, destination: str):
        self.project_name = project_name

        self.template = template
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates"
        )
        self.template_path = os.path.join(self.templates_dir, template)

        self.destination = destination
        self.dest_path = os.path.abspath(destination)
        try:
            self.__check_validity_of_args()
        except Exception as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n")
            sys.exit(1)

    def __check_validity_of_args(self):
        # get path for template to use
        if not os.path.isdir(self.template_path):
            raise InvalidArgError(
                f"Invalid template '{self.template}', resolves to path: {self.template_path}\n"
            )

        # get project name
        project_name_pattern = "^[a-z_]+$"
        if not re.match(project_name_pattern, self.project_name):
            raise InvalidArgError(
                f"Invalid project name '{self.project_name}', should match '{project_name_pattern}'\n"
            )

        # get destination
        if os.path.exists(self.dest_path):
            if os.path.isdir(self.dest_path):
                if os.listdir(self.dest_path):
                    raise InvalidArgError(
                        f"Invalid destination: '{self.dest_path}' is non-empty\n"
                    )
            else:
                raise InvalidArgError(
                    f"Invalid destination: '{self.dest_path}' exists but is not a directory'\n"
                )

        # dest path cannot be in templates dir
        if self.dest_path.startswith(self.templates_dir):
            raise InvalidArgError(
                f"Invalid destination: '{self.templates_dir}/ ... '\n"
            )


def get_args() -> BootstrapArgs:
    parser = argparse.ArgumentParser("Set up python project")
    parser.add_argument(
        "-t",
        "--template",
        metavar="<template>",
        type=str,
        nargs=1,
        help="template for use as base for setting up project",
        dest="template",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--project-name",
        metavar="<project_name>",
        type=str,
        nargs=1,
        help="project name. Must be only use lowercase and underscore characters",
        dest="project_name",
        required=True,
    )
    parser.add_argument(
        "destination",
        metavar="destination",
        type=str,
        nargs=1,
        help="destination directory path to set up project. If does not exist, it will be created, if exists, should be empty",
    )

    args = parser.parse_args()
    return BootstrapArgs(
        template=args.template[0],
        project_name=args.project_name[0],
        destination=args.destination[0],
    )


def set_up_project(dest_path, project_name):
    # rename project name module
    os.rename(
        os.path.join(dest_path, "project"),
        os.path.join(dest_path, project_name),
    )

    # TODO, there's probably a better way of doing this
    def replace_line(file_path, pattern, replacement):
        contents = []
        with open(file_path, "r") as f:
            contents = f.readlines()
        for i, line in enumerate(contents):
            if re.match(pattern, line):
                contents[i] = f"{replacement}\n"
                break
        with open(file_path, "w") as f:
            f.writelines(contents)

    # rename project in makefile
    makefile_path = os.path.join(dest_path, "Makefile")
    replace_line(
        makefile_path, r"^PROJECT_NAME:=\w*$", f"PROJECT_NAME:={project_name}\n"
    )

    # rename project in pyproject_toml
    pyproject_toml_path = os.path.join(dest_path, "pyproject.toml")
    replace_line(
        pyproject_toml_path, r"^name\s*=\s*\"\w\"\s*$", f"name = {project_name}"
    )

    # git init

    # create python virtualenv

    # poetry install

    # pre-commit install


def main():
    args = get_args()

    if not os.path.exists(args.dest_path):
        os.mkdir(args.dest_path)

    # copy template to destination
    shutil.copytree(args.template_path, args.dest_path, dirs_exist_ok=True)

    # set up project
    set_up_project(args.dest_path, args.project_name)


if __name__ == "__main__":
    main()
