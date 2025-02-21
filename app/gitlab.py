from fastapi import APIRouter, Request, HTTPException
import subprocess
import os
from app.kubernetes import inject_code_into_pod

router = APIRouter()

@router.post("/webhook")
async def gitlab_webhook(request: Request):
    payload = await request.json()
    event = request.headers.get("X-Gitlab-Event")

    if event == "Push Hook":
        repo_url = payload["repository"]["git_http_url"]
        branch = payload["ref"].split("/")[-1]
        clone_directory = f"/repos/{payload['repository']['name']}"

        # Clone or pull the latest code
        if not os.path.exists(clone_directory):
            subprocess.run(["git", "clone", repo_url, clone_directory])
        else:
            subprocess.run(["git", "-C", clone_directory, "pull", "origin", branch])

        # Inject code into the pod
        user_id = payload["user"]["id"]
        inject_code_into_pod(user_id, clone_directory)

        return {"status": "success", "message": "Code updated and injected"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported event type")