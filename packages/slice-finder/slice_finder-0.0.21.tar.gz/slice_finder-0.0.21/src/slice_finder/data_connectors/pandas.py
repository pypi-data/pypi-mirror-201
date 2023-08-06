import pandas as pd

from slice_finder.data_connectors.data_connector import DataConnector
from slice_finder.types import Filter


class PandasDataConnector(DataConnector):
    def __init__(
        self,
        df: pd.DataFrame,
        X_cols: list[str],
        y_col: str,
        pred_col: str,
    ):
        """Data connector for using Pandas."""
        
        self.df = df
        self.X_cols = X_cols
        self.y_col = y_col
        self.pred_col = pred_col

    def init(self, verbose=False, random_state: int | None = None):
        self.verbose = verbose
        self.random_state = random_state

    def apply_filter(self, df: pd.DataFrame, filter: Filter):
        """Generate DF filter from Filter."""
        if filter.operator == "<":
            return df[filter.feature] < filter.value
        elif filter.operator == ">":
            return df[filter.feature] > filter.value
        elif filter.operator == "==":
            return df[filter.feature] == filter.value
        elif filter.operator == "!=":
            return df[filter.feature] != filter.value
        elif filter.operator == "<=":
            return df[filter.feature] <= filter.value
        elif filter.operator == ">=":
            return df[filter.feature] >= filter.value
        else:
            raise ValueError(f"Invalid operator {filter.operator}")

    def filter(self, filters: list[Filter]) -> pd.DataFrame:
        """Filters the DF."""
        df = self.df
        for filter in filters:
            df = df[self.apply_filter(df, filter)]
        return df

    def parse_data_for_lgbm(
        self,
        max_unique_to_categorical: int,
    ):
        """For LGBM to work with categorical features, the features
        must be converted to pandas Categorical type.
        This function does it.

        Args:
            max_unique_to_categorical: How many unique counts the column should have
            to be converted to categorical?
            exclude_from_df_parse: Columns not to parse.
        """
        # Important not to modify base DF
        self.df = self.df.copy()

        exclude_from_df_parse = [self.y_col, self.pred_col]

        self.converted_to_categorical = set[str]()

        for col in self.df.columns:
            value_counts = len(self.df[col].value_counts())
            is_obj = self.df[col].dtype.name == "object"
            is_already_categorical = self.df[col].dtype.name == "category"
            if (
                ((value_counts <= max_unique_to_categorical) or is_obj)
                and (col not in exclude_from_df_parse)
                and not is_already_categorical
            ):
                self.df[col] = pd.Categorical(self.df[col])
                self.converted_to_categorical.add(col)

    @property
    def data(self):
        return self.df

    @property
    def X(self):
        return self.df[self.X_cols]

    @property
    def y(self):
        return self.df[self.y_col]
