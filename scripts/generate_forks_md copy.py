import os
import requests

# Replace with your GitHub username or organization name
github_account = "kevchant"
github_token = os.environ['TOKEN']

url = f"https://api.github.com/users/{github_account}/repos"
headers = {"Authorization": f"token {github_token}"}

response = requests.get(url, headers=headers)
repos = response.json()

forked_repos = [repo for repo in repos if repo.get("fork")]

for repo in forked_repos:
    parent = repo.get("parent", {})
    print(f"Parent information: {parent}")
    print(f"Forked Repository: {repo['html_url']}")
    print(f"Original Repository: {parent.get('html_url', 'Unknown')}")
    print(f"Owner: {parent.get('owner', {}).get('login', 'Unknown')}")
    print(f"Description: {parent.get('description', 'No description available')}")
    print("-" * 40)

# with open("forks.md", "w", encoding="utf-8") as f:
#     f.write("# Forked Repositories\n\n")
#     if forks:
#         for repo in forks:

#             name = repo["name"]
#             owner = repo["owner"]
#             desc = repo.get("description") or ""
#             url = repo["html_url"]
#             f.write(f"- {owner}-[{name}]({url}) - {desc}\n")
#     else:
#         f.write("No forked repositories found.\n")
