from fastapi import APIRouter, Depends
from ..models.deployment import DeploymentRequest, DeploymentResponse
from ..services.kubernetes import KubernetesResources, get_k8s
from ..services.github import get_github, GitHubService
router = APIRouter()

@router.post("/deployments", tags=["deployments"])
async def post_deployments(deployment_request: DeploymentRequest) -> DeploymentResponse:
    deployment_response = DeploymentResponse(
        service=deployment_request.service,
        version=deployment_request.version,
        status="pending",
        message="Deployment request received",
    )
    return deployment_response

@router.get("/deployments/namespaces/{namespace}/pods", tags=["get pods"])
async def get_pods(namespace: str, k8s: KubernetesResources = Depends(get_k8s)):
    return k8s.get_pods(namespace)

@router.get("/deployments/namespaces/{namespace}/deployments", tags=["get deployments"])
async def get_deployments(namespace: str, k8s: KubernetesResources = Depends(get_k8s)):
    return k8s.get_deployments(namespace)


@router.get("/github/{owner}/{repo}/prs", tags=["repository prs"])
async def get_prs(owner: str, repo: str, github: GitHubService = Depends(get_github)):
    return github.get_open_prs(f"{owner}/{repo}")