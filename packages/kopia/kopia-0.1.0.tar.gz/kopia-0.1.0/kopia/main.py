import typer

from .mysqlc.app import app as mysql_app
from .sqlite.app import app as sqlite_app


app = typer.Typer()
app.add_typer(mysql_app, name="mysql")
app.add_typer(sqlite_app, name="sqlite")


if __name__ == "__main__":
    app()
