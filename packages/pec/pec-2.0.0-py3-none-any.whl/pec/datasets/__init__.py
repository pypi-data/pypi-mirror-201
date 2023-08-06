import pkgutil as _pkgutil
from io import StringIO as _StringIO

import pandas as _pd


class DatasetLoader:
    @staticmethod
    def available():
        """List of all available datasets."""
        return ['a1', 'a2', 'a3', 's1', 's2', 's3', 's4', 'unbalanced']

    @staticmethod
    def load(name):
        """Loads a dataset by name, returning it as a Pandas DataFrame. The name of the dataset must be in available()."""
        if name not in DatasetLoader.available():
            raise RuntimeError(f'dataset name must be in {{available}}')

        csvString = str(_pkgutil.get_data(__name__, f'csv/{name}.csv').decode())
        df = _pd.read_csv(_StringIO(csvString))
        return df
