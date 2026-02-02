import git
from datetime import datetime, timedelta

def get_commits(repo_path='.', days=30, author=None):
    """Parse git commits from repository"""
    try:
        repo = git.Repo(repo_path)
        since_date = datetime.now() - timedelta(days=days)
        
        commits_data = []
        for commit in repo.iter_commits('HEAD', since=since_date):
            # Filter by author if specified
            if author and author.lower() not in commit.author.name.lower():
                continue
                
            commits_data.append({
                'message': commit.message.strip(),
                'author': commit.author.name,
                'date': datetime.fromtimestamp(commit.committed_date),
                'hash': commit.hexsha[:7]
            })
        
        return commits_data
    except Exception as e:
        print(f"Error reading git repo: {e}")
        return []

# Test function
if __name__ == "__main__":
    commits = get_commits(days=7)
    for c in commits[:5]:
        print(f"{c['date'].strftime('%Y-%m-%d')} - {c['message'][:50]}")
