from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class DeploymentRequest(BaseModel):
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    replicas: int = Field(default=1, ge=1, le=20, description="Number of replicas")
    namespace: str = Field(default="default", description="Kubernetes namespace")
    dry_run: bool = Field(default=False, description="Dry run mode")
  

class DeploymentResponse(BaseModel):
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    status: str = Field(..., description="Deployment status")
    message: str = Field(..., description="Deployment message")
    created_at: datetime = Field(default_factory=datetime.now, description="Deployment creation time")


class Deployments(BaseModel):
    deployment_request: DeploymentRequest
    deployment_response: DeploymentResponse

