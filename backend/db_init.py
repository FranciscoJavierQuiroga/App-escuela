from alembic.config import Config
from alembic import command
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import settings

# Create alembic.ini file
alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "migrations")
alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
alembic_cfg.set_main_option("file_template", "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s")

# Create migrations directory if it doesn't exist
migrations_dir = Path(__file__).parent / "migrations"
migrations_dir.mkdir(exist_ok=True)

# Create versions directory if it doesn't exist
versions_dir = migrations_dir / "versions"
versions_dir.mkdir(exist_ok=True)

# Create the env.py file for Alembic
env_py_content = """import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import SQLModel models
from app.models import *
from app.database.session import engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    \"\"\"Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    \"\"\"
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    \"\"\"Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    \"\"\"
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

# Write the env.py file
with open(migrations_dir / "env.py", "w") as f:
    f.write(env_py_content)

# Create an empty __init__.py file in the migrations directory
with open(migrations_dir / "__init__.py", "w") as f:
    pass

# Initialize Alembic
command.init(alembic_cfg, migrations_dir)

print("Alembic configuration created successfully.")