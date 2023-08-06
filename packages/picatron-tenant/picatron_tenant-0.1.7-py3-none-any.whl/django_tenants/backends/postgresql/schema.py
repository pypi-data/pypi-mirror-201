# -*- coding: utf-8 -*-
""" Created by Safa Arıman on 5/5/22 """
from django.db.backends.postgresql.schema import DatabaseSchemaEditor

__author__ = 'safaariman'


class RLSDatabaseSchemaEditor(DatabaseSchemaEditor):
    sql_enable_rls = "ALTER TABLE %(table)s ENABLE ROW LEVEL SECURITY;"  # NOQA
    sql_disable_rls = "ALTER TABLE %(table)s DISABLE ROW LEVEL SECURITY;"  # NOQA
    sql_force_rls = "ALTER TABLE %(table)s FORCE ROW LEVEL SECURITY;"  # NOQA
    sql_create_policy = (
        "CREATE POLICY _po_tenant_%(table)s ON %(table)s FOR ALL USING %(policy)s;"
    )
    sql_drop_policy = (
        "DROP POLICY IF EXISTS _po_tenant_%(table)s ON %(table)s"
    )
    sql_alter_column_default_tenant = (
        "ALTER TABLE ONLY %(table)s ALTER COLUMN tenant_id SET DEFAULT current_setting('picatron.active_tenant', true)::bigint;"  # NOQA
    )
    active_tenant = "current_setting('picatron.active_tenant', true)::bigint"
    admin_tenant = "current_setting('picatron.administration_tenant', true)::bigint"
    descendant_tenants = "current_setting('picatron.descendant_tenants', true)"

    descendant_tenants_array = f"string_to_array({descendant_tenants}, ',')::bigint[]"

    descendant_tenant_policy = f"tenant_id = ANY({descendant_tenants_array})"
    active_tenant_read_policy = f"tenant_id = {active_tenant} AND {descendant_tenant_policy}"
    active_tenant_write_policy = f"tenant_id = {active_tenant} OR {descendant_tenant_policy}"
    admin_tenant_policy = f"{active_tenant} = {admin_tenant}"

    read_policy = f"{active_tenant_read_policy} OR {admin_tenant_policy} OR {descendant_tenant_policy}"
    write_policy = f"{active_tenant_write_policy} OR {admin_tenant_policy}"

    main_rls_policy = f"({read_policy}) WITH CHECK ({write_policy})"

    def create_model(self, model):
        # if any field has the rls_required flag then rls constraints are created
        enable_rls = any(field.rls_required for field in model._meta.local_fields if hasattr(field, 'rls_required'))

        super().create_model(model=model)

        # enable RLS on table and create policy
        self._set_tenant_rls(enable_rls, model)

    def add_field(self, model, field):
        enable_rls = field.rls_required if hasattr(field, 'rls_required') else False

        super(RLSDatabaseSchemaEditor, self).add_field(model, field)

        # enable RLS on table and create policy
        self._set_tenant_rls(enable_rls, model)

    def remove_field(self, model, field):
        is_left_rls_required_field = any(
            local_field.rls_required for local_field in model._meta.local_fields
            if (hasattr(local_field, 'rls_required') and local_field.name != field.name)
        )
        is_rls_required_for_field = field.rls_required if hasattr(field, 'rls_required') else False
        disable_rls = is_rls_required_for_field and not is_left_rls_required_field

        super().remove_field(model, field)

        # disable RLS on table and delete policy
        self._unset_tenant_rls(disable_rls, model)

    def _set_tenant_rls(self, enable_rls, model):
        if enable_rls:
            self.execute(self.sql_enable_rls % {"table": self.quote_name(model._meta.db_table)})
            self.execute(self.sql_force_rls % {"table": self.quote_name(model._meta.db_table)})
            self.execute(self.sql_create_policy % {
                "table": model._meta.db_table,
                "policy": self.main_rls_policy
            })
            self.execute(self.sql_alter_column_default_tenant % {"table": self.quote_name(model._meta.db_table)})

    def _unset_tenant_rls(self, disable_rls, model):
        if disable_rls:
            self.execute(self.sql_disable_rls % {"table": self.quote_name(model._meta.db_table)})
            self.execute(self.sql_drop_policy % {"table": model._meta.db_table})

    # abstract method, not apply in this backend because requires_literal_defaults = False
    def prepare_default(self, value):
        pass
