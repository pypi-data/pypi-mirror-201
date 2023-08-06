from dataclasses import dataclass
from typing import Any


@dataclass
class Filter:
    """Filter object."""

    feature: str
    operator: str
    value: str | float | bool


@dataclass
class Extreme:
    """Extreme object."""

    data_metric_value: float
    filtered_data: Any
    filtered_data_metric_value: float
    filters: list[Filter]

    def get_prettified_view(self) -> str:
        """Replace the default behavior of `print`.

                Returns:
                    Prettified text."""

        return f"""Value of the metric on the whole dataset: {self.data_metric_value}
Value of the metric on the filtered data: {self.filtered_data_metric_value}
Filters: {self.filters}"""

    def __str__(self) -> str:
         return self.get_prettified_view()
    
    def __repr__(self) -> str:
         return self.get_prettified_view()