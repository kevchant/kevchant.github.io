import os
import requests

# Replace with your GitHub username or organization name
github_account = "kevchant"
github_token = os.environ['TOKEN']

# GitHub API URL to fetch repositories
url = f"https://api.github.com/users/{github_account}/repos"
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_repositories(api_url, headers):
    """Fetch all repositories for the given GitHub account."""
    repos = []
    while api_url:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        repos.extend(response.json())
        # Check for pagination
        api_url = response.links.get('next', {}).get('url')
    return repos

def fetch_repository_details(repo_name, headers):
    """Fetch detailed information for a specific repository."""
    repo_url = f"https://api.github.com/repos/{github_account}/{repo_name}"
    response = requests.get(repo_url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def generate_forks_markdown(forked_repos, output_file="forks.md"):
    """Generate a Markdown file listing forked repositories and their originals."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Forked Repositories\n\n")
        if forked_repos:
            for repo in forked_repos:
                name = repo["name"]
                description = repo.get("description", "No description available")
                fork_url = repo["html_url"]
                parent = repo.get("parent", {})

                original_url = parent.get("html_url", "Unknown")
                original_owner = parent.get("owner", {}).get("login", "Unknown")

                f.write(f"- **[{name}]({fork_url})**\n")
                f.write(f"  - **Original Repository**: [{original_url}]({original_url})\n")
                f.write(f"  - **Original Owner**: {original_owner}\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No forked repositories found.\n")

def main():
    # Fetch all repositories
    repos = fetch_repositories(url, headers)

    # Fetch detailed information for forked repositories
    forked_repos = []
    for repo in repos:
        if repo.get("fork"):
            detailed_repo = fetch_repository_details(repo["name"], headers)
            forked_repos.append(detailed_repo)

    # Generate the Markdown file
    generate_forks_markdown(forked_repos)

if __name__ == "__main__":
    main()