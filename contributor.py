class Contributor:
    def __init__(self, name, commits=None, files=None):
        self.name = name
        self.commits = commits if commits is not None else []
        self.files = files if files is not None else set()
