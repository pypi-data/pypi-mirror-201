from django.core.management import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        models = list(
            filter(
                lambda x: hasattr(x, 'tenant') and hasattr(x.tenant.field, 'rls_required'),
                apps.get_models()
            )
        )
        with connection.schema_editor() as schema_editor:
            for model in models:
                schema_editor._unset_tenant_rls(True, model)
                schema_editor._set_tenant_rls(True, model)
