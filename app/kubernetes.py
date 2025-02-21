from kubernetes import client, config
import subprocess

# Load Kubernetes config
config.load_kube_config()

def inject_code_into_pod(user_id: str, repo_path: str):
    pod_name = f"{user_id}-test-pod"
    namespace = user_id

    # Copy code into the pod's shared volume
    copy_command = [
        "kubectl", "cp", repo_path, f"{namespace}/{pod_name}:/shared-volume"
    ]
    result = subprocess.run(copy_command, capture_output=True, text=True)

    if result.returncode == 0:
        return {"status": "success", "message": "Code injected into pod"}
    else:
        return {"status": "failure", "message": result.stderr}