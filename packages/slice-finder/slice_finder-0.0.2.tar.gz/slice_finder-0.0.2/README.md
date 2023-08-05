# Slice Finder: A Framework for Slice Discovery

Slice Finder is a versatile and highly configurable framework designed for the discovery of informative, anomalous data subsets in Python, which exhibit substantially divergent metric values in comparison to the entire dataset.

Slice Finder is a crucial investigative instrument, as it enables data scientists to identify regions where their models demonstrate over- or under-performance.

## Key Characteristics
* Supports any data connector (Pandas, Polars, etc.)
* Compatible with any data structure (trees, lists, etc.)
* Allows the use of any metric (custom or from popular libraries)
* Implements multiple algorithms for slice discovery (genetic algorithms, uniform sampling, etc.)

## Installation
Install Slice Finder via pip:
```python
pip install slice_finder
```

# Quick Start
```python
import pandas as pd
from sklearn import metrics
from slice_finder import GASliceFinder, FlattenedLGBMDataStructure, PandasDataConnector

# Load data
df = pd.read_csv('your_data.csv')

# Initialize Genetic Algorithm Slice Finder with desired data connector and data structure
slice_finder = GASliceFinder(
    data_connector=PandasDataConnector(
        df=df,
        X_cols=df.drop(['pred', 'target'], axis=1).columns,
        y_col='target',
        pred_col='pred',
    ),
    data_structure=FlattenedLGBMDataStructure(),
    verbose=True,
    random_state=42,
)

# Find anomalous slice
extreme = slice_finder.find_extreme(
    metric=lambda df: metrics.mean_absolute_error(df['target'], df['pred']),
    n_filters=3,
    maximize=True,
)
extreme[0]
```

## Data Connectors
Built in:
* `PandasDataConnector` - allow you to use Pandas

Base Classes:
* `DataConnector` - Base data connector

More connectors will be added as demand grows.

You can create your custom data connector by extending the base class and implementing the necessary methods.

## Data Structures
Data quantization is challenging, and converting continuous values into discrete space is a non-trivial task. 

Built in:
* `FlattenedLGBMDataStructure` - Utilizes LightGBM decision trees to quantize and partition the data

Base classes:
* `DataStructure` - Base data structure
* `LGBMDataStructure` - Handles the fitting and partitioning the LGBM trees

More data structures will be added as demand grows.

You can create your custom data structure by extending the base classes and implementing the necessary methods.

## Slice Finders
Built in:
* `GASliceFinder` - Utilizes `eaMuPlusLambda` evolutionary algorithm to search for the most anomalous slice
* `UniformSliceFinder` - Utilizes uniform sampling out of the data structure

Base classes:
* `SliceFinder` - Base slice finder

More algorithms will be added based on demand. 

You can create your custom data structure by extending the base class and implementing the necessary methods.

## Metrics
Metrics are passed as functions to the `find_extreme` method, allowing you to use any metric or implement your custom logic.

## Neat things to implement
* Calculation parallelism
* More search algorithms. Ant colony optimization?

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome!
Clone the repo, run `poetry install` and start hacking.

## Support
For any questions, bug reports, or feature requests, please open an issue.