from pathlib import Path
from typing import Union

from pandas import DataFrame
from rich.console import Console
from rich.table import Table

from . import settings


def get_console(
    is_terminal: bool = True,
    log_file_name: str = settings.DEFAULT_LOG_FILE,
):
    # create terminal accordingly
    if not is_terminal:
        console = Console(file=(Path.cwd() / log_file_name).open(mode="w"))
    else:
        console = Console()
    return console


# make a console log function that logs output to a file or terminal based on the config
def console_log(
    console: Console,
    virus_dataframe: DataFrame,
    file_path: Union[str, Path],
):
    # a rule with the file name followed by the rich table for dataframe
    relative_path = str(Path(file_path).relative_to(Path.cwd()))
    console.rule(f"{relative_path}")
    table = Table(show_header=True, header_style="bold")

    # add column names to tables for schema_context,column,check,check_number,failure_case
    # TODO: `overflow` methods seems to have no change over column, thus adding ellipses manually
    table.add_column("schema_context")
    table.add_column("column")
    table.add_column("check")
    table.add_column("check_number")
    table.add_column("failure_case")

    for idx, each_row in enumerate(
        virus_dataframe.to_dict(orient="records"), 1
    ):
        table.add_row(
            str(each_row["schema_context"]),
            str(each_row["column"]),
            str(each_row["check"][:100] + "..."),
            str(each_row["check_number"]),
            str(each_row["failure_case"]),
        )

    console.print(table)
