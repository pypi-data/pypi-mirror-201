from typing import List, Dict, Union, Callable
from copy import deepcopy
from IPython.display import Markdown
import pandas as pd
from datetime import date, timedelta, datetime
import altair as alt
import numpy as np
from database_testing_tools.utils import PydbQueryEngine


def _get_status_description(passed=None, critical_failure=None):

    if passed is None:
        status = "no test ran"
    elif passed:
        status = "passed"
    elif critical_failure in [None, True]:
        status = "failed"
    else:
        status = "non-critical"

    return status


def _get_blank_result(
    name=None, passed=None, critical_failure=None, result_details=None
):
    if result_details is None:
        result_details = {}

    blank_result = {
        "name": name,
        "passed": passed,
        "param_critical_failure": critical_failure,
        "status": _get_status_description(passed, critical_failure),
        "result_details": result_details,
    }
    return blank_result


class Tester:
    def __init__(
        self,
        snapshot_column_name="mojap_snapshot_date",
        scd2_start_column_name="mojap_start_datetime",
        scd2_end_column_name="mojap_end_datetime",
        query_engine=PydbQueryEngine(),
    ):
        self.all_results = []
        self.snapshot_column_name = snapshot_column_name
        self.scd2_start_column_name = scd2_start_column_name
        self.scd2_end_column_name = scd2_end_column_name
        self.qe = query_engine

    def _update_results(self, results: Union[List, Dict]):

        if isinstance(results, dict):
            results = [results]

        self.all_results.extend(deepcopy(results))

    def overall_result(self) -> bool:
        """
        returns bool depending on status of all tests ran.
        If any test has failed where critical_failure=True
        then overall_result returns passed=False
        """
        passed = all(
            [
                r.get("passed", True)
                for r in self.all_results
                if r.get("param_critical_failure")
            ]
        )
        return passed

    def plot(
        self,
        df,
        plot_type="line",
        x="date",
        y="count",
        color="table",
        column="table",
        point=False,
        tooltip=[],
    ):
        """
        Generic line or bar chart plotting function

        df: pandas dataframe. If not other args are given this must have
            columns "date", "count" and "table"
        plot_type: 'bar' or 'line'
        x: column to show on x-axis (default 'date')
        y: column to show on y-axis (default 'count')
        color: column to group by (default 'table')
        column: bar chart only, column to group by
        point: line chart only, mark points
        tooltip: list of columns to show on tooltip on mouse hover

        Returns: Altair Chart
        """
        if plot_type == "line":
            c = (
                alt.Chart(df)
                .mark_line(point=point)
                .encode(x=x, y=y, color=color, tooltip=tooltip)
            )

        elif plot_type == "bar":
            c = (
                alt.Chart(df)
                .mark_bar()
                .encode(x=x, y=y, color=color, column=column, tooltip=tooltip)
            )

        else:

            raise ValueError(
                f"Only support plot_type of 'line' or 'bar' given {plot_type}"
            )

        if tooltip:
            c = c.interactive()

        return c

    def row_counts_snapshot(
        self,
        db_name,
        tables,
        first_snapshot,
        plot=None,
        **kwargs,
    ):

        dfs = pd.DataFrame()
        for table in tables:
            sql = f"""select {self.snapshot_column_name} as date, count(*) as count
            from {db_name}.{table}
            where {self.snapshot_column_name} >= date '{first_snapshot}'
            group by {self.snapshot_column_name}"""

            df = self.qe.run_query(sql)

            df["table"] = table

            dfs = pd.concat([df, dfs])

        dfs["date"] = dfs["date"].apply(str)
        if plot == "line" or plot == "bar":
            return self.plot(dfs, plot_type=plot, **kwargs)
        return dfs

    def row_counts_scd2(
        self,
        db_name,
        tables,
        start_date,
        increment=28,
        plot=None,
        **kwargs,
    ):

        today = date.today()

        start_date_strp = datetime.strptime(start_date, "%Y-%m-%d").date()

        increment = timedelta(days=increment)

        counts = []
        for table in tables:
            start_date_strp = datetime.strptime(start_date, "%Y-%m-%d").date()
            while start_date_strp <= today:
                start_date_cp = str(start_date_strp)
                sql = f"""select count(*) as count
                from {db_name}.{table}
                where {self.scd2_start_column_name} <=  date '{start_date_cp}'
                and {self.scd2_end_column_name} > date '{start_date_cp}'"""

                tmp = self.qe.run_query(sql)

                counts.append(
                    {"date": start_date_cp, "count": tmp.iloc[0, 0], "table": table}
                )
                start_date_strp += increment

        df = pd.DataFrame.from_dict(counts)
        if plot == "line" or plot == "bar":
            return self.plot(df, plot_type=plot, **kwargs)
        return df

    def check_all_tables_return_data(
        self,
        db_name: str,
        tables: list = None,
        critical_failure: Union[bool, dict] = True,
        only_list_failed_tables: bool = False,
        snapshot_date: str = None,
        where_statement: str = None,
        ctas_approach: dict = None,
    ):
        """
        tests whether tables return any data, fails if no data in table.
        can be set for a snapshot date or some other conditions as
        specified in the where_statement parameter.

        db_name:
            name of database to test.
        tables:
            optional list of table names to test. Tests all tables
            if omitted
        critical_failure:
            whether the test failure is considered critical. You can
            use a dict with {table_name: bool} to vary critical failures
            on a table by table basis.
        only_list_failed_tables:
            if set to True will only show failures in the returned
            result
        snapshot_date:
            the snapshot date to test for data. If set do not set
            where_statement
        where_statement:
            if set instead of snapshot_date this will be condition used
            for the test of all tables.
        ctas_approach:
            if you have one or more tables that contain nested datatypes,
            this should be used.

            e.g. for complex_table1 and complex_table2 you would pass:

                {complex_table1: True, complex_table2: True}

            All other tables will default to ctas_approach=False
            if not defined in the dict.

        """

        if snapshot_date is not None and where_statement is not None:
            raise ValueError(
                "Can only set one of the parameters: snapshot_date "
                "or where_statement not both."
            )
        elif snapshot_date:
            where_statement = (
                f"WHERE {self.snapshot_column_name} = date '{snapshot_date}'"
            )
        else:
            if where_statement is None:
                where_statement = ""
            else:
                if not where_statement.lower().startswith("where"):
                    raise ValueError("`where_statement` must start with 'where'")

        if tables is None:
            tables = self.qe.get_tables(db_name)
        elif isinstance(tables, str):
            tables = [tables]
        else:
            if not isinstance(tables, list):
                err_str = f"Expected tables as type str or list got type {type(tables)}"
                raise ValueError(err_str)

        if ctas_approach is None:
            ctas_approach = {}

        ctas_not_passed = {t: False for t in tables if t not in ctas_approach.keys()}

        ctas_approaches = dict(ctas_not_passed, **ctas_approach)

        markdown = "| Table Name | Passed Check | Error Details |\n"
        markdown += "|---|---|---|\n"
        all_results = []
        for table in tables:
            sql = f"SELECT * FROM {db_name}.{table} {where_statement} LIMIT 10"
            try:
                tab_len = len(
                    self.qe.run_query(
                        sql,
                        ctas_approach=ctas_approaches[table],
                    )
                )
                str_e = "n/a"
            except Exception as e:
                tab_len = 0
                str_e = str(e)
            passed = tab_len > 0
            test_name = f"check_all_tables_return_data.{db_name}.{table}"

            if isinstance(critical_failure, dict):
                cf = critical_failure[table]
            else:
                cf = critical_failure

            res = _get_blank_result(name=test_name, passed=passed, critical_failure=cf)
            all_results.append(res)

            if passed and only_list_failed_tables:
                pass
            else:
                passed_emoji = "✅" if passed else "❌"
                if not passed and str_e == "n/a":
                    str_e = "Query returned with 0 rows"
                markdown += f"| {table} | {passed_emoji} | {str_e} |\n"

        self._update_results(all_results)
        return {"output": Markdown(markdown), "results": all_results}

    def count_deletions_between_snapshots(
        self,
        db_name: str,
        tables: Union[str, list],
        primary_keys: dict,
        from_snapshot,
        to_snapshot,
        critical_failure,
        only_list_failed_tables=False,
    ):

        all_results = []
        markdown = "| Table Name | Passed Check | Error Details |\n"
        markdown += "|---|---|---|\n"

        if isinstance(tables, str):
            tables = [tables]

        details = "N/A"

        for table in tables:

            """Any pks in earlier snapshot that aren't in later snapshot?"""
            # First, check the given snapshots exist for the table
            distinct_snapshots_query = f"""
                select distinct {self.snapshot_column_name}
                from {db_name}.{table}
                """

            df_distinct_snapshots = self.qe.run_query(
                distinct_snapshots_query,
            )
            distinct_snapshots = [
                d.strftime("%Y-%m-%d")
                for d in df_distinct_snapshots[self.snapshot_column_name]
            ]

            if not set([from_snapshot, to_snapshot]).issubset(distinct_snapshots):
                details = (
                    f"Table {table} does not have both the given snapshots: "
                    f"{from_snapshot}, {to_snapshot}."
                )
                test_name = f"count_deletions_between_snapshots.{db_name}.{table}"
                passed = False
                res = _get_blank_result(
                    name=test_name,
                    passed=passed,
                    critical_failure=critical_failure,
                    result_details=details,
                )
                all_results.append(res)

            else:
                pk = primary_keys[table]
                query = (
                    f"select count(*) count\n"
                    f"from {db_name}.{table} t\n"
                    f"where {self.snapshot_column_name} = date '{from_snapshot}'\n"
                    "and not exists (\n"
                    f"select *\n"
                    f"from {db_name}.{table}\n"
                    f"where {pk[0]} = t.{pk[0]}\n"
                )

                for column in pk[1:]:
                    query += f"and {column} = t.{column}\n"

                query += (
                    f"and {self.snapshot_column_name} = date '{to_snapshot}'\n" ")\n"
                )

                df = self.qe.run_query(query)
                if len(df.index) > 0:
                    count = int(df.iloc[0, 0])
                else:
                    count = 0
                test_name = f"count_deletions_between_snapshots.{db_name}.{table}"
                passed = count == 0
                details = (
                    f"Table '{table}': {count} deletions between {from_snapshot} "
                    f"and {to_snapshot}"
                )
                res = _get_blank_result(
                    name=test_name,
                    passed=passed,
                    critical_failure=critical_failure,
                    result_details=details,
                )

                all_results.append(res)

            if passed and only_list_failed_tables:
                pass
            else:
                passed_emoji = "✅" if passed else "❌"
                markdown += f"| {table} | {passed_emoji} | {details} |\n"

        self._update_results(all_results)
        return {"output": Markdown(markdown), "results": all_results}

    def tables_have_same_snapshots(
        self,
        db_name: str,
        critical_failure: bool = True,
        tables: list = [],
        initial_snapshot_dates: dict = {},
        show_snapshots_from: str = None,
    ):
        """
        Checks that tables are partitioned into the same set of snapshots.
        Tables that are added later should have the same snapshots starting
        from the date of their initial snapshot as specified in
        initial_snapshot_dates.
        """
        if not tables:
            tables = self.qe.get_tables(db_name)

        query_results = {}
        # Get snapshots for each table
        for table in tables:
            query_snapshots = f"""
                select distinct {self.snapshot_column_name}
                from {db_name}.{table}
                """
            df = self.qe.run_query(query_snapshots)
            distinct_snapshots = [str(s) for s in list(df[self.snapshot_column_name])]
            sorted_snapshots = sorted(distinct_snapshots)
            query_results[table] = sorted_snapshots

        all_snapshots = [
            snapshot for snapshots in query_results.values() for snapshot in snapshots
        ]
        # Deduplicated sorted list of all snapshots in the database
        all_snapshots = sorted(list(set(all_snapshots)))

        # if not set show_snapshots_from defaults to first snapshot
        if show_snapshots_from is None:
            show_snapshots_from = all_snapshots[0]

        # Check they match
        pass_flag = True
        for table, snapshots in query_results.items():
            if snapshots != all_snapshots:
                # Handle tables added later
                if table in initial_snapshot_dates:
                    initial_date = initial_snapshot_dates[table]
                    if initial_date in all_snapshots:
                        index = all_snapshots.index(initial_date)
                        all_snapshots_split = all_snapshots[index:]
                        if snapshots != all_snapshots_split:
                            pass_flag = False
                        else:
                            query_results[table] = snapshots
                    else:
                        pass_flag = False
                else:
                    pass_flag = False
        index = all_snapshots.index(show_snapshots_from)
        snapshots_to_show = all_snapshots[index:]

        # Generate pretty output
        markdown = f"| table | {(' | ').join(snapshots_to_show)}"
        markdown += "|\n|"
        for index in range(len(snapshots_to_show) + 1):
            markdown += "---|"
        for key in query_results:
            markdown += "\n|"
            markdown += f"{key} | "
            for snapshot in snapshots_to_show:
                if snapshot in query_results[key]:
                    markdown += " ✅ |"
                else:
                    markdown += " ❌ |"

        test_name = f"tables_have_same_snapshots.{db_name}"
        results = _get_blank_result(
            name=test_name, passed=pass_flag, critical_failure=critical_failure
        )
        self._update_results(results)
        out = {"output": Markdown(markdown), "results": results}
        return out

    def run_user_defined_test(
        self,
        test_function: Callable,
        function_name: str,
        critical_failure=True,
        **kwargs,
    ):

        out = test_function(**kwargs)

        if "results" in out:
            for r in out["results"]:
                if "name" not in r.keys():
                    r["name"] = function_name

            self._update_results(out["results"])

        return out

    def get_results_table(self, only_list_failed_tests=False):

        markdown = "| Table Name | Passed Check | Error Details |\n"
        markdown += "|---|---|---|\n"
        for result in self.all_results:
            passed = result.get("passed")
            if passed is None or (passed and only_list_failed_tests):
                pass

            if passed:
                result_emoji = "✅"
            elif result.get("param_critical_failure", True):
                result_emoji = "❌"
            else:
                result_emoji = "🟠"

            markdown += (
                f"| {result['name']} | {result_emoji} | {result.get('status')} |\n"
            )

        return Markdown(markdown)

    def check_derived_tables_rows_equal_source(
        self,
        derived_db,
        derived_tables,
        source_db,
        source_tables,
        snapshot_date,
        additional_source_where=None,
        table_joins=None,
        critical_failure=False,
    ):

        results_list = []
        arg_dict = {
            "d": derived_tables,
            "s": source_tables,
            "a": additional_source_where,
            "t": table_joins,
        }

        for a, b in arg_dict.items():
            if isinstance(b, str) or b is None:
                arg_dict[a] = [b]

        derived_tables = arg_dict["d"]
        source_tables = arg_dict["s"]
        additional_source_where = arg_dict["a"]
        table_joins = arg_dict["t"]

        if additional_source_where == [None]:
            additional_source_where = []
            for i in source_tables:
                additional_source_where.append(None)

        if table_joins == [None]:
            table_joins = []
            for i in source_tables:
                table_joins.append(None)

        if (
            not len(source_tables)
            == len(derived_tables)
            == len(additional_source_where)
            == len(table_joins)
        ):
            raise ValueError(
                "number of items in each list, source_tables, derived_tables,"
                " additional_source_where and table_joins need to be equal."
            )

        markdown = "| table | Passed Check | Error Details |\n"
        markdown += " |---|---|---|\n|"

        for s, d, j, a in zip(
            source_tables, derived_tables, table_joins, additional_source_where
        ):

            if a is None:
                a = ""
            elif not a.lower().startswith("and"):
                raise ValueError(
                    "additonal criteria for where statement in source "
                    "table needs to begin 'and'"
                )

            s1 = f"""
            SELECT COUNT(*) as c
            FROM {derived_db}.{d}
            WHERE {self.snapshot_column_name} = date '{snapshot_date}'
            """

            if j is None:
                s2 = f"""
                SELECT COUNT(*) as c
                FROM {source_db}.{s}
                WHERE {self.snapshot_column_name} = date '{snapshot_date}' {a}
                """
            else:
                s2 = f"""
                SELECT COUNT(*) as c
                FROM {source_db}.{s} {j}
                WHERE {s}.{self.snapshot_column_name} = date '{snapshot_date}' {a}
                """

            df1 = self.qe.run_query(s1)
            df2 = self.qe.run_query(s2)

            derived_count = df1.iloc[0][0]
            source_count = df2.iloc[0][0]

            passed = derived_count == source_count
            if passed:
                error_details = "n/a"
            else:
                error_details = (
                    f"{s} table in {source_db} has "
                    f"{source_count} rows, {d} table in "
                    f"{derived_db} has {derived_count} rows"
                )

            details = {
                "result_str": f"{derived_db}.{d} rows = "
                f"{source_count}; {source_db}.{s} rows = {derived_count}",
                "snapshot_date": snapshot_date,
                "source_db": source_db,
                "source_table": s,
                "derived_db": derived_db,
                "derived_table": d,
                "source_rows": source_count,
                "derived_rows:": derived_count,
            }

            test_name = f"check_derived_table_rows_equal_source.{derived_db}.{d}"

            res = _get_blank_result(
                name=test_name,
                passed=passed,
                critical_failure=critical_failure,
                result_details=details,
            )

            results_list.append(res)
            passed_emoji = "✅" if passed else "❌"

            markdown += f"**{d}** | {passed_emoji} | {error_details} |\n"

        self._update_results(results_list)

        return {"output": Markdown(markdown), "results": results_list}

    def expect_increasing_trend(
        self,
        data,
        x_col_name: str,
        y_col_name: str,
        from_x_value=None,
        to_x_value=None,
        critical_failure: bool = True,
        poly_order: int = 1,
        eval_on_poly: bool = False,
        ignore_most_recent: int = None,
        ignore_first: int = None,
        name_col_name="table",
    ) -> alt.Chart:
        """
        col_name:
            the name of the column in the data that is being evaluated
        from_x_value:
            value of the x data to evaluate from, mutually exclusive to ignore_first
        ignore_first:
            will evaluate from this index position, mutually exclusive to from_x_value
        to_x_value:
            value of the x data to evaluate to, mutualy exclusive to ignore_most_recent
        ignore_most_recent:
            will ignore this number of the most recent records. mutually exclusive to
            to_x_value
        critical_failure:
            set to False to flag this test as 'non fatal' (downstream processing)
        eval_on_poly:
            Set to true to base the evaluation on the poly fit rather than than the raw
            data
        """

        # are there multiple data/tables in the datframe?
        try:
            data_set_names = data[name_col_name].unique()
        except Exception:
            # no name column, assumed all the same data and give a gucci new name
            name_for_y = np.asarray(
                [f"auto_name_{name_col_name}"] * len(data), dtype=str
            )
            name_for_y = pd.Series(name_for_y)
            data[name_col_name] = name_for_y
            data_set_names = [f"auto_name_{name_col_name}"]

        data_sets = []
        if data_set_names is not None:
            for data_sets_name in data_set_names:
                data_sets.append(data[data[name_col_name] == data_sets_name])

        chart_data = pd.DataFrame()
        for i, data_set in enumerate(data_sets):
            if eval_on_poly:
                new_chart_data = self.poly_fit_data(
                    data_set,
                    x_col_name=x_col_name,
                    y_col_name=y_col_name,
                    from_x_value=from_x_value,
                    to_x_value=to_x_value,
                    poly_order=poly_order,
                    ignore_most_recent=ignore_most_recent,
                    ignore_first=ignore_first,
                    name_col_name=name_col_name,
                    return_chart_or_data="data",
                )
                chart_data = pd.concat([chart_data, new_chart_data])
                # evaluate new_chart_data and result dict or something idk man
                data_set_name = data_set[name_col_name].unique()[0]
                poly_data_set = new_chart_data[
                    new_chart_data[name_col_name] != data_set_name
                ]
                passed = poly_data_set[y_col_name].is_monotonic_increasing
                result_details = {}
            else:
                chart_data = pd.concat([chart_data, data_set])
                # evaluate data_set (clip it first) and result dict probs
                clipped_data = self._clip_data(
                    data_set,
                    x_col_name,
                    from_x_value=from_x_value,
                    to_x_value=to_x_value,
                    ignore_first=ignore_first,
                    ignore_most_recent=ignore_first,
                )
                passed = clipped_data[y_col_name].is_monotonic_increasing
                result_details = {}

            # add to results
            new_result = _get_blank_result(
                name=f"expect_rising_trend_{i}",
                passed=passed,
                critical_failure=critical_failure,
                result_details=result_details,
            )
            self._update_results(new_result)

        # set min/max y vals

        min_y = 0.99 * chart_data[y_col_name].min()
        max_y = 1.01 * chart_data[y_col_name].max()
        y = alt.Y(y_col_name, scale=alt.Scale(domain=[min_y, max_y]))
        chart = self.plot(chart_data, x=x_col_name, y=y, column=name_col_name)

        # Altair doesn't like pandas new Float64 and wants float64 (yes there's a diff)
        for col in chart.data:
            if str(chart.data[col].dtype) == "Float64":
                chart.data[col] = chart.data[col].astype(np.float64)

        return chart, new_result

    def _clip_data(
        self,
        data: pd.DataFrame,
        x_col_name: str,
        from_x_value=None,
        to_x_value=None,
        ignore_first: int = None,
        ignore_most_recent: int = None,
    ) -> pd.DataFrame:
        data = data.reset_index()
        data = data.drop("index", axis=1)

        if (
            from_x_value is None
            and to_x_value is None
            and ignore_first is None
            and ignore_most_recent is None
        ):
            return data

        x = data[x_col_name]

        if from_x_value and ignore_first is not None:
            raise ValueError("only one of 'from_x_value' and 'ignore_first' allowed")
        elif from_x_value is not None:
            from_x_value_index = np.where(x == from_x_value)[0]
            if from_x_value_index.shape != (1,):
                raise ValueError("from_x_value did not return exacly 1 value")
            else:
                from_x_value_index = from_x_value_index[0]
                data = data[from_x_value_index:]
        elif ignore_first is not None:
            data = data[ignore_first:]

        if to_x_value and ignore_most_recent is not None:
            raise ValueError(
                "only one of 'to_x_value' and 'ignore_most_recent' allowed"
            )
        elif to_x_value is not None:
            to_x_value_index = np.where(x == to_x_value)[0]
            if to_x_value_index.shape != (1,):
                raise ValueError("to_x_value did not return exacly 1 value")
            else:
                to_x_value_index = to_x_value_index[0]
                data = data[: to_x_value_index - from_x_value_index + 1]
        elif ignore_most_recent is not None:
            data = data[:-ignore_most_recent]

        data = data.reset_index()
        data = data.drop("index", axis=1)

        return data

    def poly_fit_data(
        self,
        data: pd.DataFrame,
        x_col_name: str,
        y_col_name: str,
        from_x_value=None,
        to_x_value=None,
        poly_order: int = 1,
        ignore_most_recent: int = None,
        ignore_first: int = None,
        name_col_name="table",
        return_chart_or_data="chart",
    ) -> alt.Chart:

        clipped_data = self._clip_data(
            data,
            x_col_name,
            from_x_value=from_x_value,
            to_x_value=to_x_value,
            ignore_first=ignore_first,
            ignore_most_recent=ignore_most_recent,
        )

        x = clipped_data[x_col_name]
        y = clipped_data[y_col_name]
        name = clipped_data[name_col_name].unique()[0]

        # create the poly
        poly_x = y.index.to_numpy()
        np_y = y.to_numpy(np.float64)
        poly_coefs = np.polyfit(poly_x, np_y, poly_order)
        poly = np.poly1d(poly_coefs)
        poly_y = poly(poly_x)
        poly_y = pd.Series(poly_y)

        # give the poly y a name, and concat into a pd.DataFrame
        poly_y_name = np.asarray([f"poly_fit_{name}"] * len(poly_y), dtype=str)
        poly_y_name = pd.Series(poly_y_name)
        poly_data_w_name = pd.concat(
            [x, poly_y, poly_y_name],
            keys=[x_col_name, y_col_name, name_col_name],
            axis=1,
        )

        # concat the data and the poly_data_w_name
        chart_data = pd.concat([data, poly_data_w_name])

        if return_chart_or_data == "chart":
            # find min/max y axis:
            min_y = 0.99 * chart_data[y_col_name].min()
            max_y = 1.01 * chart_data[y_col_name].max()
            chart = self.plot(
                chart_data,
                x=x_col_name,
                y=alt.Y(y_col_name, scale=alt.Scale(domain=[min_y, max_y])),
                column=name_col_name,
            )
            return chart
        elif return_chart_or_data == "data":
            return chart_data
        else:
            raise ValueError("chart or data, pick one bruh")

    def plot_sql(
        self,
        sql,
        x,
        y,
        color=alt.value("black"),
        **kwargs,
    ):
        """
        Function should take in any sql string
        and produce a plot x vs y grouped by color

        sql: sql to generate data to plot
        x: column in data for x-axis
        y: column in data for y-axis
        color: optional column to group by, or color of the plot

        For other possible kwargs see Tester.plot

        Returns: Altair Chart
        """

        cols = [x, y, color]
        for key, _ in kwargs.items():
            cols.append(key)
        if "plot_type" in cols and "column" not in cols:
            if kwargs["plot_type"] == "bar":

                raise ValueError(
                    "You must specify a column name to group "
                    "the bar chart by with column=<col_name>"
                )

        df = self.qe.run_query(sql)
        for col in cols:
            try:
                if isinstance(df[col].loc[0], date):
                    df[col] = df[col].apply(str)
            except KeyError:
                pass

        return self.plot(df, x=x, y=y, color=color, **kwargs)

    def pk_is_unique(
        self,
        db_name: str,
        table: str,
        table_type: str = "",
        pk: Union[str, list] = None,
        date: str = "",
        critical_failure: bool = True,
    ):
        """
        Checks for duplicate records for the given primary key.
        pk is a list of column names.
        table_type should be 'snapshot' or 'scd'.
        date should be a string in the form 'YYYY-MM-DD'.
        """
        if pk is None or pk == []:
            raise ValueError("'pk' should be a list of column names")
        if isinstance(pk, str):
            pk = [pk]
        if table_type not in ["snapshot", "scd"]:
            raise ValueError("'table_type' should be one of: 'snapshot', 'scd'")
        scd = table_type == "scd"

        if scd:
            sub_query = "select count(*) as count \n"
        else:
            sub_query = f"select count(*) as count, {self.snapshot_column_name}\n"

        sub_query += f"from {db_name}.{table}\n"

        if scd:
            sub_query += (
                f"where mojap_start_datetime <= date '{date}' "
                f"and mojap_end_datetime > date '{date}'\n"
            )
        else:
            sub_query += f"where {self.snapshot_column_name} = date '{date}' "

        sub_query += f"group by {pk[0]}"
        for column in pk[1:]:
            sub_query += f", {column}"

        if scd:
            sub_query += "\n"
        else:
            sub_query += f", {self.snapshot_column_name}\n"

        sub_query += "having count(*) > 1\n"

        count_query = f"select count(*) as count from (\n{sub_query})"

        df = self.qe.run_query(count_query)
        count = int(df.iloc[0, 0])

        markdown = (
            f"Duplicate PKs for table '{table}': {count} duplicated PKs at {date}"
        )
        result_details = {
            "count": count,
        }
        pass_flag = count == 0

        test_name = f"pk_is_unique.{db_name}.{table}"
        results = _get_blank_result(
            name=test_name,
            passed=pass_flag,
            critical_failure=critical_failure,
            result_details=result_details,
        )
        self._update_results(results)
        return {"output": Markdown(markdown), "results": results}

    def _build_all_cols_null_count_sql(self, db_name, table, columns, snapshot):

        sql = "SELECT "

        for col in columns:
            null_str = f"sum(case when {col} is null then 1 else 0 end) as {col},"
            sql += null_str

        sql = sql[: len(sql) - 1]

        sql += f" from {db_name}.{table}"

        sql += f" where {self.snapshot_column_name} = date '{snapshot}'"

        return sql

    def _return_desc_sorted_table_snapshots(
        self,
        db_name: str,
        table: str,
    ) -> List[str]:
        """
        Returns table snapshot dates as strings in a list for a given table.
        They are sorted descending
        """

        # get snapshots for table
        query_snapshots = f"""
                select distinct {self.snapshot_column_name}
                from {db_name}.{table}
                group by {self.snapshot_column_name}
                order by {self.snapshot_column_name} DESC
                """

        df_snapshots = self.qe.run_query(query_snapshots)

        snapshots = [
            d.strftime("%Y-%m-%d") for d in df_snapshots[self.snapshot_column_name]
        ]

        return snapshots

    def new_null_columns_in_snapshot(
        self,
        db_name: str,
        tables: list = None,
        critical_failure: bool = True,
        snapshot: str = None,
        prev_snapshot: str = None,
        ctas_approach: dict = {},
    ):
        """
        this checks whether any column in a particular snapshot table
        data contains all null values when previously it didn't.

        db_name:
            name of the database to run the test on.
        tables:
            optional list of table names to test. Tests all tables
            if omitted.
        critical_failure:
            whether the test failure is considered critical.
        snapshot:
            str of date in format 'YYYY-MM-DD' relating to the later snapshot
            of data for the test.
        prev_snapshot:
            str of date in format 'YYYY-MM-DD' relating to the earlier snapshot
            of data for the test.
        ctas_approach:
            if you have one or more tables that contain nested datatypes,
            this should be used.

            e.g. for complex_table1 and complex_table2 you would pass:

                {complex_table1: True, complex_table2: True}

            All other tables will default to ctas_approach=False
            if not defined in the dict.
        """

        if tables is None:
            tables = self.qe.get_tables(db_name)

        ctas_not_passed = {t: False for t in tables if t not in ctas_approach.keys()}
        ctas_approaches = dict(ctas_not_passed, **ctas_approach)

        all_results = []
        d = {}

        set_snapshot = True if snapshot is None else False
        set_prev_snapshot = True if prev_snapshot is None else False
        snapshot_str = ""

        markdown = "| Table Name | Passed Check | Error Details |\n"
        markdown += "|---|---|---|\n"

        for table in tables:

            passed = True
            d[table] = {}

            snapshots_list = self._return_desc_sorted_table_snapshots(
                db_name,
                table,
            )

            # if None use the most recent and one previous to most recent snapshots
            if set_snapshot:
                snapshot = snapshots_list[0]

            if set_prev_snapshot:
                prev_snapshot = snapshots_list[1]

            snapshot_str = (
                f"snapshots compared were: `{snapshot}` and `{prev_snapshot}`"
            )

            # check snapshot exists and skip to next table if not
            if snapshot not in snapshots_list or prev_snapshot not in snapshots_list:
                d[table]["passed"] = False
                d[table]["detail"] = (
                    f"snapshot `{snapshot}` or `{prev_snapshot}` doesn't "
                    f"exist in the {table} table. Run the test without the "
                    "snapshot and prev_snapshot parameters or with snapshots that exist"
                )

                pass_flag = False

                test_name = f"new_null_columns_in_snapshot.{db_name}.{table}"
                results = _get_blank_result(
                    name=test_name,
                    passed=pass_flag,
                    critical_failure=critical_failure,
                    result_details=d[table]["detail"],
                )

                markdown += f"| {table} | ❌ | {d[table]['detail']} |\n"

                continue

            row_count_new = self.qe.run_query(
                f"""
                select count(*) as c
                from {db_name}.{table}
                where {self.snapshot_column_name} = date '{snapshot}'
                """,
            ).iloc[0, 0]

            row_count_old = self.qe.run_query(
                f"""
                select count(*) as c
                from {db_name}.{table}
                where {self.snapshot_column_name} = date '{prev_snapshot}'
                """,
            ).iloc[0, 0]

            columns = self.qe.run_query(
                f"select * from {db_name}.{table} limit 1",
                ctas_approach=ctas_approaches[table],
            ).columns

            sql_new = self._build_all_cols_null_count_sql(
                db_name=db_name, table=table, columns=columns, snapshot=snapshot
            )

            sql_old = self._build_all_cols_null_count_sql(
                db_name=db_name, table=table, columns=columns, snapshot=prev_snapshot
            )

            nulls_new = self.qe.run_query(sql_new)
            nulls_old = self.qe.run_query(sql_old)

            for column in nulls_new.columns:

                null_count_new = nulls_new[column].item()

                if column not in nulls_old.columns:
                    # skip testing that column
                    continue

                null_count_old = nulls_old[column].item()

                if (
                    null_count_new == row_count_new
                    and not null_count_old == row_count_old
                ):
                    d[table][column] = {
                        "passed": False,
                        "detail": "FAIL " + snapshot_str,
                    }
                    passed = False

            d[table]["passed"] = passed

            if passed:
                d[table]["detail"] = snapshot_str
                passed_emoji = "✅"
            elif not passed:
                col_fail_list = [f"`{c}`" for c in d[table] if not c == "passed"]
                col_fail_str = "<br>    - ".join(col_fail_list)
                d[table]["detail"] = (
                    f"These columns were null in the newer `{snapshot}`, "
                    f"but not older `{prev_snapshot}` snapshot:<br><br>- {col_fail_str}"
                )
                passed_emoji = "❌"

            markdown += f"| {table} | {passed_emoji} | {d[table]['detail']} |\n"

            test_name = f"new_null_columns_in_snapshot.{db_name}.{table}"
            results = _get_blank_result(
                name=test_name,
                passed=passed,
                critical_failure=critical_failure,
                result_details=d[table]["detail"],
            )

            all_results.append(results)

        self._update_results(all_results)

        return {"output": Markdown(markdown), "results": all_results}
