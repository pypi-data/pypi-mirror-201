"""LVA client library"""
import time

from google import auth as google_auth
from google.auth.transport import grpc as google_auth_transport_grpc
from google.auth.transport import requests as google_auth_transport_requests

from useful_lva_sdk.common.lva_resources_pb2 import Analysis
from useful_lva_sdk.common.lva_service_pb2 import \
    CreateAnalysisRequest, ListAnalysesRequest, DeleteAnalysisRequest
from useful_lva_sdk.common.lva_service_pb2_grpc import LiveVideoAnalyticsStub
from useful_lva_sdk.common.operations_pb2 import Operation, GetOperationRequest
from useful_lva_sdk.common.operations_pb2_grpc import OperationsStub


def get_endpoint(env: str) -> str:
    """
    Get service endpoint based on the environment.
    """
    if env == 'autopush':
        return 'autopush-visionai.sandbox.googleapis.com'
    if env == 'staging':
        return 'staging-visionai.sandbox.googleapis.com'
    return 'visionai.googleapis.com'


class LVAClient:
    """LVA client"""

    def __init__(self, env='prod', project=None, location=None, cluster=None):
        """
        LVAClient is the gRPC client calling the LVA service.

        :param env: service environment
        :param project: the project id
        :param location: the location id
        :param cluster: the cluster id
        """
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

    def create_analysis(self, analysis_id, analysis):
        """
        Create an analysis

        :param analysis_id: the analysis id
        :param analysis: the analysis object
        """
        parent = f'projects/{self._project}/locations/{self._location}/clusters/{self._cluster}'
        metadata = [('x-goog-request-params', f'parent={parent}')]
        req = CreateAnalysisRequest(
            parent=parent,
            analysis_id=analysis_id,
            analysis=analysis,
        )
        self._wait_for_lro(self._stub.CreateAnalysis(request=req, metadata=metadata).name)

    def list_analysis(self) -> list[Analysis]:
        """
        List analyses.

        :return: List of analyses
        :rtype: list[Analysis]
        """
        parent = f'projects/{self._project}/locations/{self._location}/clusters/{self._cluster}'
        metadata = [('x-goog-request-params', f'parent={parent}')]
        req = ListAnalysesRequest(
            parent=parent
        )
        return self._stub.ListAnalyses(request=req, metadata=metadata).analyses

    def delete_analysis(self, analysis):
        """
        Delete an analysis.

        :param analysis: analysis id.
        """
        name = f'projects/{self._project}/' \
               f'locations/{self._location}/' \
               f'clusters/{self._cluster}/' \
               f'analyses/{analysis}'
        metadata = [('x-goog-request-params', f'name={name}')]
        req = DeleteAnalysisRequest(name=name)
        self._wait_for_lro(self._stub.DeleteAnalysis(request=req, metadata=metadata).name)

    def _wait_for_lro(self, op_name):
        metadata = [('x-goog-request-params', f'name={op_name}')]
        req = GetOperationRequest(name=op_name)
        while True:
            operation: Operation = self._op_stub.GetOperation(request=req, metadata=metadata)
            if not operation.done:
                time.sleep(1)
            else:
                if not operation.error:
                    raise ValueError(operation.error)
                break
