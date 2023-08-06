import typer

import sqlite3


app = typer.Typer()


@app.command()
def dump(
    database: str = typer.Argument(..., help="Database name"),
    output_file: str = typer.Argument(..., help="Output file name"),
):
    """Create an SQLite database dump."""
    try:
        # Connect to the database
        connection = sqlite3.connect(database)

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the SQLite dump command
        with open(output_file, "w") as f:
            for line in connection.iterdump():
                f.write(f"{line}\n")

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Print success message
        typer.echo(f"SQLite database dump created successfully: {output_file}")

    except sqlite3.Error as e:
        typer.echo(f"Error creating SQLite database dump: {e}")


if __name__ == "__main__":
    app()
