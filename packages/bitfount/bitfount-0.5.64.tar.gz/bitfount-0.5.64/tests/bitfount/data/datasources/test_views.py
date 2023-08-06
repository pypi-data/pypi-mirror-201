"""Tests for view datasources."""
import datetime
from typing import List, cast
from unittest.mock import Mock, create_autospec

import pandas as pd
import pytest
from pytest import fixture

from bitfount.data.datasources.csv_source import CSVSource
from bitfount.data.datasources.views import _CSVDropColViewConfig, _DropColsCSVDataview
from bitfount.data.types import _SingleOrMulti
from tests.utils.helper import unit_test


@fixture
def dataframe() -> pd.DataFrame:
    """Simple dataframe for testing.

    Creates a simple 5-column dataframe with a bunch of different dtypes.
    """
    df = pd.DataFrame(
        {
            "int_column": [1, 2, 3],
            "float_column": [1.0, 2.0, 3.0],
            "str_column": ["1", "2", "3"],
        }
    )
    df["date"] = datetime.date(2020, 1, 1)
    df["datetime"] = datetime.datetime(2020, 1, 1, 0, 0)
    return df


@unit_test
class TestDropColsCSVDataview:
    """Tests for the _DropColsCSVDataview class."""

    @fixture
    def mock_csv_datasource(self, dataframe: pd.DataFrame) -> Mock:
        """A mock CSV Datasource instance for view testing.

        Dataframe will be preset on this mock.
        """
        mock_csv_datasource: Mock = create_autospec(CSVSource, instance=True)
        # Need to directly replace get_data to avoid issues with methodtools.lru_cache
        mock_csv_datasource.get_data = Mock(return_value=dataframe)
        return mock_csv_datasource

    @fixture
    def columns_to_drop(self) -> List[str]:
        """Columns to drop in the view."""
        return ["int_column", "date"]

    @fixture
    def dropped_cols_view(
        self, columns_to_drop: List[str], mock_csv_datasource: Mock
    ) -> _DropColsCSVDataview:
        """The view datasource with columns dropped."""
        return _DropColsCSVDataview(mock_csv_datasource, columns_to_drop)

    @pytest.mark.parametrize(
        "cols_to_drop", ("single_col", ("multiple", "cols")), ids=("single", "multiple")
    )
    def test_drop_col_view_parses_single_multi_cols(
        self, cols_to_drop: _SingleOrMulti[str], mock_csv_datasource: Mock
    ) -> None:
        """Test that class can be created with single or multiple columns."""
        drop_cols_view = _DropColsCSVDataview(mock_csv_datasource, cols_to_drop)

        # Should be converted to a list for internal storage either way
        assert isinstance(drop_cols_view._drop_cols, list)
        # Single column case:
        if isinstance(cols_to_drop, str):
            assert len(drop_cols_view._drop_cols) == 1
            assert drop_cols_view._drop_cols[0] == cols_to_drop
        # Multiple columns case:
        else:
            assert len(drop_cols_view._drop_cols) == len(cols_to_drop)
            assert drop_cols_view._drop_cols == list(cols_to_drop)

    def test_get_data(self, dropped_cols_view: _DropColsCSVDataview) -> None:
        """Test that get_data returns a dataframe with dropped columns."""
        expected_df = pd.DataFrame(
            {
                "float_column": [1.0, 2.0, 3.0],
                "str_column": ["1", "2", "3"],
            }
        )
        expected_df["datetime"] = datetime.datetime(2020, 1, 1, 0, 0)

        data = dropped_cols_view.get_data()

        assert data.equals(expected_df)

    def test_get_values(self, dropped_cols_view: _DropColsCSVDataview) -> None:
        """Test that get_values works as expected."""
        expected_values = {
            "float_column": [1.0, 2.0, 3.0],
            "str_column": ["1", "2", "3"],
            "datetime": [pd.to_datetime(datetime.datetime(2020, 1, 1, 0, 0))],
        }

        values = dropped_cols_view.get_values(
            ["float_column", "str_column", "datetime"]
        )

        # Check that these and only these columns are present
        assert expected_values.keys() == values.keys()
        for i in expected_values:
            assert list(values[i]) == expected_values[i]

    def test_get_values_dropped_column(
        self, dropped_cols_view: _DropColsCSVDataview
    ) -> None:
        """Test that error raised if get_values requests a dropped column."""
        with pytest.raises(KeyError):
            dropped_cols_view.get_values(["int_column"])

        # Check that the "dropped column" was in the underlying data
        assert "int_column" in dropped_cols_view._datasource.get_data()

    def test_get_column(self, dropped_cols_view: _DropColsCSVDataview) -> None:
        """Test that get_column works as expected."""
        expected_col = pd.Series([1.0, 2.0, 3.0])

        col = dropped_cols_view.get_column("float_column")

        assert cast(pd.Series, col).equals(expected_col)

    def test_get_column_dropped_column(
        self, dropped_cols_view: _DropColsCSVDataview
    ) -> None:
        """Test that get_column raises error if a dropped column is requested."""
        with pytest.raises(KeyError):
            dropped_cols_view.get_column("int_column")

        # Check that the "dropped column" was in the underlying data
        assert "int_column" in dropped_cols_view._datasource.get_data()

    def test_get_dtypes(
        self, columns_to_drop: List[str], dropped_cols_view: _DropColsCSVDataview
    ) -> None:
        """Test that get_dtypes works as expected."""
        dtypes = dropped_cols_view.get_dtypes()

        # Don't make assertions on actual dtypes as these may be platform dependent
        # Just want to check that dropped columns aren't present
        for i in columns_to_drop:
            assert i not in dtypes

    def test___len__(
        self, dataframe: pd.DataFrame, dropped_cols_view: _DropColsCSVDataview
    ) -> None:
        """Test that __len__ works as expected."""
        len_view = len(dropped_cols_view)

        # No rows are dropped so should be the same as the original dataframe
        # AND the same as the underlying dataframe.
        assert (
            len_view
            == 3
            == len(dataframe)
            == len(dropped_cols_view._datasource.get_data())
        )


@unit_test
class TestCSVDropColViewConfig:
    """Tests for CSVDropColViewConfig."""

    @fixture
    def mock_datasource(self) -> Mock:
        """A mock datasource."""
        mock_datasource: Mock = create_autospec(CSVSource, instance=True)
        return mock_datasource

    def test_build(self, mock_datasource: Mock) -> None:
        """Test build() method."""
        drop_cols = ["hello", "world"]
        config = _CSVDropColViewConfig(drop_cols)

        view_datasource = config.build(mock_datasource)

        assert view_datasource._drop_cols == drop_cols
