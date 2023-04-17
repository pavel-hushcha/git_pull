#!/usr/bin/python3

import argparse
import concurrent.futures
import pathlib
import subprocess
import sys


def find_git_directories(path: pathlib.Path) -> list[str | None]:
    git_directories: list[str | None] = []
    process = subprocess.Popen(
        ['git', 'rev-parse', '--show-toplevel'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=path,
        text=True,
    )
    stdout_data, stderr_data = process.communicate()
    if (git_directory := stdout_data.strip()) == path.as_posix():
        git_directories.append(git_directory)
        return git_directories
    else:
        for directory in path.glob('*/'):
            git_directories.extend(find_git_directories(directory))
        return git_directories


def pull_git(directory: str) -> None:
    process = subprocess.Popen(
        ['git', 'pull'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=directory,
        text=True,
    )
    try:
        stdout_data, stderr_data = process.communicate(timeout=10)
        print(f'Pulled git in {directory}')
        print(stdout_data, stderr_data)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout_data, stderr_data = process.communicate()
        print(stdout_data, stderr_data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action='store', type=pathlib.Path, help='The path to the folder for git pull.')
    args = parser.parse_args(sys.argv[1:])

    path = args.path or pathlib.Path.cwd()
    if not path.is_dir():
        raise parser.error('Path must be a directory.')
    git_directories = find_git_directories(path)
    if git_directories:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(pull_git, git_directories)
        print(f'Processed {len(git_directories)} GIT directories. Please see the details above.')
    else:
        print('No GIT directory has been found.')


if __name__ == '__main__':
    main()
