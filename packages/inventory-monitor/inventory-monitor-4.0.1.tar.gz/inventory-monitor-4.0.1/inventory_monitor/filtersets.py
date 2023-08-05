import django_filters
from dcim.models import Device, Site, Location, InventoryItem
from django.db.models import Q
from extras.filters import TagFilter
from netbox.filtersets import BaseFilterSet, NetBoxModelFilterSet

from .models import (Component, ComponentService, Contract, Contractor,
                     ContractTypeChoices, Invoice, Probe)

# Probe
class ProbeFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    serial = django_filters.CharFilter(lookup_expr="icontains")
    time__gte = django_filters.DateTimeFilter(
        field_name='time',
        lookup_expr='gte'
    )
    time__lte = django_filters.DateTimeFilter(
        field_name='time',
        lookup_expr='lte'
    )
    latest_only_per_device = django_filters.BooleanFilter(
        method='_latest_only_per_device', label='Latest inventory (per device)')

    latest_only = django_filters.BooleanFilter(
        method='_latest_only', label='Latest inventory')

    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device__id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )

    class Meta:
        model = Probe
        fields = ('id', 'device_descriptor', 'site_descriptor', 'location_descriptor', 'part', 'name',
                  'serial', 'device', 'site', 'location', 'description', 'category')

    def search(self, queryset, name, value):
        device_descriptor = Q(device_descriptor__icontains=value)
        site_descriptor = Q(site_descriptor__icontains=value)
        location_descriptor = Q(location_descriptor__icontains=value)
        part = Q(part__icontains=value)
        name = Q(name__icontains=value)
        serial = Q(serial__icontains=value)
        description = Q(description__icontains=value)
        return queryset.filter(device_descriptor | part | name | serial | description | site_descriptor | location_descriptor)

    def _latest_only_per_device(self, queryset, name, value):
        if value == True:
            latest_inventory_pks = Probe.objects.all().order_by(
                'serial', 'device_id', '-time').distinct('serial', 'device_id').values('pk')
            # latest_inventory_pks = Probe.objects.all().distinct('serial').order_by('serial', '-time').values('pk')
            return queryset.filter(pk__in=latest_inventory_pks)

        else:
            return queryset

    def _latest_only(self, queryset, name, value):
        if value == True:
            latest_inventory_pks = Probe.objects.all().distinct(
                'serial').order_by('serial', '-time').values('pk')
            return queryset.filter(pk__in=latest_inventory_pks)
        else:
            return queryset


# Contractor
class ContractorFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()

    name = django_filters.CharFilter(lookup_expr="icontains")
    company = django_filters.CharFilter(lookup_expr="icontains")
    address = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Contractor
        fields = ('id', 'name', 'company', 'address')

    def search(self, queryset, name, value):
        name = Q(name__icontains=value)
        company = Q(company__icontains=value)
        address = Q(address__icontains=value)
        return queryset.filter(name | company | address)


# Contract
class ContractFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()
    name = django_filters.CharFilter(lookup_expr="exact", field_name='name')
    name__ic = django_filters.CharFilter(
        field_name='name', lookup_expr="icontains", label="Name Contains")
    name_internal = django_filters.CharFilter(lookup_expr="icontains")
    contractor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contractor__id',
        queryset=Contractor.objects.all(),
        to_field_name='id',
        label='Contractor (ID)',
    )
    contractor = django_filters.ModelMultipleChoiceFilter(
        field_name='contractor__name',
        queryset=Contractor.objects.all(),
        to_field_name='name',
        label='Contractor (name)',
    )

    type = django_filters.MultipleChoiceFilter(
        choices=ContractTypeChoices,
        required=False
    )

    price = django_filters.NumberFilter(
        required=False
    )
    signed__gte = django_filters.DateFilter(
        field_name='signed',
        lookup_expr='gte'
    )
    signed__lte = django_filters.DateFilter(
        field_name='signed',
        lookup_expr='lte'
    )
    signed = django_filters.DateFilter(
        field_name='signed',
        lookup_expr='contains'
    )
    accepted__gte = django_filters.DateFilter(
        field_name='accepted',
        lookup_expr='gte'
    )
    accepted__lte = django_filters.DateFilter(
        field_name='accepted',
        lookup_expr='lte'
    )
    accepted = django_filters.DateFilter(
        field_name='accepted',
        lookup_expr='contains'
    )
    invoicing_start__gte = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='gte'
    )
    invoicing_start__lte = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='lte'
    )
    invoicing_start = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='contains'
    )
    invoicing_end__gte = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='gte'
    )
    invoicing_end__lte = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='lte'
    )
    invoicing_end = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='contains'
    )
    parent_id = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__id',
        queryset=Contract.objects.all(),
        to_field_name='id',
        label='Contract (ID)',
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__name',
        queryset=Contract.objects.all(),
        to_field_name='name',
        label='Contract (name)',
    )
    contract_type = django_filters.MultipleChoiceFilter(
        choices=(('All', 'All'), ('Contract', 'Contract'),
                 ('Subcontract', 'Subcontract')),
        required=False,
        label='Contract type',
        method='_contract_type',
    )

    master_contracts = django_filters.BooleanFilter(
        method='_master_contracts', label='Master contracts only')

    class Meta:
        model = Contract
        fields = ('id', 'name', 'name_internal', 'contractor', 'type', 'price',
                  'signed', 'accepted', 'invoicing_start', 'invoicing_end')

    def search(self, queryset, name, value):
        name = Q(name__icontains=value)
        name_internal = Q(name_internal__icontains=value)
        return queryset.filter(name | name_internal)

    def _master_contracts(self, queryset, name, value):
        if value == True:
            return queryset.filter(parent=None)
        else:
            return queryset

    def _contract_type(self, queryset, name, value):
        if value == ['All']:
            return queryset
        elif value == ['Contract']:
            return queryset.filter(parent=None)
        elif value == ['Subcontract']:
            return queryset.exclude(parent=None)
        else:
            return queryset


# Invoice
class InvoiceFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()
    name = django_filters.CharFilter(lookup_expr="exact", field_name='name')
    name__ic = django_filters.CharFilter(
        field_name='name', lookup_expr="icontains", label="Name Contains")
    name_internal = django_filters.CharFilter(lookup_expr="icontains")
    project = django_filters.CharFilter(lookup_expr="icontains")

    contract_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contract__id',
        queryset=Contract.objects.all(),
        to_field_name='id',
        label='Contract (ID)',
    )
    contract = django_filters.ModelMultipleChoiceFilter(
        field_name='contract__name',
        queryset=Contract.objects.all(),
        to_field_name='name',
        label='Contract (name)',
    )

    # TODO: forms.DecimalField
    price = django_filters.NumberFilter(
        required=False
    )

    invoicing_start__gte = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='gte'
    )
    invoicing_start__lte = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='lte'
    )
    invoicing_start = django_filters.DateFilter(
        field_name='invoicing_start',
        lookup_expr='contains'
    )
    invoicing_end__gte = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='gte'
    )
    invoicing_end__lte = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='lte'
    )
    invoicing_end = django_filters.DateFilter(
        field_name='invoicing_end',
        lookup_expr='contains'
    )

    class Meta:
        model = Invoice
        fields = ('id', 'name', 'name_internal', 'project', 'contract',
                  'price', 'invoicing_start', 'invoicing_end')

    def search(self, queryset, name, value):
        name = Q(name__icontains=value)
        name_internal = Q(name_internal__icontains=value)
        return queryset.filter(name | name_internal)

# Component
class ComponentFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()
    serial = django_filters.CharFilter(
        lookup_expr="iexact", field_name='serial')
    serial_actual = django_filters.CharFilter(
        lookup_expr="iexact", field_name='serial_actual')
    partnumber = django_filters.CharFilter(
        lookup_expr="iexact", field_name='partnumber')
    device = django_filters.ModelMultipleChoiceFilter(
        required=False,
        field_name='device__id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device (ID)')
    location = django_filters.ModelMultipleChoiceFilter(
        required=False,
        field_name='location__id',
        queryset=Location.objects.all(),
        to_field_name='id',
        label='Device (ID)')    
    inventory_item = django_filters.ModelMultipleChoiceFilter(
        required=False, 
        field_name='inventory_item__id',
        queryset=InventoryItem.objects.all(),
        to_field_name='id',
        label='Inventory Item (ID)')
    asset_number = django_filters.CharFilter(
        lookup_expr="icontains", field_name='asset_number')
    project = django_filters.CharFilter(lookup_expr="icontains")
    vendor = django_filters.CharFilter(
        lookup_expr="icontains", field_name='vendor')
    price = django_filters.NumberFilter(
        required=False,
        field_name='price',
        lookup_expr='exact',
    )
    price__gte = django_filters.NumberFilter(
        required=False,
        field_name='price',
        lookup_expr='gte',
    )
    price__lte = django_filters.NumberFilter(
        required=False,
        field_name='price',
        lookup_expr='lte',
    )
    quantity = django_filters.NumberFilter(
        required=False,
        field_name='quantity',
        lookup_expr='exact',
    )
    quantity__gte = django_filters.NumberFilter(
        required=False,
        field_name='quantity',
        lookup_expr='gte',
    )
    quantity__lte = django_filters.NumberFilter(
        required=False,
        field_name='quantity',
        lookup_expr='lte',
    )
    order_contract = django_filters.ModelMultipleChoiceFilter(
        field_name='order_contract__id',
        queryset=Contract.objects.all(),
        to_field_name='id',
        label='Order Contract (ID)',
    )
    warranty_start = django_filters.DateFilter(
        field_name='warranty_start',
        lookup_expr='contains'
    )
    warranty_start__gte = django_filters.DateFilter(
        field_name='warranty_start',
        lookup_expr='gte'
    )
    warranty_start__lte = django_filters.DateFilter(
        field_name='warranty_start',
        lookup_expr='lte'
    )
    warranty_end = django_filters.DateFilter(
        field_name='warranty_end',
        lookup_expr='contains'
    )
    warranty_end__gte = django_filters.DateFilter(
        field_name='warranty_end',
        lookup_expr='gte'
    )
    warranty_end__lte = django_filters.DateFilter(
        field_name='warranty_end',
        lookup_expr='lte'
    )

    class Meta:
        model = Component
        fields = ('id', 'serial', 'serial_actual', 'partnumber', 'asset_number',
                  'project', 'device', 'site', 'vendor', 'price',
                  'order_contract', 'warranty_start', 'warranty_end', "inventory_item")

    def search(self, queryset, name, value):
        serial = Q(serial__icontains=value)
        serial_actual = Q(serial_actual__icontains=value)
        device = Q(device__name__icontains=value)
        project = Q(project__icontains=value)
        site = Q(site__name__icontains=value)
        vendor = Q(vendor__icontains=value)
        order_contract = Q(order_contract__name__icontains=value)
        return queryset.filter(serial | serial_actual | project | site | vendor | order_contract | device)


# ComponentService
class ComponentServiceFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    tag = TagFilter()
    service_start = django_filters.DateFilter(
        field_name='service_start',
        lookup_expr='contains'
    )
    service_start__gte = django_filters.DateFilter(
        field_name='service_start',
        lookup_expr='gte'
    )
    service_start__lte = django_filters.DateFilter(
        field_name='service_start',
        lookup_expr='lte'
    )
    service_end = django_filters.DateFilter(
        field_name='service_end',
        lookup_expr='contains'
    )
    service_end__gte = django_filters.DateFilter(
        field_name='service_end',
        lookup_expr='gte'
    )
    service_end__lte = django_filters.DateFilter(
        field_name='service_end',
        lookup_expr='lte'
    )
    service_param = django_filters.CharFilter(
        lookup_expr="icontains", field_name='service_param')
    service_price = django_filters.NumberFilter(
        required=False,
        field_name='service_price',
        lookup_expr='exact',
    )
    service_price__gte = django_filters.NumberFilter(
        required=False,
        field_name='service_price',
        lookup_expr='gte',
    )
    service_price__lte = django_filters.NumberFilter(
        required=False,
        field_name='service_price',
        lookup_expr='lte',
    )
    service_category = django_filters.CharFilter(
        lookup_expr="icontains", field_name='service_category')
    service_category_vendor = django_filters.CharFilter(
        lookup_expr="icontains", field_name='service_category_vendor')
    component = django_filters.ModelMultipleChoiceFilter(
        field_name='component__id',
        queryset=Component.objects.all(),
        to_field_name='id',
        label='Component (ID)',
    )
    contract = django_filters.ModelMultipleChoiceFilter(
        field_name='contract__id',
        queryset=Contract.objects.all(),
        to_field_name='id',
        label='Contract (ID)',
    )

    class Meta:
        model = ComponentService
        fields = ('id', 'service_start', 'service_end', 'service_param',
                  'service_price', 'service_category', 'service_category_vendor',
                  'component', 'contract')

    def search(self, queryset, name, value):
        service_param = Q(service_param__icontains=value)
        service_category = Q(service_category__icontains=value)
        service_category_vendor = Q(service_category_vendor__icontains=value)
        component = Q(component__serial__icontains=value)
        contract = Q(contract__name__icontains=value)
        return queryset.filter(service_param | service_category | service_category_vendor | component | contract)
