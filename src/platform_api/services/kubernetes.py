from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint



class KubernetesService:
    def __init__(self, is_mock: bool = False):
        self.is_mock = is_mock
        if not self.is_mock:
            config.load_kube_config()
            self.api_client = client.ApiClient()
            self.core_v1 = client.CoreV1Api(self.api_client)
    def get_pods(self, namespace: str = "default") -> dict[str, str]:
        """
        Get all pods in a namespace.
        
        Args:
            namespace: The namespace to query
            
        Returns:
            A dictionary mapping pod names to their status
        """
        pod_info = {}
        if self.is_mock:
            return {}
        try:
            api_response = self.core_v1.list_namespaced_pod(namespace, pretty=True)
            for pod in api_response.items:
                pod_info[pod.metadata.name] = {"status": pod.status.phase, "namespace": pod.metadata.namespace, "restart_count": pod.status.container_statuses[0].restart_count if pod.status.container_statuses else 0}
            return pod_info
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            return None

def get_k8s() -> KubernetesService:
    return KubernetesService()
