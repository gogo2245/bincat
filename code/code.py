from github import Github
import time
import git
import shutil
from utils import *


# Removes all content in `_working` directory
def delete_working_content(output_dir):
    shutil.rmtree(os.path.join(output_dir, '_working'))
    os.mkdir(os.path.join(output_dir, '_working'))


# prepares all needed directories
def check_required_directories(output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    if not os.path.isdir(os.path.join(output_dir, '_working')):
        os.mkdir(os.path.join(output_dir, '_working'))
    else:
        delete_working_content(output_dir)


# main function of code file
def run(config):
    # get data from config
    max_repos = config['max_repos']
    file_prefix = str(int(time.time()))
    required_bytes = config['required_bytes']
    languages_with_suffix = config['languages_with_suffix']
    output_dir = config['output_dir']

    # Open access to github
    github = Github(config['github_access_key'])

    # this dict will store remaining byte sizes for every requested language
    todo = {}

    # checks if all required directories are created
    check_required_directories(output_dir)

    # create directories for every language
    # if directory exists checks if it contains required data size
    # if not adds missing data size to todo dict
    for key in languages_with_suffix:
        check_if_dir_exists_or_create(os.path.join(output_dir, key))
        size = get_directory_size(os.path.join(output_dir, key))
        if size < required_bytes:
            todo[key] = required_bytes - size

    repos = github.get_repos()
    repo_counter = 0

    # recieves repo
    for repo in repos:
        # checks if we have all work done or if we need to work with more repos
        if repo_counter > max_repos or len(todo) == 0:
            break
        # if repo is private skip repo
        if repo.private:
            continue
        repo_counter += 1
        try:
            # get language of repo
            language = repo.language

            # if repo is written in one of missing languages we proccess it otherwise repo is skipped
            if language not in todo:
                continue

            # Repo is cloned to _working dict
            git.Repo.clone_from(repo.clone_url, os.path.join(output_dir, '_working'))
            # All files with requested suffix are moved to language dir
            move_files(os.path.join(output_dir, '_working'), os.path.join(output_dir, language),
                       file_prefix + '_' + str(repo_counter),
                       languages_with_suffix[language])
            # Repo is deleted
            delete_working_content(output_dir)

            # Missing data size is recalculated
            todo[language] = required_bytes - get_directory_size(os.path.join(output_dir, language))
            if todo[language] <= 0:
                todo.pop(language)
            print('Status: remaining:', todo)
        except:
            print('Status: skipping repo (error occurred)')

    shutil.rmtree(os.path.join(output_dir, '_working'))
