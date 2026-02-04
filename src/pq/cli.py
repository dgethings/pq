"""CLI argument parsing module."""

import sys
from pathlib import Path
from typing import Annotated, Any
import typer

from pq.evaluator import evaluate_query
from pq.loader import DocumentLoadError, load_document, read_stdin
from pq.types import FileTypes
from rich import print


app = typer.Typer()


@app.command()
def main(
    query: Annotated[
        str,
        typer.Argument(help="Python expression that returns a subset of given file"),
    ],
    file_path: Annotated[
        Path, typer.Argument(help="Input file, use '-' to read from stdin")
    ],
    # format: Annotated[
    #     FileTypes,
    #     typer.Option(
    #         help="When reading from stdin you need to specify the file format"
    #     ),
    # ],
) -> None:
    """Main CLI entry point.

    Args:
        file_path: Optional file path argument
    """
    data = load_document(file_path=file_path)
    result = evaluate_query(query, data)
    print(result)


# if not query and not file_path:
#     raise typer.BadParameter(
#         message="Must supply a file path, query string and file path or query string and redirect STDIN"
#     )
# if isinstance(query, Path):
#     file_path = query
#     query = "_"
# if query and (not file_path and not format):
#     raise typer.BadParameter(
#         message="Must provide a format when reading from stdin"
#     )
# if file_path is not None and not file_path.exists():
#     raise typer.BadParameter(f"Cannot find: {file_path}")
# if file_path is not None and file_path.exists():
#     data = load_document(file_path=file_path)
# if file_path is None and format:
#     data = load_document(stdin_content=sys.stdin.read())
#
# if not data:
#     raise typer.BadParameter("unable to process args")
#
# if query:
#     evaluate_query(expression=query, data=data)
# try:
#     if file_path is not None:
#         data = load_document(file_path=Path(file_path))
#     else:
#         if sys.stdin.isatty():
#             typer.echo(
#                 "Error: No input provided. Use: pq <file.json> or cat file.json | pq",
#                 err=True,
#             )
#             raise typer.Exit(1)
#         stdin_content = read_stdin()
#         data = load_document(stdin_content=stdin_content)
#
#     from pq.main import QueryApp
#
#     app_instance = QueryApp(data)
#     app_instance.run()
#
#     sys.exit(app_instance.return_code or 0)
#
# except DocumentLoadError as e:
#     typer.echo(f"Error loading document: {e}", err=True)
#     raise typer.Exit(1)
# except KeyboardInterrupt:
#     raise typer.Exit(0)
# except Exception as e:
#     typer.echo(f"Unexpected error: {e}", err=True)
#     raise typer.Exit(1)


if __name__ == "__main__":
    app()
