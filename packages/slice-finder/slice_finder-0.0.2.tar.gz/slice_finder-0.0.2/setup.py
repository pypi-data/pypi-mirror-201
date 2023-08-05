# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slice_finder',
 'slice_finder.data_connectors',
 'slice_finder.data_structures',
 'slice_finder.slice_finders']

package_data = \
{'': ['*']}

install_requires = \
['deap>=1.3,<2.0',
 'lightgbm>=3.0.0,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.5,<2.0.0']

setup_kwargs = {
    'name': 'slice-finder',
    'version': '0.0.2',
    'description': 'A Framework for Slice Discovery',
    'long_description': "# Slice Finder: A Framework for Slice Discovery\n\nSlice Finder is a versatile and highly configurable framework designed for the discovery of informative, anomalous data subsets in Python, which exhibit substantially divergent metric values in comparison to the entire dataset.\n\nSlice Finder is a crucial investigative instrument, as it enables data scientists to identify regions where their models demonstrate over- or under-performance.\n\n## Key Characteristics\n* Supports any data connector (Pandas, Polars, etc.)\n* Compatible with any data structure (trees, lists, etc.)\n* Allows the use of any metric (custom or from popular libraries)\n* Implements multiple algorithms for slice discovery (genetic algorithms, uniform sampling, etc.)\n\n## Installation\nInstall Slice Finder via pip:\n```python\npip install slice_finder\n```\n\n# Quick Start\n```python\nimport pandas as pd\nfrom sklearn import metrics\nfrom slice_finder import GASliceFinder, FlattenedLGBMDataStructure, PandasDataConnector\n\n# Load data\ndf = pd.read_csv('your_data.csv')\n\n# Initialize Genetic Algorithm Slice Finder with desired data connector and data structure\nslice_finder = GASliceFinder(\n    data_connector=PandasDataConnector(\n        df=df,\n        X_cols=df.drop(['pred', 'target'], axis=1).columns,\n        y_col='target',\n        pred_col='pred',\n    ),\n    data_structure=FlattenedLGBMDataStructure(),\n    verbose=True,\n    random_state=42,\n)\n\n# Find anomalous slice\nextreme = slice_finder.find_extreme(\n    metric=lambda df: metrics.mean_absolute_error(df['target'], df['pred']),\n    n_filters=3,\n    maximize=True,\n)\nextreme[0]\n```\n\n## Data Connectors\nBuilt in:\n* `PandasDataConnector` - allow you to use Pandas\n\nBase Classes:\n* `DataConnector` - Base data connector\n\nMore connectors will be added as demand grows.\n\nYou can create your custom data connector by extending the base class and implementing the necessary methods.\n\n## Data Structures\nData quantization is challenging, and converting continuous values into discrete space is a non-trivial task. \n\nBuilt in:\n* `FlattenedLGBMDataStructure` - Utilizes LightGBM decision trees to quantize and partition the data\n\nBase classes:\n* `DataStructure` - Base data structure\n* `LGBMDataStructure` - Handles the fitting and partitioning the LGBM trees\n\nMore data structures will be added as demand grows.\n\nYou can create your custom data structure by extending the base classes and implementing the necessary methods.\n\n## Slice Finders\nBuilt in:\n* `GASliceFinder` - Utilizes `eaMuPlusLambda` evolutionary algorithm to search for the most anomalous slice\n* `UniformSliceFinder` - Utilizes uniform sampling out of the data structure\n\nBase classes:\n* `SliceFinder` - Base slice finder\n\nMore algorithms will be added based on demand. \n\nYou can create your custom data structure by extending the base class and implementing the necessary methods.\n\n## Metrics\nMetrics are passed as functions to the `find_extreme` method, allowing you to use any metric or implement your custom logic.\n\n## Neat things to implement\n* Calculation parallelism\n* More search algorithms. Ant colony optimization?\n\n## License\nThis project is licensed under the MIT License.\n\n## Contributing\nContributions are welcome!\nClone the repo, run `poetry install` and start hacking.\n\n## Support\nFor any questions, bug reports, or feature requests, please open an issue.",
    'author': 'Igal Leikin',
    'author_email': 'igaloly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/igaloly/slice_finder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
