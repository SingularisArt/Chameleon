#!/usr/bin/env python3

import argparse
import os
import subprocess

from path import Path
import yaml


home = Path("~").expanduser()
wall_jpg_path = home / ".config/wall.jpg"

config_dir = home / ".config/chameleon"
config_path = home / ".config/chameleon/config.yaml"


class Colors:
    HEADER = "\033[95m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"


def run_command(command_list, cwd=None, get_output=None):
    stdout = subprocess.PIPE if get_output else subprocess.DEVNULL
    stderr = subprocess.PIPE if get_output else subprocess.DEVNULL
    if isinstance(command_list, list):
        command_list = " ".join(command_list)

    if cwd == "":
        cwd = None

    p = subprocess.Popen(
        command_list,
        cwd=cwd,
        stdout=stdout,
        stderr=stderr,
        shell=True,
    )
    p.wait()

    return p.communicate()[0].decode("utf-8") if get_output else ""


def get_info_for_item(config, item):
    try:
        path = os.path.expanduser(config[item]["path"])
    except KeyError:
        path = ""

    try:
        command = config[item]["command"]
    except KeyError:
        command = ""

    return path, command


def parse_yaml(config_path):
    with open(config_path, mode="r") as file:
        file_dict = yaml.full_load(file)
        file.close()
    return file_dict


def print_status(status, program):
    end = Colors.END
    fail = Colors.FAIL
    warning = Colors.WARNING
    green = Colors.GREEN
    blue = Colors.BLUE

    if status == 0:
        print(f"{green} ⚡ {end} Themed {program}{end}")
    elif status == 1:
        print(f"{fail} X {end} {warning} Failed to theme {program}{end}")
    elif status == 2:
        print(f"{fail} X {end} {warning} User Hook {program} failed{end}")
    elif status == 3:
        print(
            f"{green} ⚡ {end} {blue} {program} User hook {end} succeeded{end}",
        )


def clear_cache():
    run_command(["rm", "-rf", "~/.cache/wal"])


def parse_args():
    parser = argparse.ArgumentParser(
        description="Chameleon Arguments",
        usage="%(prog)s -i/t [image/theme] [arguments for wal]",
    )
    parser.add_argument(
        "--theme",
        "-t",
        metavar="theme",
        type=str,
        nargs="?",
        help="a color scheme name to use as a theme",
    )
    parser.add_argument(
        "--image",
        "-i",
        metavar="image",
        type=str,
        nargs="?",
        help="an image file to use as a theme",
    )

    args = parser.parse_known_args()

    return args


def call_wal(args, walargs):
    if args.image:
        try:
            clear_cache()

            imagepath = Path(args.image)
            commandlist = ["wal", "-i", imagepath]
            commandlist.extend(walargs)

            run_command(commandlist)
            run_command(["feh", "--bg-scale", args.image])

            if args.image != wall_jpg_path:
                run_command(["cp", args.image, wall_jpg_path])
        except Exception:
            print_status(1, "pywal")
            return
    elif args.theme:
        try:
            commandlist = ["wal", "--theme", args.theme]
            commandlist.extend(walargs)
            run_command(commandlist)
        except Exception:
            print_status(1, "pywal")
            return

    print_status(0, "pywal")


def theme_program(config, name, program_name):
    try:
        path, command = get_info_for_item(config, name)

        if isinstance(command, str):
            run_command(command, cwd=path)
        elif isinstance(command, list):
            for cmd in command:
                run_command(cmd, cwd=path)
    except Exception as error:
        if config.debug:
            print(error)

        print_status(1, program_name)

        return

    print_status(0, program_name)


def main():
    config = parse_yaml(config_path)
    args, walargs = parse_args()
    call_wal(args, walargs)
    for conf in config:
        if conf != "debug":
            theme_program(config, conf, config[conf]["name"])


if __name__ == "__main__":
    main()
