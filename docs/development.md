# Local Development

This guide sets up the project on your own machine so you can view the screen mockups, load the database, and work with the Python packages the server uses. To put the site on EC2, see [deploy.md](deploy.md).

The repo does not contain a Flask application yet. Locally, you can run the mockups in `ui/`, build a SQLite database from `schema.sql` and `sampledata.sql`, and install Flask and Gunicorn from `deploy/requirements.txt`.

## What's in the repo

| Path | Purpose |
| --- | --- |
| `ui/` | Static HTML and CSS mockups of each screen |
| `schema.sql` | Creates the database tables described in [db.md](../db.md) |
| `sampledata.sql` | Inserts sample spaces, computers, equipment, and reservations |
| `openapi.yaml` | The HTTP contract between the browser and the server |
| `use_cases.md` | Booking flows and error cases, used as acceptance tests |
| `deploy/requirements.txt` | Python packages: Flask and Gunicorn |
| `scripts/userdata.sh` | EC2 startup script; not used locally |

## Prerequisites

- **Git**
- **Python 3.9 or newer.** Check with `python3 --version`.
- **SQLite 3.** Check with `sqlite3 --version`. macOS includes it. On Ubuntu, run `sudo apt install sqlite3`.

## 1. Clone the repo

```bash
git clone https://github.com/cs390f26/Esports-spec-repo.git
cd Esports-spec-repo
```

Run every command in this guide from the repo root.

## 2. Create the virtual environment

A virtual environment keeps this project's packages separate from your system Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r deploy/requirements.txt
```

Your prompt shows `(.venv)` while the environment is active. Activate it again each time you open a new terminal. Run `deactivate` to leave it.

When you add a package, install it and add it to `deploy/requirements.txt` so the EC2 instance gets it too:

```bash
pip install <package>
echo "<package>" >> deploy/requirements.txt
```
## 3. View the mockups

Serve the `ui/` folder with Python's built-in web server:

```bash
python3 -m http.server 8000 --directory ui
```

Open [http://localhost:8000/01-overview.html](http://localhost:8000/01-overview.html). Press `Ctrl+C` to stop the server.

The mockups keep their sample stations and bookings in the browser's local storage, under the key `nexus-simplified-v1`. To reset them, clear that key in your browser's developer tools (**Application → Local Storage**) and reload.

## 4. Set up the database

Create a local SQLite database from the schema, then load the sample data:

```bash
sqlite3 esports.db < schema.sql
sqlite3 esports.db < sampledata.sql
```

`schema.sql` drops and recreates every table, so run both commands again at any time to reset the database.

Check that the data loaded:

```bash
sqlite3 esports.db "SELECT space_id, space_name, is_active FROM Spaces;"
```

```text
1|Station 01 - Cyberhound Rig|1
2|Station 02 - Cyberhound Rig|0
```

To explore the data, open an interactive session with `sqlite3 esports.db`. Type `.tables` to list the tables, `.headers on` to show column names, and `.quit` to exit.

The sample data reflects these rules from [db.md](../db.md):

- Station 02 is inactive. Its existing reservation, 8802, is kept.
- Only one `CONFIRMED` reservation can exist per space and start time. A second one fails with a `UNIQUE constraint failed` error.
- Status and category values are limited to the values listed in the schema.

## 5. Read the API spec

`openapi.yaml` lists every endpoint, its request and response bodies, and the errors users can run into. To browse it, paste the file into [Swagger Editor](https://editor.swagger.io/), or install the **OpenAPI (Swagger) Editor** extension in your editor.

## Keeping local files out of git

The virtual environment and the database file are local only. `.gitignore` already excludes them:

```text
.venv/
*.db
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `pip: command not found`, or packages install outside the project | The virtual environment is not active | Run `source .venv/bin/activate` |
| `ModuleNotFoundError: No module named 'flask'` | Packages were installed in a different environment | Activate `.venv`, then rerun `pip install -r deploy/requirements.txt` |
| `Address already in use` when starting the web server | Something else is using port 8000 | Use another port, such as `python3 -m http.server 8080 --directory ui` |
| The mockups show old bookings | Local storage still holds earlier data | Clear `nexus-simplified-v1` in the browser's local storage |
| `Error: no such table` | `schema.sql` was not loaded into this database file | Run both `sqlite3` commands from step 4 |
