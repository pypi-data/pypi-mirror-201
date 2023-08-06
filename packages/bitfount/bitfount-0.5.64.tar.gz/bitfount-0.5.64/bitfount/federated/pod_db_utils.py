"""Utilities for the Pod results database."""
import hashlib
import sqlite3
from sqlite3 import Connection
from typing import List, Sequence, cast

import numpy as np
import pandas as pd
import pandas._libs.lib as lib

from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.types import DataSplit
from bitfount.federated import _get_federated_logger
from bitfount.federated.types import SerializedProtocol

logger = _get_federated_logger(__name__)

# ######## ADAPTED FROM `pandas.io.sql.py` (CAN'T BE IMPORTED) #########

# ---- SQL without SQLAlchemy ---
# sqlite-specific sql strings and handler class
# dictionary used for readability purposes
_SQL_TYPES = {
    "string": "TEXT",
    "floating": "REAL",
    "integer": "INTEGER",
    "datetime": "TIMESTAMP",
    "date": "DATE",
    "time": "TIME",
    "boolean": "INTEGER",
}


def _sql_type_name(col: pd.Series) -> str:
    """Takes a pandas column and returns the appropriate SQLite dtype."""
    # Infer type of column, while ignoring missing values.
    # Needed for inserting typed data containing NULLs, GH 8778.
    col_type = lib.infer_dtype(col, skipna=True)

    if col_type == "timedelta64":
        logger.warning(
            "the 'timedelta' type is not supported, and will be "
            "written as integer values (ns frequency) to the database.",
        )
        col_type = "integer"

    elif col_type == "datetime64":
        col_type = "datetime"

    elif col_type == "empty":
        col_type = "string"

    elif col_type == "complex":
        raise ValueError("Complex datatypes not supported")

    if col_type not in _SQL_TYPES:
        col_type = "string"

    return _SQL_TYPES[col_type]


#########################################################################


def _add_data_to_pod_db(pod_name: str, data: pd.DataFrame, table_name: str) -> None:
    """Adds the data in the provided dataframe to the pod database.

    Args:
        data: Dataframe to be added to the database.
        table-name: The table from the datasource corresponding to the data.

    Raises:
        ValueError: If there are clashing column names in the datasource
            and the pod database.
    """
    con = sqlite3.connect(f"{pod_name}.sqlite")
    cur = con.cursor()
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
    )
    con.commit()
    if "datapoint_hash" in data.columns:
        raise ValueError(
            "`datapoint_hash` not supported as column name in the datasource."
        )
    # Placeholder for the datapoint hash
    data["datapoint_hash"] = ""

    # sqlite transforms bool values to int, so we need to make sure that
    # they are the same in the df so the hashes match
    bool_cols = [col for col in data.columns if data[col].dtype == bool]
    # replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    data[bool_cols] *= 1
    # read the db data for the datasource
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    existing_data: pd.DataFrame = pd.read_sql_query(
        f'SELECT * FROM "{table_name}"', con  # nosec
    )
    existing_cols_without_index = set(
        sorted(
            [i for i in existing_data.columns if i not in ["rowID", "datapoint_hash"]]
        )
    )
    # check if df is empty or if columns all columns are the same,
    # if not all the hashes will have to be recomputed
    if (
        not existing_data.empty
        and set(sorted(data.columns)) == existing_cols_without_index
    ):
        data = pd.concat(
            [
                data,
                existing_data.drop(
                    columns=["datapoint_hash", "rowID"], errors="ignore"
                ),
            ],
            join="outer",
            ignore_index=True,
        )
        data.drop_duplicates(inplace=True)
    else:
        cur = con.cursor()
        # replace table if columns are mismatched
        cur.execute(f"DROP TABLE '{table_name}'")
        cur.execute(f"""CREATE TABLE "{table_name}" ('rowID' INTEGER PRIMARY KEY)""")
        for col in data.columns:
            cur.execute(
                f"ALTER TABLE '{table_name}' ADD COLUMN '{col}' {_sql_type_name(data[col])}"  # noqa: B950
            )

    hashed_list = []
    for _, row in data.iterrows():
        hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    data["datapoint_hash"] = hashed_list
    data.to_sql(table_name, con=con, if_exists="append", index=False)
    con.close()


def _map_task_to_hash_add_to_db(
    serialized_protocol: SerializedProtocol, task_hash: str, project_db_con: Connection
) -> None:
    """Maps the task hash to the protocol and algorithm used.

    Adds the task to the task database if it is not already present.

    Args:
        serialized_protocol: The serialized protocol used for the task.
        task_hash: The hash of the task.
        project_db_con: The connection to the database.
    """
    algorithm_ = serialized_protocol["algorithm"]
    if not isinstance(algorithm_, Sequence):
        algorithm_ = [algorithm_]
    for algorithm in algorithm_:
        if "model" in algorithm:
            algorithm["model"].pop("schema", None)
            if algorithm["model"]["class_name"] == "BitfountModelReference":
                algorithm["model"].pop("hub", None)

    cur = project_db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: B950
    )
    data = pd.read_sql("SELECT * FROM 'task_definitions' ", project_db_con)
    if task_hash not in list(data["taskhash"]):
        logger.info("Adding task to task database")
        cur.execute(
            """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: B950
            (
                task_hash,
                serialized_protocol["class_name"],
                str(algorithm_),
            ),
        )
    else:
        logger.debug("Task already in task database")
    project_db_con.commit()


def _save_results_to_db(
    project_db_con: Connection,
    datasource: BaseSource,
    results: List[np.ndarray],
    run_on_new_data_only: bool,
    pod_identifier: str,
    show_datapoints_in_results_db: bool,
    table: str,
    task_hash: str,
) -> None:
    """Saves the results to the database.

    Args:
        project_db_con: The connection to the project database.
        datasource: The datasource used for the task.
        results: The results of the task.
        run_on_new_data_only: Whether the task was run on new data only. This is
            used to determine which rows of the data should be saved to the database.
        pod_identifier: The identifier of the pod.
        show_datapoints_in_results_db: Whether to show the datapoints in the results
            database.
        table: The table to save the results to.
        task_hash: The hash of the task.
    """
    logger.info("Saving results to database")
    # Read in existing results from the relevant database table
    pod_db_con = sqlite3.connect(f"{pod_identifier.split('/')[1]}.sqlite")
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    pod_data = pd.read_sql(f'SELECT * FROM "{table}"', pod_db_con)  # nosec
    pod_db_con.close()

    # We only care about the test data since we don't log
    # anything in the database for validation or training data
    if datasource._test_idxs is None:
        if not datasource.iterable:
            raise ValueError("Datasource has no test set, cannot save results.")
        else:
            datasource = cast(FileSystemIterableSource, datasource)
            data_splitter = datasource.data_splitter or PercentageSplitter()
            filenames = data_splitter.get_filenames(datasource, DataSplit.TEST)
            run_data = datasource.data.loc[
                datasource.data["_original_filename"].isin(filenames)
            ].reset_index(drop=True)
    else:
        run_data = datasource.data.loc[datasource._test_idxs].reset_index(drop=True)

    if "datapoint_hash" in run_data.columns:
        run_data.drop("datapoint_hash", inplace=True, axis=1)

    # convert results to string
    results_as_str = [str(item) for item in results]
    # mypy_reason: This access is completely fine, the pandas stubs are overzealous
    run_data.loc[:, "results"] = results_as_str  # type: ignore[index] # Reason: see comment # noqa: B950
    columns = list(pod_data.columns)
    columns.remove("datapoint_hash")
    columns.remove("rowID")
    # get the datapoint hashes from the pod db
    data_w_hash = pd.merge(
        pod_data,
        run_data,
        how="outer",
        left_on=columns,
        right_on=columns,
        indicator=True,
    ).loc[lambda x: x["_merge"] == "both"]
    # drop the indicator and index columns
    data_w_hash.drop("_merge", inplace=True, axis=1)
    if "rowID" in data_w_hash.columns:
        data_w_hash.drop("rowID", inplace=True, axis=1)
    data_w_hash.drop_duplicates(inplace=True, keep="last")
    # Ignoring the security warning because the sql query is trusted and
    # the task_hash is calculated at __init__.
    task_data = pd.read_sql(
        f'SELECT "datapoint_hash" FROM "{task_hash}"', project_db_con  # nosec
    )
    # If this is the first time the task is run, it will not
    # have all the columns, so we need to make sure they are
    # added. Otherwise, we don't need to worry about the columns
    # as any alterations to them will be classified as a new task
    project_db_cur = project_db_con.cursor()
    if len(task_data) == 0 and show_datapoints_in_results_db:
        for col in columns:
            project_db_cur.execute(
                f"ALTER TABLE '{task_hash}' ADD COLUMN '{col}' {_sql_type_name(data_w_hash[col])}"  # noqa: B950
            )
    if run_on_new_data_only:
        # do merge and get new datapoints only
        data_w_hash = pd.merge(
            data_w_hash,
            task_data,
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        data_w_hash = data_w_hash.drop(columns=["rowID", "_merge"], errors="ignore")
        logger.info(
            f"The task was run on {len(data_w_hash)} " f"records from the datasource."
        )

    # remove existing data from the results
    existing_data_hashes = list(
        pd.read_sql(f"SELECT * FROM '{task_hash}' ", project_db_con)[  # nosec
            "datapoint_hash"
        ]
    )
    data_w_hash = data_w_hash[
        ~data_w_hash["datapoint_hash"].isin(existing_data_hashes)
    ].reset_index(drop=True)

    # save results to db
    if show_datapoints_in_results_db:
        data_w_hash.to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )
    else:
        data_w_hash[["datapoint_hash", "results"]].to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )

    logger.info("Results saved to database")
