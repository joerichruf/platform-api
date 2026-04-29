from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.config.config_exception import ConfigException
from typing import Protocol


class KubernetesResources(Protocol):
    def get_pods(self, namespace: str = "default") -> list[dict]:
        ...
    
    def get_deployments(self, namespace: str = "default") -> list[dict]:
        ...


class KubernetesService:
    def __init__(self):
        try:
            config.load_kube_config()
        except ConfigException as e:
            raise RuntimeError(f"Invalid or missing kubeconfig: {e}")
        except FileNotFoundError:
            raise RuntimeError("kubeconfig file not found — is kubectl configured?")
        self.api_client = client.ApiClient()
        self.core_v1 = client.CoreV1Api(self.api_client)
        self.apps_v1 = client.AppsV1Api(self.api_client)
    def get_pods(self, namespace: str = "default") -> list[dict]:
        """
        Get all pods in a namespace.
        
        Args:
            namespace: The namespace to query
            
        Returns:
            A list of dictionaries containing pod information
        """
        pod_list = []
        try:
            api_response = self.core_v1.list_namespaced_pod(namespace, pretty=True)
            for pod in api_response.items:
                pod_list.append({
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "namespace": pod.metadata.namespace,
                    "restart_count": pod.status.container_statuses[0].restart_count if pod.status.container_statuses else 0
                })
            return pod_list
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            return None
    def get_deployments(self, namespace: str = "default") -> list[dict]:
        """
        Get all deployments in a namespace.
        
        Args:
            namespace: The namespace to query
            
        Returns:
            A list of dictionaries containing deployment information
        """
        deployment_list = []
        try:
            api_response = self.apps_v1.list_namespaced_deployment(namespace, pretty=True)
            for deployment in api_response.items:
                deployment_list.append({
                    "name": deployment.metadata.name,
                    "namespace": deployment.metadata.namespace,
                    "ready_replicas": deployment.status.ready_replicas or 0,
                    "replicas": deployment.status.replicas or 0
                })
            return deployment_list
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_deployment: %s\n" % e)
            return None

class FakeKubernetesService:
    def __init__(self):
        self.pods = {}
        self.deployments = {}

    def get_pods(self, namespace: str = "default") -> list[dict]:
        return self.pods.get(namespace, [])

    def get_deployments(self, namespace: str = "default") -> list[dict]:
        return self.deployments.get(namespace, [])


def get_k8s() -> KubernetesResources:
    return KubernetesService()
