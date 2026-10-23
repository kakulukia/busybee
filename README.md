# Busy Bee Catering

Django website with Pug templates, Sass styles and checked-in frontend assets.
Python dependencies are managed with [uv](https://docs.astral.sh/uv/).

## Local setup

Install the current version of uv, then run from the project directory:

```sh
uv sync --locked
uv run python manage.py migrate --settings=settings.dev
uv run python manage.py runserver --settings=settings.dev
```

The project requires Python 3.15 or newer and uses Python 3.15.1 by default, as
specified in `.python-version`. uv downloads the interpreter when needed and
creates `.venv`. Native dependencies such as uWSGI require a C compiler and the
platform development headers. On macOS, install the Xcode command line tools.

When migrating an existing checkout, remove the old `.venv` symlink before the
first sync. The old `.direnv` environment can then be removed when no longer
needed.

`manage.py` prompts for missing secrets defined in `my_secrets/definitions.py`.
Values are stored in the ignored `my_secrets/secrets.py`; keep that file private.
The development settings use a console email backend.

If you use direnv, `direnv allow` activates `.venv`, syncs the locked dependencies
and defaults to `settings.dev`, preserving an existing `DJANGO_SETTINGS_MODULE`.
Otherwise, pass `--settings=settings.dev` as above or set
`DJANGO_SETTINGS_MODULE=settings.dev`. Personal settings can inherit from
`settings.dev`, as `settings.andy` does.

## Dependencies and checks

```sh
uv add package-name
uv add --dev package-name
uv lock --upgrade
uv sync --locked
uv run python manage.py check --settings=settings.dev
uv run python manage.py test --settings=settings.dev
uv run python manage.py makemigrations --check --dry-run --settings=settings.dev
uv pip check
uv run ruff check .
uv run ruff format --check .
```

Commit `pyproject.toml`, `.python-version` and `uv.lock` together when dependencies
change. `uv sync` includes the development group. Production installations use
`uv sync --locked --no-dev`.

The debug toolbar uses its built-in profiling panel instead of the obsolete
`djdt-flamegraph` extension. Enable the profiling panel in the toolbar when needed
and run the development server with `--nothreading --noreload` for profiling.

Ruff handles linting and formatting. Run `uv run ruff format .` to format files.
Formatting targets 90 columns; linting permits up to 140 columns for lines that
cannot be wrapped. Generated migrations are excluded.

`bash misc/setup_repo.sh` installs an optional Ruff pre-commit hook for staged
Python files. It checks lint and formatting without modifying or staging files.
It leaves existing hooks in place and reports when manual integration is required.

## Deployment

The deployment tasks use `fab-classic` and uv, preserving the Fabric 1 API:

```sh
uv run fab --list
uv run fab migrate
```

`migrate` pulls the repository on the configured host, installs production
dependencies from `uv.lock`, applies database migrations, compresses and collects
static files, and restarts the PM2 process. These commands change the live system;
run them only as part of an approved deployment.

The server needs uv on its noninteractive shell's `PATH`, a supported Python
interpreter or access to uv's Python downloads, and build tools for uWSGI.
Replace any existing Poetry or pyenv `.venv` symlink before the first uv sync.
`settings/busybee.sh` starts uWSGI through uv from the project root.

The production log rotation rule is stored in `settings/busybee.logrotate`.
Install it on the server with:

```sh
sudo install -o root -g root -m 0644 \
  /opt/www/busybee/settings/busybee.logrotate /etc/logrotate.d/busybee
sudo logrotate --debug /etc/logrotate.d/busybee
```

The existing daily `logrotate.timer` processes this rule. It keeps 14 compressed
archives per Busybee log and skips empty or missing files. `copytruncate` keeps
logging active without restarting PM2 or the application.

The frontend libraries and CDN references are maintained separately from the
Python dependencies.
