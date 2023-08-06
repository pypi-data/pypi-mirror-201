"""LVA graph builder library"""
from useful_lva_sdk.core.lva_graph import LvaGraph
from useful_lva_sdk.core.operator import Operator


class LvaGraphBuilder:
    """
    LVA graph builder.

    Sample usage:
        analysis = LvaGraphBuilder("test-analysis") \
            .add_analyzer(GcsVideoSource(), "gcs_source") \
            .add_analyzer(GcsProtoSink(), "gcs_sink") \
            .add_analyzer(OccupancyCounting(), "oc") \
            .connect("oc", "gcs_sink") \
            .connect("gcs_source", "oc") \
            .build().analysis()
    """
    def __init__(self, name):
        """
        Instantiate an LVA graph builder.
        """
        self._analyzers: dict[str, Operator] = {}
        self._graph = LvaGraph(name)

    def add_analyzer(self, operator, name):
        """
        Add an analyzer to the LVA graph.

        :param operator: the operator ID
        :param name: the analyzer name

        :return: The LVA graph builder.
        :rtype: LvaGraphBuilder
        """
        if name in self._analyzers:
            raise ValueError('analyzer {name} already exists')
        self._analyzers[name] = operator
        self._graph.add_vertex(operator, name)
        return self

    def connect(self, src, dst, channel=None):
        """
        Connect two analyzers via the streaming channel s.

        :param src: the source analyzer.
        :param dst: the destination analyzer.
        :param channel: the streaming channel.
        If the ch is None, the 1st element in the src.output_args will be used.

        :return: The LVA graph builder.
        :rtype: LvaGraphBuilder
        """
        if src not in self._analyzers:
            raise ValueError(f'analyzer {src} is not defined')
        if dst not in self._analyzers:
            raise ValueError(f'analyzer {dst} is not defined')
        if channel is not None and channel not in self._analyzers[src].output_args:
            raise ValueError(f'channel {channel} is not defined by analyzer {src}')
        if channel is None and len(self._analyzers[src].output_args) != 1:
            raise ValueError(f'analyzer {src} must have exact 1 output args')
        if channel is None:
            channel = self._analyzers[src].output_args[0]
        self._graph.add_edge(src, dst, channel)
        return self

    def build(self):
        """
        Build the LVA graph.

        :return: The LVA graph.
        :rtype: lva_graph.LvaGraph
        """
        return self._graph
