from src.useful_lva_sdk.core.lva_graph import LvaGraph
from src.useful_lva_sdk.core.operator import Operator


class LvaGraphBuilder:
    """
    Instantiate an LVA graph builder.
    """
    def __init__(self, name):
        self._analyzers: dict[str, Operator] = {}
        self._graph = LvaGraph(name)

    """
    Add an analyzer to the LVA graph.
    
    :param operator: the operator ID
    :param name: the analyzer name
    
    :return: The LVA graph builder.
    :rtype: LvaGraphBuilder
    """
    def add_analyzer(self, operator, name):
        if name in self._analyzers:
            raise ValueError('analyzer {name} already exists')
        self._analyzers[name] = operator
        self._graph.add_vertex(operator, name)
        return self

    """
    Connect two analyzers via the streaming channel s.
    
    :param src: the source analyzer.
    :param dst: the destination analyzer.
    :param ch: the streaming channel. If the ch is None, the 1st element in the src.output_args will be used.
    
    :return: The LVA graph builder.
    :rtype: LvaGraphBuilder
    """
    def connect(self, src, dst, ch=None):
        if src not in self._analyzers:
            raise ValueError(f'analyzer {src} is not defined')
        if dst not in self._analyzers:
            raise ValueError(f'analyzer {dst} is not defined')
        if ch is not None and ch not in self._analyzers[src].output_args:
            raise ValueError(f'channel {ch} is not defined by analyzer {src}')
        if ch is None and len(self._analyzers[src].output_args) != 1:
            raise ValueError(f'analyzer {src} must have exact 1 output args')
        else:
            ch = self._analyzers[src].output_args[0]
        self._graph.add_edge(src, dst, ch)
        return self

    """
    Build the LVA graph.
    
    :return: The LVA graph.
    :rtype: lva_graph.LvaGraph
    """
    def build(self):
        return self._graph
