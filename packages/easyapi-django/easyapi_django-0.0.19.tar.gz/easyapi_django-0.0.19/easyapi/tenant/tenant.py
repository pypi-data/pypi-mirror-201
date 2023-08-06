from contextvars import ContextVar

from django.db import connections
from django.apps import AppConfig

try:
    from settings import TENANT_MODEL
except Exception:
    TENANT_MODEL = None

tenant_model = AppConfig.get_models(*TENANT_MODEL.split('.', 1)) if TENANT_MODEL else None

DB_PREFIX = 'tenant'
db_state = ContextVar("db_state", default='default')


def save_connection(account):
    if not account.db:
        return

    account_db = f'{DB_PREFIX}_{account.id}'
    db_state.set(account_db)

    if account_db in connections.databases:
        return connections.databases[account_db]

    connection = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': account_db,
        'HOST': account.db.host,
        'USER': account.db.user,
        'PASSWORD': account.db.password,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'TIME_ZONE': None,
        'PORT': '',
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'use_unicode': True,
            'charset': 'utf8mb4',
            'connect_timeout': 120,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1"
        },
    }
    connections.databases[account_db] = connection

    return connection


async def set_tenant(identifier):
    if tenant_model:
        account = await tenant_model.objects.filter(
            identifier=identifier,
        ).select_related('db').afirst()
        connection = save_connection(account)

        account_db = f'{DB_PREFIX}_{identifier}'
        if connection and account_db not in connections.databases:
            connections.databases[account_db] = connection

    else:
        account_db = 'default'

    db_state.set(account_db)

    return account_db
