"""Operator registry that includes all supported operators."""
from abc import abstractmethod, ABC


class Operator(ABC):
    """Base operator class"""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the operator
        """

    @property
    @abstractmethod
    def output_args(self) -> list[str]:
        """
        Output arguments of the operator
        """

    @property
    @abstractmethod
    def attributes(self):
        """
        Attributes of the operator
        """


class GcsVideoSource(Operator):
    """GCS video source operator"""
    @property
    def name(self):
        return "GcsSource"

    @property
    def output_args(self):
        return ["output_stream"]

    @property
    def attributes(self):
        return {}


class GcsProtoSink(Operator):
    """GCS proto sink operator"""
    @property
    def name(self):
        return "GcsProtoSink"

    @property
    def output_args(self):
        return []

    @property
    def attributes(self):
        return {}


class OccupancyCounting(Operator):
    """Occupancy counting operator"""
    @property
    def name(self):
        return "OccupancyCounting"

    @property
    def output_args(self):
        return ["output_stream"]

    @property
    def attributes(self):
        return {}
