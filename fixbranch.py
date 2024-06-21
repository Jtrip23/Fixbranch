import os
import pandas as pd
from github import Github

def create_branch(username, token, repo_name, base_branch, new_branch_name):
    try:
        g = Github(username, token)
        repo = g.get_repo(f"{username}/{repo_name}")
        base_ref = repo.get_branch(base_branch)
        
        # Iterate over each new branch name and create the branch
        for branch in new_branch_name:
            new_ref = repo.create_git_ref(
                ref=f"refs/heads/{branch}",
                sha=base_ref.commit.sha
            )
            print(f"Branch '{branch}' created successfully in '{repo_name}'.")
    except Exception as e:
        print(f"Error creating branch in '{repo_name}': {e}")

def create_branches_from_excel(username, token, excel_file):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        for index, row in df.iterrows():
            repo_name = row['source_repo_name']
            
            # Fixed base branch as 'release'
            base_branch = 'main'
            
            # Fixed new branch names
            new_branch_names = ['feature_cloudhub1', 'development_cloudhub1', 'integration_cloudhub', 'release_cloudhub1', 'cloudhub']
            
            create_branch(username, token, repo_name, base_branch, new_branch_names)
    except Exception as e:
        print(f"Error reading Excel file or creating branches: {e}")

if __name__ == "__main__":
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    excel_file = 'repositories.xlsx'  # Path to your Excel file
    create_branches_from_excel(username, token, excel_file)
