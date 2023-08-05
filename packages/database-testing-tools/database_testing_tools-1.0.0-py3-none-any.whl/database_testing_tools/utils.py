import json
import tempfile
from typing import List, Union
import sqlglot
import pydbtools as pydb
from dataengineeringutils3.s3 import read_json_from_s3
from duckdb import DuckDBPyConnection
from abc import ABC, abstractmethod


class BaseQueryEngine(ABC):
    @abstractmethod
    def run_query(self, sql):
        """
        Returns a dataframe by executing a query with the specified database engine.
        The queries written in the package were designed to work with Amazon Athena,
        which uses the Presto SQL dialect, so other implementations need to include
        a transpile step with sqlglot in order to run correctly.
        """
        pass

    def get_tables(self, db_name: str) -> List[str]:
        """ Returns a list of all tables in database """
        query = (
            "SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema = '{db_name}'"
        )
        df = self.run_query(query)
        tables = list(df["table_name"])
        return tables


class PydbQueryEngine(BaseQueryEngine):
    def run_query(self, sql, **kwargs):
        """
        Executes a query with pydbtools.read_sql_query and returns the dataframe
        """
        return pydb.read_sql_query(sql, **kwargs)


class DuckDbEngine(BaseQueryEngine):
    def __init__(self, conn: DuckDBPyConnection):
        self.conn = conn

    def run_query(self, sql, **kwargs):
        """
        Transpiles the given SQL from presto to duckdb,
        then runs the query and returns as a dataframe
        """
        query = sqlglot.transpile(sql, read="presto", write="duckdb")[0]
        return self.conn.execute(query).df()


def write_hidden_notebook_cells(in_path: str, outpath: str = None) -> str:
    """Iterate through code cells and set the metadata of the cell to hidden
    for commuter if the cell starts with "# meta.hide-input" or is tagged as
    "hide-input". Tag names are taken from jupyterbook tag notation.
    Writes the editted notebook to a specified outpath
    (or tempfile name if unspecified).

    Args:
        in_path (str): Path to existing notebook
        outpath (str, optional): File that you want to write editted notebook to.
            If unspecified it will write to tempfile name. Defaults to None.

    Returns:
        str: The path that the new notebook was written to
    """
    if outpath is None:
        outpath = next(tempfile._get_candidate_names()) + ".ipynb"

    with open(in_path) as f:
        nb = json.load(f)

    for c in nb["cells"]:
        check1 = c["cell_type"] == "code" and c.get("source", [""])[
            0
        ].strip().startswith("# meta.hide-input")

        check2 = c["cell_type"] == "code" and "hide-input" in c["metadata"].get(
            "tags", []
        )

        if check1 or check2:
            c["metadata"]["inputHidden"] = True

    with open(outpath, "w") as f:
        json.dump(nb, f)

    return outpath


def get_overall_result_from_notebook(in_path) -> Union[bool, None]:
    """
    will get the overall test results as got by the
    Tester class overall_result method from a notebook
    that tests have run in and produced outputs.
    overall_result should be the only output of a cell
    to be picked up.

    in_path:
        path to notebook that have run database-tasing-tools
        tests and contain the overall_result as an output.
        Can be a local or s3 path.
    """

    if in_path.startswith("s3://"):
        nb = read_json_from_s3(in_path)
    else:
        with open(in_path) as f:
            nb = json.load(f)

    for c in nb["cells"]:
        if "overall_result()" in "".join(c["source"]):
            overall_result_str = c["outputs"][0]["data"]["text/plain"][0]
        else:
            overall_result_str = None

    if overall_result_str == "False":
        overall_result = False
    elif overall_result_str == "True":
        overall_result = True
    else:
        overall_result = None

    return overall_result
