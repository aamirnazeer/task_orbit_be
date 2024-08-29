from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, MetaData, create_engine
from sqlalchemy import pool
from app.models.users import Base as UserBase
from app.models.boards import Base as BoardsBase
from app.models.cards import Base as CardsBase
from app.models.refresh_tokens import Base as RefreshTokensBase
from alembic import context
from sqlalchemy_utils import create_database, database_exists

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
metadata = MetaData()

for base in (UserBase, BoardsBase, CardsBase, RefreshTokensBase):
    for table in base.metadata.tables.values():
        table.to_metadata(metadata)

target_metadata = metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
if os.getenv("ENV") == 'test':
    config.set_main_option("sqlalchemy.url", os.getenv("SQLALCHEMY_DATABASE_URL_TEST", ""))
else:
    config.set_main_option("sqlalchemy.url", os.getenv("SQLALCHEMY_DATABASE_URL", ""))

if not database_exists(os.getenv("SQLALCHEMY_DATABASE_URL", "")):
    create_database(os.getenv("SQLALCHEMY_DATABASE_URL", ""))
    print("SQLALCHEMY_DATABASE_URL created")

if not database_exists(os.getenv("SQLALCHEMY_DATABASE_URL_TEST", "")) and os.getenv("ENV") == 'local':
    create_database(os.getenv("SQLALCHEMY_DATABASE_URL_TEST", ""))
    print("SQLALCHEMY_DATABASE_URL_TEST created")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = os.getenv("SQLALCHEMY_DATABASE_URL", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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
