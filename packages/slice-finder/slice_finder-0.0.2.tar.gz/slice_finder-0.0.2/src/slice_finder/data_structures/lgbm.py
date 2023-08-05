from dataclasses import dataclass
from typing import Any, Optional

from lightgbm import LGBMClassifier, LGBMRegressor

from slice_finder.data_connectors.data_connector import DataConnector
from slice_finder.data_connectors.pandas import PandasDataConnector
from slice_finder.data_structures.data_structure import DataStructure


@dataclass
class RulesTree:
    feature: str
    threshold: str | float
    operator: str
    left: Optional["RulesTree"]
    right: Optional["RulesTree"]


class LGBMDataStructure(DataStructure):
    def __init__(
        self,
        task: str | None = None,
        tree_kwargs: dict[str, Any] | None = None,
        max_unique_to_categorical=200,
    ):
        """LGBM tree.

        Notes:
            Currenly works only as a base class for flattened LGBM.

        Args:
            task: `classification`, `regression` or None. If None, huristic
            will be applied to determine the task
            tree_kwargs: Parameters for the tree
            max_unique_to_categorical: The number of maximum unique values
            for a column to be considered as categorical
        """
         
        self.task = task
        self.tree: LGBMRegressor | LGBMClassifier | None = None
        self.tree_dict: dict[str, Any] | None = None
        self.rules_trees: list[RulesTree] = []
        self.tree_kwargs = tree_kwargs if tree_kwargs is not None else {}
        self.max_unique_to_categorical = max_unique_to_categorical
        if "max_cat_to_onehot" not in self.tree_kwargs:
            self.tree_kwargs["max_cat_to_onehot"] = self.max_unique_to_categorical

    def init(
        self,
        data_connector: DataConnector,
        verbose=False,
        random_state: int | None = None,
    ):
        if not isinstance(data_connector, PandasDataConnector):
            raise ValueError("LGBM currently supporst only Pandas data connector")

        self.data_connector = data_connector
        self.verbose = verbose

        if "random_state" not in self.tree_kwargs and random_state is not None:
            self.tree_kwargs["random_state"] = random_state

        self.data_connector.parse_data_for_lgbm(self.max_unique_to_categorical)
        self.fit_tree()
        self.set_rules_tree()

    def set_rules_tree(self):
        for tree_info in self.tree_dict["tree_info"]:
            rules_tree = self.set_rules_tree_internal(tree_info["tree_structure"])
            self.rules_trees.append(rules_tree)
        return self.rules_trees

    def set_rules_tree_internal(self, tree_dict: dict[str, Any]) -> RulesTree | None:
        if "leaf_index" in tree_dict:
            # If the current node is a leaf node, return the leaf value
            return None
        else:
            # If the current node is a split node, extract the split information
            split_feature = tree_dict["split_feature"]
            feature_names = self.tree_dict["feature_names"]
            feature_name = feature_names[split_feature]
            threshold = tree_dict["threshold"]
            if feature_name in self.data_connector.converted_to_categorical:
                threshold = self.data_connector.data[feature_name].cat.categories[int(threshold)]
            operator = tree_dict["decision_type"]
            left = self.set_rules_tree_internal(tree_dict["left_child"])
            right = self.set_rules_tree_internal(tree_dict["right_child"])
            return RulesTree(
                feature=feature_name,
                threshold=threshold,
                operator=operator,
                left=left,
                right=right,
            )

    def fit_tree(self) -> LGBMRegressor | LGBMClassifier:
        if self.tree is not None:
            return self.tree

        if self.task is None:
            tree_constructor = (
                LGBMRegressor if len(self.data_connector.y.value_counts()) > 30 else LGBMClassifier
            )
        elif self.task == "classification":
            tree_constructor = LGBMClassifier
        elif self.task == "regression":
            tree_constructor = LGBMRegressor
        else:
            raise Exception(f"Task {self.task} is not compatible.")

        tree = tree_constructor(**self.tree_kwargs)

        tree.fit(self.data_connector.X, self.data_connector.y)

        self.tree = tree
        self.tree_dict = self.tree.booster_.dump_model()

        return self.tree
