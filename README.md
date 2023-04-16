# Git Pull Script (uses only standard libraries)

This is a Python script for automating the `git pull` command in multiple Git repositories located within a specified folder. It recursively searches for Git repositories in subdirectories of the provided folder and performs a `git pull` operation in each repository.

## Prerequisites
- Python 3.10 or higher installed on your system
- Git installed on your system and available in your system's PATH

## Usage

```
$ python git_pull.py [-h] [-p PATH]
```

- `-h`, `--help`: Show help message and exit.
- `-p`, `--path`: Optional. Specify the path to the folder containing Git repositories for which `git pull` needs to be performed. If not provided, the current working directory will be used as the default path.

## Example

```
$ python git_pull.py -p /path/to/repositories
```

This will search for Git repositories in the specified folder (`/path/to/repositories`) and its subdirectories, and perform a `git pull` operation in each repository to fetch and merge the latest changes from the remote repository.

## Note
- If a Git repository has uncommitted changes or there are conflicts while pulling, the script will not perform the pull operation for that repository.
- The script uses the `git rev-parse` command to determine the top-level directory of a Git repository, and then performs the `git pull` operation in that directory.
- The script prints the output of `git pull` command for each repository to the console, including any error messages or conflicts encountered during the pull operation.
- The script has a timeout of 10 seconds for each `git pull` operation. If the operation exceeds this timeout, the script will forcefully terminate the process and print the output to the console.

## Disclaimer
Use this script at your own risk. It is always recommended to backup your repositories before performing any automated operations. The script may have unintended consequences or cause data loss if not used correctly. The script author is not responsible for any damages or loss incurred through the use of this script.
