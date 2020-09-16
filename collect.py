import json
import sys

from contributor import Contributor
from github import GithubCollector
from git import Repo


def save_contributors_files(contributors, filename, repo_path):
    repo = Repo(repo_path)
    contributors_cnt = len(contributors)
    for i, contributor in enumerate(contributors):
        for commit_sha in contributor.commits:
            commit = repo.commit(commit_sha)
            if len(commit.parents) != 1:
                continue
            contributor.files.update([file.a_path for file in commit.diff(commit.parents[0])])
        print(f'collecting commits: {(i + 1) * 100 // contributors_cnt}%')

    contributors_json = {contributor.name: list(contributor.files) for contributor in contributors}
    with open(filename, 'w') as fout:
        json.dump(contributors_json, fout)


def save_contributors_commits(filename, token):
    collector = GithubCollector('facebook', 'react', token)
    contributors = collector.collect_commits(50)
    contributors_json = {contributor.name: contributor.commits for contributor in contributors}
    with open(filename, 'w') as fout:
        json.dump(contributors_json, fout)


def load_contributors_commits(filename):
    with open(filename, 'r') as fin:
        return [Contributor(name, commits) for name, commits in json.load(fin).items()]


def load_contributors_files(filename):
    with open(filename, 'r') as fin:
        return [Contributor(name, files=set(files)) for name, files in json.load(fin).items()]


def print_help():
    print('usage:')
    print(f'  {sys.argv[0]} commits <output_file> <github_auth_token> -- collect all users\' commits')
    print(f'  {sys.argv[0]} files <input_file> <output_file> <path_to_local_repo> -- collect all users\' files')


def main():
    argc = len(sys.argv)
    if argc == 3 and sys.argv[1] == 'commits':
        save_contributors_commits(sys.argv[1], sys.argv[2])
    elif argc == 4 and sys.argv[1] == 'files':
        save_contributors_files(load_contributors_commits(sys.argv[1]), sys.argv[2], sys.argv[3])
    else:
        print_help()


if __name__ == '__main__':
    main()
