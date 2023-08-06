from importlib import import_module
from django.conf import settings

from django_tenants import app_settings
from django_tenants.backends.postgresql.schema import RLSDatabaseSchemaEditor

ORIGINAL_BACKEND = getattr(settings, 'ORIGINAL_BACKEND', 'django.db.backends.postgresql')

original_backend = import_module(ORIGINAL_BACKEND + '.base')


class DatabaseWrapper(original_backend.DatabaseWrapper):
    SchemaEditorClass = RLSDatabaseSchemaEditor

    def __init__(self, *args, **kwargs):
        self.tenant = None
        self.descendants = None
        super().__init__(*args, **kwargs)

    def set_tenant(self, tenant):
        self.tenant = tenant

    def set_tenant_descendants(self, descendants):
        # In order to hit the query before the assignment (because of lazy queries) list casting is necessary.
        self.descendants = list(descendants)

    def _cursor(self, name=None):
        cursor = super(DatabaseWrapper, self)._cursor(name=name)  # NOQA

        if cursor.cursor.withhold:
            return cursor

        if name:
            return cursor

        cursor.execute(f'SET picatron.administration_tenant = {app_settings.MAIN_TENANT_ID}')

        if self.tenant:
            cursor.execute(f'SET picatron.active_tenant = {self.tenant.pk}')
        else:
            cursor.execute(f'SET picatron.active_tenant = {app_settings.MAIN_TENANT_ID}')

        if self.descendants:
            comma_seperated_descendants = ",".join([str(descendant.pk) for descendant in self.descendants])
            cursor.execute(f'SET picatron.descendant_tenants = "{comma_seperated_descendants}"')
        else:
            cursor.execute(f'SET picatron.descendant_tenants TO DEFAULT')

        return cursor


class FakeTenant:
    """
    We can't import any db model in a backend (apparently?), so this class is used
    for wrapping schema names in a tenant-like structure.
    """
    def __init__(self):
        self.is_main = True
