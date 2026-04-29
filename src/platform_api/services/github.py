from ..configs.config import get_settings
from github import Github, GithubException


class GitHubService:
    def __init__(self):
        """
        Initialize the GitHub service.
        """
        self.settings = get_settings()
        self.github_token = self.settings.github_token
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is not set, please add it to .env")
        try:
            self.github_client = Github(self.github_token)
        except GithubException as e:
            raise ValueError(f"Failed to initialize GitHub client: {e.data.get('message', str(e))}")
        
    def get_open_prs(self, repo_name: str) -> list[dict]:
        """
        Get open pull requests for a repository.
        """
        try:
            repo = self.github_client.get_repo(repo_name)
        except GithubException as e:
            raise ValueError(f"Failed to get repository '{repo_name}'. {e.data.get('message', str(e))}")
        prs = repo.get_pulls(state="open")
        result = []
        for pr in prs:
            result.append({
                "PR_title": pr.title,
                "PR_number": pr.number,
                "PR_url": pr.html_url,
                "PR_created_at": pr.created_at.isoformat(),
                "PR_author": pr.user.login
            })
        return result

def get_github() -> GitHubService:
    return GitHubService()
