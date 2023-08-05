import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from .helpers import (TEMPLATE_SERVICES_CONTRACTS, TEMPLATE_SERVICES_END,
                      NumberColumn)
from .models import (Component, ComponentService, Contract, Contractor,
                     Invoice, Probe)


# Probe
class ProbeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    site = tables.Column(linkify=True)
    location = tables.Column(linkify=True)
    changes_count = tables.Column()
    discovered_data = tables.JSONColumn()

    class Meta(NetBoxTable.Meta):
        model = Probe
        fields = ('pk', 'id', 'time', 'name', 'device_descriptor', 'site_descriptor', 'location_descriptor', 'description',
                  'part', 'serial', 'device', 'site', 'location', 'comments', 'changes_count', 'actions', 'category', 'creation_time')
        default_columns = ('id', 'time', 'name', 'serial', 'part', 'device_descriptor', 'device',
                           'site_descriptor', 'site', 'location_descriptor', 'locations', 'changes_count')


# Contractor
class ContractorTable(NetBoxTable):
    name = tables.Column(linkify=True)
    contracts_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = Contractor
        fields = ('pk', 'id', 'name', 'company', 'address',
                  'comments', 'contracts_count', 'actions')
        default_columns = ('id', 'name', 'company', 'contracts_count')


# Contract
class ContractTable(NetBoxTable):
    name = tables.Column(linkify=True)
    contractor = tables.Column(linkify=True)
    subcontracts_count = tables.Column()
    invoices_count = tables.Column()
    contract_type = tables.Column(orderable=False)
    attachments_count = tables.Column()
    parent = tables.Column(linkify=True)
    type = ChoiceFieldColumn()
    price = NumberColumn()

    class Meta(NetBoxTable.Meta):
        model = Contract
        fields = ('pk', 'id', 'name', 'name_internal', 'contractor', 'type', 'contract_type', 'price', 'signed',
                  'accepted', 'invoicing_start',  'invoicing_end', 'parent', 'comments', 'invoices_count', 'subcontracts_count', 'attachments_count', 'actions')
        default_columns = ('id', 'name', 'name_internal', 'contractor', 'type', 'contract_type', 'price',
                           'signed', 'accepted', 'invoicing_start',  'invoicing_end', 'parent', 'attachments_count')


# Invoice
class InvoiceTable(NetBoxTable):
    name = tables.Column(linkify=True, verbose_name='Invoice Number')
    name_internal = tables.Column(verbose_name='Internal ID')
    contract = tables.Column(linkify=True)
    attachments_count = tables.Column()
    price = NumberColumn()

    class Meta(NetBoxTable.Meta):
        model = Invoice
        fields = ('pk', 'id', 'name', 'name_internal', 'project', 'contract', 'price',
                  'invoicing_start',  'invoicing_end', 'comments', 'attachments_count', 'actions')
        default_columns = ('id', 'name', 'name_internal', 'contract', 'project',
                            'invoicing_start',  'invoicing_end', 'price', 'attachments_count')


# Component
class ComponentTable(NetBoxTable):
    serial = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    inventory_item = tables.Column(linkify=True)
    site = tables.Column(linkify=True)
    location = tables.Column(linkify=True)
    order_contract = tables.Column(linkify=True)
    price = NumberColumn()
    tags = columns.TagColumn()
    services_to = columns.TemplateColumn(template_code=TEMPLATE_SERVICES_END)
    services_contracts = tables.TemplateColumn(
        template_code=TEMPLATE_SERVICES_CONTRACTS)

    class Meta(NetBoxTable.Meta):
        model = Component
        fields = ('pk', 'id', 'serial', 'serial_actual',
                  'partnumber', 'device', 'asset_number', 'project', 'location',
                  'site', 'vendor', 'quantity', 'price', 'order_contract', 'inventory_item',
                  'warranty_start', 'warranty_end', 'comments', 'actions', 'tags',
                  'services_count', 'services_contracts', 'services_to')

        default_columns = ('id', 'serial', 'serial_actual',
                           'device', 'asset_number', 'site',
                           'quantity', 'price', 'actions')

# ComponentService
class ComponentServiceTable(NetBoxTable):
    component = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)
    service_price = NumberColumn(accessor='service_price')

    class Meta(NetBoxTable.Meta):
        model = ComponentService
        fields = ('pk', 'id', 'service_start', 'service_end',
                  'service_param', 'service_price', 'service_category', 'service_category_vendor',
                  'component', 'contract', 'comments', 'actions')
        default_columns = ('id', 'contract', 'service_start', 'service_end',
                           'service_price', 'service_category', 'service_category_vendor', 'service_param', 'actions')
