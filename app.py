import os
from fastapi import FastAPI, Request
from github import Github, Auth
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
auth = Auth.Token(os.environ.get('GH_TOKEN'))


@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    # listen for issue
    if "issue" in data:
        if data.get("action") == "opened":
            repo_name = data["repository"]["full_name"]
            issue_number = data["issue"]["number"]

            with Github(auth=auth) as gh:
                repo = gh.get_repo(repo_name)
                issue = repo.get_issue(number=issue_number)
                issue.create_comment(
                    "🚀 Terima kasih telah membuat issue! Kami akan segera meninjaunya.")

            return "Issue Opened"

        if data.get("action") == "created":

            return "Issue Created"

    return "Success"
