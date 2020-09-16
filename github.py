import itertools
import json

from urllib import request
from contributor import Contributor


class GithubCollector:
    def __init__(self, owner, repo, token):
        self.url_prefix = f'https://api.github.com/repos/{owner}/{repo}/'
        self.headers = {'Authorization': f'token {token}'}

    def _query_json(self, options):
        req = request.Request(self.url_prefix + options, headers=self.headers)
        with request.urlopen(req) as response:
            return json.load(response)

    def _get_contributors(self, top):
        return self._query_json(f'contributors?per_page={top}')

    def _get_commits_by_author(self, author):
        result = []
        for i in itertools.count(start=1):
            page = self._query_json(f'commits?author={author}&per_page=100&page={i}')
            result += page
            if len(page) < 100:
                break
        return result

    def _get_commit_by_sha(self, sha):
        return self._query_json(f'commits/{sha}')

    def collect_commits(self, top):
        contributors_json = self._get_contributors(top)
        contributors = [Contributor(contributor['login']) for contributor in contributors_json[:top]]
        for i, contributor in enumerate(contributors):
            commits_json = self._get_commits_by_author(contributor.name)
            contributor.commits = [commit['sha'] for commit in commits_json]
            print(f'collecting commits: {(i + 1) * 100 // top}%')
        return contributors
