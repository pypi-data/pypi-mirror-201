from abc import abstractmethod, ABC


class Operator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def output_args(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def attributes(self):
        pass


class GcsVideoSource(Operator):
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
    @property
    def name(self):
        return "OccupancyCounting"

    @property
    def output_args(self):
        return ["output_stream"]

    @property
    def attributes(self):
        return {}
