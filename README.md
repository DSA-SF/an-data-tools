# an-sql-sync

Syncs member data from Action Network into a postgres database

## Development

### Recommended approach: devcontainers

The devcontainer is configured with all dependencies (Python and Postgres in particular).

- Set up [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/tutorial)
- Open `an-sql-sync/` in VS Code and Open in Container
- Open a terminal and `python src/create_tables.py`
- `python src/main.py`

### Running locally

- `pip install -r requirements.txt`
- Run a local Postgres instance: `docker run -p 5432:5432 postgres`
- `python src/create_tables.py`
- `python src/main.py`
