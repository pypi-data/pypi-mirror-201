"""Support for different "views" over existing datasets.

These allow constraining the usable data that is exposed to a modeller, or only
presenting a transformed view to the modeller rather than the raw underlying data.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterable, List, TypeVar, Union

import methodtools
import numpy as np
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.csv_source import CSVSource
from bitfount.data.types import _SingleOrMulti
from bitfount.types import _Dtypes


# NOTE: These classes are only temporary creations until we develop a fuller,
#       transformation-enabled view capability.
#
#       They should not be released as part of the public API.
class _DataView(BaseSource, ABC):
    def __init__(self, datasource: BaseSource) -> None:
        super().__init__()
        self._datasource = datasource


# See above comment
class _DropColsCSVDataview(_DataView):
    """A data view that presents CSV data with columns removed."""

    _datasource: CSVSource

    def __init__(self, datasource: CSVSource, drop_cols: _SingleOrMulti[str]) -> None:
        super().__init__(datasource)
        self._drop_cols: List[str] = (
            [drop_cols] if isinstance(drop_cols, str) else list(drop_cols)
        )

    # TODO: [BIT-1780] Simplify referencing data in here and in other sources
    #       We want to avoid recalculating but we don't want to cache more
    #       than one result at a time to save memory
    @methodtools.lru_cache(maxsize=1)
    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from underlying CSV dataset.

        Will handle drop columns specified in view.

        Returns:
            A DataFrame-type object which contains the data.
        """
        csv_df: pd.DataFrame = self._datasource.get_data(**kwargs)
        # Ensure we return a copy of the dataframe rather than mutating the original
        drop_csv_df = csv_df.drop(columns=self._drop_cols)
        return drop_csv_df

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in CSV dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.get_data(**kwargs)[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from CSV dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        csv_df: pd.DataFrame = self.get_data(**kwargs)
        return csv_df[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the CSV dataset.

        Returns:
            A mapping from column names to column types.
        """
        csv_df: pd.DataFrame = self.get_data(**kwargs)
        return self._get_data_dtypes(csv_df)

    def __len__(self) -> int:
        return len(self.get_data())


_DS = TypeVar("_DS", bound=BaseSource)


class _ViewDatasourceConfig(ABC, Generic[_DS]):
    """A class dictating the configuration of a view."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def build(self, underlying_datasource: _DS) -> _DataView:
        """Build a view instance corresponding to this config."""


class _CSVDropColViewConfig(_ViewDatasourceConfig[CSVSource]):
    """Config class for _DropColsCSVDropColView."""

    def __init__(
        self, drop_cols: _SingleOrMulti[str], *args: Any, **kwargs: Any
    ) -> None:
        self._drop_cols: List[str] = (
            [drop_cols] if isinstance(drop_cols, str) else list(drop_cols)
        )

    def build(self, underlying_datasource: CSVSource) -> _DropColsCSVDataview:
        """Build a _DropColsCSVDropColView from this configuration."""
        return _DropColsCSVDataview(underlying_datasource, self._drop_cols)
