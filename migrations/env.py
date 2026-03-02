import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Import setting dan Base model kamu
from app.core.config import settings
from app.db.session import Base
import app.db.base_imports
# Import semua model agar terdeteksi oleh autogenerate
import app.models  

# Objek konfigurasi Alembic
config = context.config

# 2. Setup Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Setup Metadata untuk --autogenerate
target_metadata = Base.metadata

def get_url():
    """Mengambil URL dari settings dan memastikan driver mysql+pymysql digunakan."""
    url = settings.database_url
    if url and url.startswith("mysql://"):
        return url.replace("mysql://", "mysql+pymysql://", 1)
    return url

def run_migrations_offline() -> None:
    """Menjalankan migrasi dalam 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Mendeteksi perubahan tipe data kolom
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Menjalankan migrasi dalam 'online' mode."""
    # Ambil konfigurasi dari alembic.ini sebagai dasar
    configuration = config.get_section(config.config_ini_section, {})
    # Override URL dengan yang sudah diperbaiki
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()