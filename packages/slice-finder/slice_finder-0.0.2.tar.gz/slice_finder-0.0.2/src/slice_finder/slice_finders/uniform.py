from typing import Any, Callable

from slice_finder.slice_finders.slice_finder import SliceFinder
from slice_finder.types import Extreme


class UniformSliceFinder(SliceFinder):
    """Slice discovery using uniform sampling."""

    def find_extreme(
        self,
        metric: Callable[[Any], float],
        n_iters=300,
        n_filters=3,
        min_size=0.01,
        n_hof=1,
        maximize=False,
        maximum=float("inf"),
        minimum=float("-inf"),
    ) -> list[Extreme]:
        """Find slice with an extreme value of a metric.
        
        Args:
            metric: Function that calculates metric value over data
            n_hof: Number of extreme values to return
            n_iters: Number of iterations
            n_filters: Number of filters
            maximize: `True` will search for the maximum
            metric's value, and `False` will search for the minumum one
            min_size: Minimum size, in fractions, of the extreme subset.
            For exmaple, for value `0.01`, the extreme subset must be at
            least 1% of the data, in size, to be considered
            maximum: If `maximize`, and `maximum` is reached, the search stoppes
            minimum: If `not maximize`, and `minimum` is reached, the search stoppes
        """

        data_metric_value = metric(self.data_connector.data)
        hof = [Extreme(
            data_metric_value=data_metric_value,
            filtered_data=self.data_connector.data,
            filtered_data_metric_value=float("-inf") if maximize else float("inf"),
            filters=[],
        )]

        for _ in range(n_iters):
            filters = self.data_structure.get_n_filters(n_filters)
            filtered_data = self.data_connector.filter(filters)
            is_passing_size_threshold = (
                len(filtered_data) >= len(self.data_connector.data) * min_size
            )

            if not is_passing_size_threshold:
                continue

            filtered_data_metric_value = metric(filtered_data)

            if maximize and filtered_data_metric_value > hof[0].filtered_data_metric_value:
                hof.insert(0, Extreme(
                    data_metric_value=data_metric_value,
                    filtered_data=filtered_data,
                    filtered_data_metric_value=filtered_data_metric_value,
                    filters=filters,
                ))
                if self.verbose:
                    print(hof[0].filtered_data_metric_value, hof[0].filters)
                if filtered_data_metric_value >= maximum:
                    break
            elif not maximize and filtered_data_metric_value < hof[0].filtered_data_metric_value:
                hof.insert(0, Extreme(
                    data_metric_value=data_metric_value,
                    filtered_data=filtered_data,
                    filtered_data_metric_value=filtered_data_metric_value,
                    filters=filters,
                ))
                if self.verbose:
                    print(hof[0].filtered_data_metric_value, hof[0].filters)
                if filtered_data_metric_value <= minimum:
                    break

        return hof[:n_hof]
