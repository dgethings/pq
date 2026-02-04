"""CLI argument parsing module."""

import sys

import typer
from rich import print

from pq.evaluator import evaluate_query
from pq.loader import load_document
from pq.cli_arg import Query, FilePath, FileType, Version

app = typer.Typer()


@app.command()
def main(
    query: Query,
    file_path: FilePath = None,
    file_type: FileType = None,
    v: Version = None,
) -> None:
    """Run a query against a document.

    Query a document using JSONPath or similar query language.
    Reads from a file or stdin and evaluates the query against the document data.
    """
    data = None
    if file_path is None and file_type is None:
        raise typer.BadParameter(
            "Must supply either file path or if reading from stdin must supply file type"
        )
    if file_type:
        data = load_document(stdin_content=sys.stdin.read(), format=file_type)
    if file_path:
        data = load_document(file_path=file_path)
    if data is None:
        raise typer.BadParameter("Ummm, how did we get here?")
    result = evaluate_query(query, data)
    print(result)


if __name__ == "__main__":
    app()
