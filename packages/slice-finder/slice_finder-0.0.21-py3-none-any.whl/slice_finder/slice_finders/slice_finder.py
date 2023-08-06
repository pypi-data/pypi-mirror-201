import random
import numpy as np

from slice_finder.data_connectors.data_connector import DataConnector
from slice_finder.data_structures.data_structure import DataStructure

from abc import abstractmethod


class SliceFinder:
    def __init__(
        self,
        data_connector: DataConnector,
        data_structure: DataStructure,
        verbose=False,
        random_state: int | None = None,
    ):
        random.seed(random_state)
        np.random.seed(random_state)

        self.verbose = verbose

        self.data_connector = data_connector
        self.data_connector.init(
            verbose=verbose,
            random_state=random_state,
        )

        self.data_structure = data_structure
        self.data_structure.init(
            data_connector=self.data_connector,
            verbose=verbose,
            random_state=random_state,
        )

    @abstractmethod
    def find_extreme(self, *args, **kwargs):
        raise NotImplementedError()
