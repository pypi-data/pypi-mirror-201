from dataclasses import dataclass
import random
from typing import Any

from slice_finder.data_connectors.data_connector import DataConnector
from slice_finder.data_structures.lgbm import LGBMDataStructure, RulesTree
from slice_finder.types import Filter


@dataclass
class FlattenedRulesTreeValue:
    """
    Args:
        type: May be `continuous` or `single`
        thresholds: Set of unique thresholds
    """

    type: str  # continuous, single
    thresholds: set[str] | set[float] | set[bool]


FlattenedRulesTree = dict[str, FlattenedRulesTreeValue]


class FlattenedLGBMDataStructure(LGBMDataStructure):
    def __init__(
        self,
        task: str | None = None,
        tree_kwargs: dict[str, Any] | None = None,
        max_unique_to_categorical=200,
    ):
        """Flattened representation of an LGBM tree.
    
        Notes:
        Currenly works only as a base class for flattened LGBM.

        Args:
            task: `classification`, `regression` or None. If None, huristic
            will be applied to determine the task
            tree_kwargs: Parameters for the tree
            max_unique_to_categorical: The number of maximum unique values
            for a column to be considered as categorical
        """
        
        super().__init__(
            task=task,
            tree_kwargs=tree_kwargs,
            max_unique_to_categorical=max_unique_to_categorical,
        )
        self.flattened_rules_tree: dict[str, FlattenedRulesTreeValue] | None = None

    def init(
        self,
        data_connector: DataConnector,
        verbose=False,
        random_state: int | None = None,
    ):
        super().init(
            data_connector=data_connector,
            verbose=verbose,
            random_state=random_state,
        )
        self.set_flattened_rules_tree()

    def get_filter(self):
        feature = random.choice(sorted(list(self.flattened_rules_tree.keys())))
        tree_value = self.flattened_rules_tree[feature]
        value = random.choice(sorted(list(tree_value.thresholds)))

        if tree_value.type == "continuous":
            operator = random.choice(["<=", ">"])
        elif tree_value.type == "single":
            operator = random.choice(["=="])
        else:
            raise Exception(f"Operator {operator} not found")

        return Filter(
            feature=feature,
            operator=operator,
            value=value,
        )

    def create_flattened_rules_tree_value(self, operator: str):
        if operator == "==":
            return FlattenedRulesTreeValue(type="single", thresholds=set[str]())
        elif operator == "<=":
            return FlattenedRulesTreeValue(type="continuous", thresholds=set[float]())
        raise Exception(f"Operator {operator} does not supported")

    def set_flattened_rules_tree(self) -> FlattenedRulesTree:
        if self.flattened_rules_tree is not None:
            return self.flattened_rules_tree

        flattened_rules_tree: FlattenedRulesTree = {}

        def recurse(tree_item: RulesTree):
            feature: FlattenedRulesTreeValue = flattened_rules_tree.setdefault(
                tree_item.feature, self.create_flattened_rules_tree_value(tree_item.operator)
            )

            feature.thresholds.add(tree_item.threshold)
            if tree_item.left is not None:
                recurse(tree_item.left)
            if tree_item.right is not None:
                recurse(tree_item.right)

        for tree in self.rules_trees:
            recurse(tree)

        self.flattened_rules_tree = flattened_rules_tree

        return self.flattened_rules_tree
