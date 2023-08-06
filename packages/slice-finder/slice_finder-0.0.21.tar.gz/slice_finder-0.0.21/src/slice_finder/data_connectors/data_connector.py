from abc import abstractmethod, abstractproperty
from slice_finder.types import Filter

class DataConnector:
    """Base DataConnector object."""

    @abstractmethod
    def init(
        self,
        verbose: bool,
        random_state: int | None,
    ):
        """This function will run in the __init__ of the the SliceFinder."""
        raise NotImplementedError()

    @abstractmethod
    def filter(self, filters: list[Filter]):
        """Custom login to filter the data."""
        raise NotImplementedError()

    @abstractproperty
    def data(self):
        """Return the data object."""
        raise NotImplementedError()

    @abstractproperty
    def X(self):
        """X."""
        raise NotImplementedError()

    @abstractproperty
    def y(self):
        """y."""
        raise NotImplementedError()
