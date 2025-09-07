


from pydriller import Repository
import pandas as pd
import git


git.refresh(path='/usr/bin/git')  


repo = "https://github.com/apache/calcite"



bug_fix_commits = []

keywords = [
    "fix", "fixed", "fixes", "bug", "crash",
    "solves", "resolution", "resolve", "issue", "regression",
    "fall back", "assert", "coverity", "reproducible",
    "stack", "broken", "differential testing", "error",
    "hang", "test fix", "steps to reproduce", "failure",
    "leak", "stack trace", "heap overflow", "freeze",
    "problem", "overflow", "avoid", "workaround",
    "break", "stop"
]



for commit in Repository(repo).traverse_commits():
    msg = commit.msg.lower()
    if any(keyword in msg.lower() for keyword in keywords):
        bug_fix_commits.append({
            'Hash': commit.hash,
            'Message': commit.msg,
            'Hashes of parents': commit.parents,  
            'Is a merge commit?': commit.merge,
            'List of modified files': [f.filename for f in commit.modified_files]
    })

df_commits = pd.DataFrame(bug_fix_commits)
df_commits.to_csv('bug_fix_commits.csv', index=False)
print("Saving Done ")