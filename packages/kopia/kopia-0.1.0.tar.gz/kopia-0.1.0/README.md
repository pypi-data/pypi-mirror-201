# Kopia
Kopia is a command-line tool for creating database dumps. It supports both MySQL and SQLite databases.

## Installation
You can install kopia using pip: `pip install kopia`

## Usage
### Creating a MySQL dump
To create a MySQL dump, use the mysql command followed by the dump subcommand:

`kopia mysql dump <db_name> <username> <password>`

### Creating a SQLite dump
To create a SQLite dump, use the sqlite command followed by the dump subcommand:

`kopia sqlite dump <db_path>`

## Contributing
If you'd like to contribute to Kopia, please submit a pull request on GitHub:

https://github.com/weactivist/kopia
