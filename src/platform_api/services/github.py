from ..configs.config import get_settings, Settings
from github import Github


class GitHubService:
    def __init__(self):
        """
        Initialize the GitHub service.
        """
        self.settings = get_settings()
        self.github_token = self.settings.github_token
        try:
            self.github_client = Github(self.github_token)
        except Exception as e:
            raise ValueError(f"Failed to initialize GitHub client: {e}")
        
    def get_open_prs(self, repo_name: str):
        """
        Get open pull requests for a repository.
        """
        repo = self.github_client.get_repo(repo_name)
        prs = repo.get_pulls(state="open")
        for pr in prs:
            print(pr)
        return None

def get_github() -> GitHubService:
    return GitHubService()
