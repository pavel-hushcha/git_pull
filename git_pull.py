#!/usr/bin/python3

import argparse
import concurrent.futures
import pathlib
import subprocess
import sys
import time


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


def pull_git(directory: str) -> tuple[str, str]:
    process = subprocess.Popen(
        ['git', 'pull'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=directory,
        text=True,
    )
    try:
        stdout_data, stderr_data = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout_data, stderr_data = process.communicate()
    return stdout_data, stderr_data


def main() -> None:
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', action='store', type=pathlib.Path, help='The path to the folder for git pull.')
    args = parser.parse_args(sys.argv[1:])

    path = args.path or pathlib.Path.cwd()
    if not path.is_dir():
        raise parser.error('Path must be a directory.')
    git_directories = find_git_directories(path)
    if git_directories:
        results: dict[str, dict] = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}
            for directory in git_directories:
                future = executor.submit(pull_git, directory)
                futures[future] = directory

            for future in concurrent.futures.as_completed(futures):
                stdout_data, stderr_data = future.result()
                results[futures[future]] = {
                    "Success": stdout_data,
                    "Failed": stderr_data,
                }

        for number, directory in enumerate(results):
            print()
            print(f'{number + 1}. Path: {directory}')
            print(results[directory]["Success"].rstrip())
            if results[directory]["Failed"]:
                print(results[directory]["Failed"].rstrip())
    else:
        print('No GIT directories have been found.')

    print('================================================================================')
    print(f'Processed {len(git_directories)} GIT directories. Please see the details above.')
    end_time = time.time()
    duration = end_time - start_time
    print(f"Duration of execution: {duration:.2f} seconds")


if __name__ == '__main__':
    main()
