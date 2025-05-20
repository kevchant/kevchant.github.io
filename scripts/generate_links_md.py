import os
import requests

# Replace with your GitHub username or organization name
github_account = "kevchant"
# github_token = os.environ['TOKEN']

# GitHub API URL to fetch repositories
url = f"https://api.github.com/users/{github_account}/repos"
headers = {
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
# For Microsoft Fabric
def generate_azdo_microsoft_fabric_markdown(repos, output_file="azdomicrosoftfabric.md"):
    """Generate a Markdown file listing non-fork repositories with specific criteria."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Azure DevOps Repositories for Microsoft Fabric\n\n")
        filtered_repos = [
            repo for repo in repos
            if not repo.get("fork") and repo["name"].startswith("AzureDevOps") and "microsoft-fabric" in repo.get("topics", [])
        ]
        if filtered_repos:
            for repo in filtered_repos:
                name = repo["name"]
                print(f"Name: {name}")
                description = repo.get("description", "No description available")
                repo_url = repo["html_url"]
                f.write(f"- **[{name}]({repo_url})**\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No matching repositories found.\n")

def generate_gh_microsoft_fabric_markdown(repos, output_file="ghmicrosoftfabric.md"):
    """Generate a Markdown file listing non-fork repositories with specific criteria."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# GitHub Repositories for Microsoft Fabric\n\n")
        filtered_repos = [
            repo for repo in repos
            if not repo.get("fork") and repo["name"].startswith("GitHub") and "microsoft-fabric" in repo.get("topics", [])
        ]
        if filtered_repos:
            for repo in filtered_repos:
                name = repo["name"]
                print(f"Name: {name}")
                description = repo.get("description", "No description available")
                repo_url = repo["html_url"]
                f.write(f"- **[{name}]({repo_url})**\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No matching repositories found.\n")
# For SQL Server
def generate_azdo_sqlserver_markdown(repos, output_file="azdosqlserver.md"):
    """Generate a Markdown file listing non-fork repositories with specific criteria."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Azure DevOps Repositories for SQL Server\n\n")
        filtered_repos = [
            repo for repo in repos
            if not repo.get("fork") and repo["name"].startswith("AzureDevOps") and "sql-server" in repo.get("topics", [])
        ]
        if filtered_repos:
            for repo in filtered_repos:
                name = repo["name"]
                print(f"Name: {name}")
                description = repo.get("description", "No description available")
                repo_url = repo["html_url"]
                f.write(f"- **[{name}]({repo_url})**\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No matching repositories found.\n")

def generate_gh_sqlserver_markdown(repos, output_file="ghsqlserver.md"):
    """Generate a Markdown file listing non-fork repositories with specific criteria."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# GitHub Repositories for SQL Server\n\n")
        filtered_repos = [
            repo for repo in repos
            if not repo.get("fork") and repo["name"].startswith("GitHub") and "sql-server" in repo.get("topics", [])
        ]
        if filtered_repos:
            for repo in filtered_repos:
                name = repo["name"]
                print(f"Name: {name}")
                description = repo.get("description", "No description available")
                repo_url = repo["html_url"]
                f.write(f"- **[{name}]({repo_url})**\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No matching repositories found.\n")
def main():
    # Fetch all repositories
    repos = fetch_repositories(url, headers)

    # Fetch detailed information for forked repositories
    forked_repos = []
    for repo in repos:
        if repo.get("fork"):
            detailed_repo = fetch_repository_details(repo["name"], headers)
            forked_repos.append(detailed_repo)

    # Generate the Markdown files
    generate_azdo_microsoft_fabric_markdown(repos)
    generate_gh_microsoft_fabric_markdown(repos)
    generate_azdo_sqlserver_markdown(repos)
    generate_gh_sqlserver_markdown(repos)
    generate_forks_markdown(forked_repos)

if __name__ == "__main__":
    main()