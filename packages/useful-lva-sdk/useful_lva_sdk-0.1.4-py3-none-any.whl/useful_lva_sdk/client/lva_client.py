import time

from google import auth as google_auth
from google.auth.transport import requests as google_auth_transport_requests
from google.auth.transport import grpc as google_auth_transport_grpc
from src.useful_lva_sdk.common import LiveVideoAnalyticsStub
from src.useful_lva_sdk.common.operations_pb2_grpc import OperationsStub


def get_endpoint(env: str) -> str:
    if env == 'autopush':
        return 'autopush-visionai.sandbox.googleapis.com'
    if env == 'staging':
        return 'staging-visionai.sandbox.googleapis.com'
    return 'visionai.googleapis.com'


class LVAClient:
    """
    LVAClient is the gRPC client calling the LVA service.

    :param env: service environment
    :param project: the project id
    :param location: the location id
    :param cluster: the cluster id
    """

    def __init__(self, env='prod', project=None, location=None, cluster=None):
        if project is None:
            raise ValueError('project is not specified')
        if location is None:
            raise ValueError('location is not specified')
        if cluster is None:
            raise ValueError('cluster is not specified')
        credentials, _ = google_auth.default()

        channel = google_auth_transport_grpc.secure_authorized_channel(
            credentials,
            google_auth_transport_requests.Request(),
            get_endpoint(env))
        self._stub = LiveVideoAnalyticsStub(channel)
        self._op_stub = OperationsStub(channel)
        self._project = project
        self._location = location
        self._cluster = cluster

    """
    Create an analysis
    
    :param analysis_id: the analysis id
    :param analysis: the analysis object
    """

    def create_analysis(self, analysis_id, analysis):
        parent = f'projects/{self._project}/locations/{self._location}/clusters/{self._cluster}'
        metadata = [('x-goog-request-params', f'parent={parent}')]
        req = CreateAnalysisRequest(
            parent=parent,
            analysis_id=analysis_id,
            analysis=analysis,
        )
        self._wait_for_lro(self._stub.CreateAnalysis(request=req, metadata=metadata).name)

    """
    List analyses.
    
    :return: List of analyses
    :rtype: list[Analysis]
    """

    def list_analysis(self) -> list[Analysis]:
        parent = f'projects/{self._project}/locations/{self._location}/clusters/{self._cluster}'
        metadata = [('x-goog-request-params', f'parent={parent}')]
        req = ListAnalysesRequest(
            parent=parent
        )
        return self._stub.ListAnalyses(request=req, metadata=metadata).analyses

    """
    Delete an analysis.
    
    :param analysis: the analysis name.
    """

    def delete_analysis(self, analysis):
        name = f'projects/{self._project}/locations/{self._location}/clusters/{self._cluster}/analyses/{analysis}'
        metadata = [('x-goog-request-params', f'name={name}')]
        req = DeleteAnalysisRequest(name=name)
        self._wait_for_lro(self._stub.DeleteAnalysis(request=req, metadata=metadata).name)

    def _wait_for_lro(self, op):
        metadata = [('x-goog-request-params', f'name={op}')]
        req = GetOperationRequest(name=op)
        while True:
            op: Operation = self._op_stub.GetOperation(request=req, metadata=metadata)
            if not op.done:
                time.sleep(1)
            else:
                if not op.error:
                    raise ValueError(op.error)
                break
