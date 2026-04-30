from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from ..models.deployment import DeploymentRequest, DeploymentResponse
from ..services.kubernetes import KubernetesResources, get_k8s
from ..services.github import get_github, GitHubService
import uuid
from datetime import datetime
from time import sleep
router = APIRouter()

jobs: dict = {}
def create_job(service: str) -> dict:
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "service": service,
        "status": "pending",
        "message": "Job created",
        "created_at": datetime.now().isoformat(),
        "finished_at": None,
        "error": None
    }
    jobs[job_id] = job
    return job

@router.post("/deployments", tags=["deployments"])
async def post_deployments(deployment_request: DeploymentRequest) -> DeploymentResponse:
    deployment_response = DeploymentResponse(
        service=deployment_request.service,
        version=deployment_request.version,
        status="pending",
        message="Deployment request received",
    )
    return deployment_response

@router.post("/deployments/{service}/deploy", tags=["deployments"])
async def post_deploy(
    service: str,
    repo: str,
    ref: str,
    background_tasks: BackgroundTasks,
    version: str = "latest",
    workflow_id: str = "269032094",
    github: GitHubService = Depends(get_github)
) -> dict:
    job = create_job(service)
    background_tasks.add_task(run_deployment, job["id"], repo, ref, github, workflow_id, {"service": service, "version": version})
    return {"job_id": job["id"], "status": "queued"}

def run_deployment(job_id: str, repo: str, ref: str, github: GitHubService, workflow_id: str, inputs: dict):
    jobs[job_id]["status"] = "running"
    try:
        github.trigger_workflow_run(repo, workflow_id, ref, inputs)
        sleep(4)
        while True:
            status, conclusion = github.get_workflow_run_status(repo, workflow_id)
            if status == "completed":
                break
            sleep(2)
        if conclusion != "success":
            raise ValueError(f"Workflow failed: {conclusion}")
        jobs[job_id]["status"] = "complete"
        jobs[job_id]["finished_at"] = datetime.now().isoformat()
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@router.get("/deployments/namespaces/{namespace}/pods", tags=["get pods"])
async def get_pods(namespace: str, k8s: KubernetesResources = Depends(get_k8s)):
    return k8s.get_pods(namespace)

@router.get("/deployments/namespaces/{namespace}/deployments", tags=["get deployments"])
async def get_deployments(namespace: str, k8s: KubernetesResources = Depends(get_k8s)):
    return k8s.get_deployments(namespace)

@router.get("/jobs", tags=["get jobs"])
async def get_job():
    return list(jobs.values())

@router.get("/github/{owner}/{repo}/prs", tags=["repository prs"])
async def get_prs(owner: str, repo: str, github: GitHubService = Depends(get_github)):
    return github.get_open_prs(f"{owner}/{repo}")