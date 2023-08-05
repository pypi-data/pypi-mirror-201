from slice_finder.data_connectors.data_connector import DataConnector
from abc import abstractmethod

class DataStructure:
    @abstractmethod
    def init(
        self,
        data_connector: DataConnector,
        verbose: bool,
        random_state: int | None,
    ):
        """This function will run in the __init__ of the the SliceFinder."""

        raise NotImplementedError()

    @abstractmethod
    def get_filter(self):
        """Get Filter object."""

        raise NotImplementedError()

    def get_n_filters(self, n_filters: int):
        """Get n filter objects."""
        
        return [self.get_filter() for _ in range(n_filters)]
