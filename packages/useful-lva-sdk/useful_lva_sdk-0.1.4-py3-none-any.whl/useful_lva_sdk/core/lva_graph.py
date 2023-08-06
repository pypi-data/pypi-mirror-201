import queue

from src.useful_lva_sdk.common import Analysis
from src.useful_lva_sdk.common import AnalysisDefinition, AnalyzerDefinition


class Vertex:
    """Vertex in the LVA graph."""

    """
    Instantiate a Vertex.
    
    :param operator: The operator name.
    :param name: The analyzer name.
    """
    def __init__(self, operator, name):
        self.operator = operator
        self.name = name


class Edge:
    """Edge in the LVA graph."""

    """
    Instantiate an Edge.
    
    :param src: The source analyzer.
    :param dst: The destination analyzer.
    :param ch: The streaming channel between source and destination analyzer.
    """
    def __init__(self, src, dst, ch):
        self.src = src
        self.dst = dst
        self.ch = ch


class LvaGraph:
    """
    Instantiate an LVA graph.

    :param name: The name of the graph.
    :type name: string
    """
    def __init__(self, name):
        self.name = name
        self._vertices: dict[str, Vertex] = {}
        self._edges_in: dict[str, list[Edge]] = {}
        self._edges_out: dict[str, list[Edge]] = {}
        self._out_degrees: dict[str, int] = {}

    """
    Add a vertex to the LVA graph.
    
    :param operator: The operator name.
    :param name: The analyzer name.
    """
    def add_vertex(self, operator, name) -> None:
        self._vertices[name] = Vertex(operator, name)

    """
    Add an edge to the LVA graph.
    
    :param src: The source analyzer.
    :param dst: The destination analyzer.
    :param ch: The streaming channel between the source and destination analyzer.
    """
    def add_edge(self, src, dst, ch) -> None:
        if dst not in self._edges_in:
            self._edges_in[dst] = []
        if src not in self._edges_out:
            self._edges_out[src] = []
        if src not in self._out_degrees:
            self._out_degrees[src] = 0
        self._edges_in[dst].append(Edge(src, dst, ch))
        self._edges_out[src].append(Edge(src, dst, ch))
        self._out_degrees[src] += 1

    """
    Analysis converts the LVA graph to an Analysis resource.
    
    :return: The LVA analysis.
    :rtype: Analysis.
    """
    def analysis(self) -> Analysis:
        analyzers: list[AnalyzerDefinition] = []
        q: queue.Queue[Vertex] = queue.Queue()
        out_degrees = self._out_degrees
        for operator in self._vertices.values():
            if operator.name not in out_degrees or out_degrees[operator.name] == 0:
                q.put(operator)
        while not q.empty():
            v = q.get()
            analyzer = AnalyzerDefinition(
                analyzer=v.name,
                operator=v.operator.name,
            )
            if v.name in self._edges_in:
                for e in self._edges_in[v.name]:
                    analyzer.inputs.append(AnalyzerDefinition.StreamInput(input=f'{e.src}:{e.ch}'))
                    out_degrees[e.src] -= 1
                    if out_degrees[e.src] == 0:
                        q.put(self._vertices[e.src])
            analyzers.append(analyzer)
        return Analysis(
            name=self.name,
            analysis_definition=AnalysisDefinition(analyzers=analyzers),
            disable_event_watch=True)
