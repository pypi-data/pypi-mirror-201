from dcim.models import Device, Location, Site, InventoryItem
from django import forms
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms import (BOOLEAN_WITH_BLANK_CHOICES, DatePicker,
                             DateTimePicker, DynamicModelMultipleChoiceField,
                             StaticSelect, TagFilterField)
from utilities.forms.fields import CommentField, DynamicModelChoiceField

from .models import Contract, Contractor, ContractTypeChoices, Invoice, Probe, Component, ComponentService

# Probe
class ProbeForm(NetBoxModelForm):
    comments = CommentField(
        label="Comments"
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = Probe
        fields = ('name', 'serial', 'time',  'category', 'part', 'device_descriptor', 'device',
                  'site_descriptor', 'site', 'location_descriptor', 'location', 'description', 'tags', 'comments',)


class ProbeFilterForm(NetBoxModelFilterSetForm):
    model = Probe

    # TODO: Add FilterSets, Add FilterForm
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Common', ('serial', 'category', 'device_descriptor', 'description')),
        ('Linked', ('device_id',)),
        ('Dates', ('time__gte', 'time__lte')),
        ('Misc', ('latest_only_per_device', 'latest_only')),
    )

    tag = TagFilterField(model)
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device')
    )
    serial = forms.CharField(
        required=False
    )
    device_descriptor = forms.CharField(
        required=False
    )
    category = forms.CharField(
        required=False
    )
    description = forms.CharField(
        required=False
    )
    time__gte = forms.DateTimeField(
        required=False,
        label=('Time From'),
        widget=DateTimePicker()
    )
    time__lte = forms.DateTimeField(
        required=False,
        label=('Time Till'),
        widget=DateTimePicker()
    )
    latest_only_per_device = forms.NullBooleanField(
        required=False,
        label='Latest inventory only (per device)',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    latest_only = forms.NullBooleanField(
        required=False,
        label='Latest inventory only',
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )


# Contractor
class ContractorForm(NetBoxModelForm):
    comments = CommentField(
        label="Comments"
    )

    class Meta:
        model = Contractor
        fields = ('name', 'company', 'address', 'tags', 'comments', 'tags')


class ContractorFilterForm(NetBoxModelFilterSetForm):
    model = Contractor

    tag = TagFilterField(model)

    name = forms.CharField(
        required=False
    )
    company = forms.CharField(
        required=False
    )
    address = forms.CharField(
        required=False
    )


# Contract
class ContractForm(NetBoxModelForm):
    comments = CommentField(
        label="Comments"
    )

    contractor = DynamicModelChoiceField(
        queryset=Contractor.objects.all(),
        required=True
    )

    parent = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        query_params={"parent_id": "null"},
        required=False,
        label=("Parent Contract")
    )

    signed = forms.DateField(
        required=False,
        label=('Signed'),
        widget=DatePicker()
    )

    accepted = forms.DateField(
        required=False,
        label=('Accepted'),
        widget=DatePicker()
    )

    invoicing_start = forms.DateField(
        required=False,
        label=('Invoicing Start'),
        widget=DatePicker()
    )

    invoicing_end = forms.DateField(
        required=False,
        label=('Invoicing End'),
        widget=DatePicker()
    )

    class Meta:
        model = Contract
        fields = ('name', 'name_internal', 'contractor', 'type', 'price', 'signed',
                  'accepted', 'invoicing_start',  'invoicing_end', 'parent', 'comments', 'tags')


class ContractFilterForm(NetBoxModelFilterSetForm):
    model = Contract

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Common', ('name', 'name_internal', 'contract_type', 'type',)),
        ('Linked', ('contractor_id', 'parent_id')),
        ('Dates', ('signed', 'signed__gte', 'signed__lte', 'accepted', 'accepted__gte', 'accepted__lte', 'invoicing_start',
         'invoicing_start__gte', 'invoicing_start__lte', 'invoicing_end', 'invoicing_end__gte', 'invoicing_end__lte')),
    )

    tag = TagFilterField(model)

    name = forms.CharField(
        required=False
    )

    name_internal = forms.CharField(
        required=False
    )
    contract_type = forms.ChoiceField(
        label='Contract Type',
        choices=(('All', 'All'), ('Contract', 'Contract'),
                 ('Subcontract', 'Subcontract')),
        required=False,
        initial='All'
    )
    contractor_id = DynamicModelMultipleChoiceField(
        queryset=Contractor.objects.all(),
        required=False,
        label=_('Contractor')
    )

    parent_id = DynamicModelMultipleChoiceField(
        queryset=Contract.objects.filter(parent_id=None),
        required=False,
        label=_('Parent Contract')
    )

    type = forms.MultipleChoiceField(
        choices=ContractTypeChoices,
        required=False
    )

    price = forms.DecimalField(
        required=False
    )

    accepted__gte = forms.DateField(
        required=False,
        label=('Accepted From'),
        widget=DatePicker()
    )
    accepted__lte = forms.DateField(
        required=False,
        label=('Accepted Till'),
        widget=DatePicker()
    )
    accepted = forms.DateField(
        required=False,
        label=('Accepted'),
        widget=DatePicker()
    )

    signed__gte = forms.DateField(
        required=False,
        label=('Signed From'),
        widget=DatePicker()
    )
    signed__lte = forms.DateField(
        required=False,
        label=('Signed Till'),
        widget=DatePicker()
    )
    signed = forms.DateField(
        required=False,
        label=('Signed'),
        widget=DatePicker()
    )

    invoicing_start__gte = forms.DateField(
        required=False,
        label=('Invoicing Start: From'),
        widget=DatePicker()
    )
    invoicing_start__lte = forms.DateField(
        required=False,
        label=('Invoicing Start: Till'),
        widget=DatePicker()
    )
    invoicing_start = forms.DateField(
        required=False,
        label=('Invoicing Start'),
        widget=DatePicker()
    )

    invoicing_end__gte = forms.DateField(
        required=False,
        label=('Invoicing End: From'),
        widget=DatePicker()
    )
    invoicing_end__lte = forms.DateField(
        required=False,
        label=('Invoicing End: Till'),
        widget=DatePicker()
    )
    invoicing_end = forms.DateField(
        required=False,
        label=('Invoicing End'),
        widget=DatePicker()
    )


# Invoice
class InvoiceForm(NetBoxModelForm):
    comments = CommentField(
        label="Comments"
    )

    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=True
    )

    invoicing_start = forms.DateField(
        required=False,
        label=('Invoicing Start'),
        widget=DatePicker()
    )

    invoicing_end = forms.DateField(
        required=False,
        label=('Invoicing End'),
        widget=DatePicker()
    )

    class Meta:
        model = Invoice
        fields = ('name', 'name_internal', 'project', 'contract', 'price',
                  'invoicing_start',  'invoicing_end', 'comments', 'tags')


class InvoiceFilterForm(NetBoxModelFilterSetForm):
    model = Invoice

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Common', ('name', 'name_internal', 'project',)),
        ('Linked', ('contract_id',)),
        ('Dates', ('invoicing_start', 'invoicing_start__gte', 'invoicing_start__lte',
         'invoicing_end', 'invoicing_end__gte', 'invoicing_end__lte')),
    )

    tag = TagFilterField(model)

    name = forms.CharField(
        required=False
    )

    name_internal = forms.CharField(
        required=False
    )

    project = forms.CharField(
        required=False
    )

    contract_id = DynamicModelMultipleChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        label=_('Contract')
    )

    price = forms.DecimalField(
        required=False
    )

    invoicing_start__gte = forms.DateField(
        required=False,
        label=('Invoicing Start: From'),
        widget=DatePicker()
    )
    invoicing_start__lte = forms.DateField(
        required=False,
        label=('Invoicing Start: Till'),
        widget=DatePicker()
    )
    invoicing_start = forms.DateField(
        required=False,
        label=('Invoicing Start'),
        widget=DatePicker()
    )

    invoicing_end__gte = forms.DateField(
        required=False,
        label=('Invoicing End: From'),
        widget=DatePicker()
    )
    invoicing_end__lte = forms.DateField(
        required=False,
        label=('Invoicing End: Till'),
        widget=DatePicker()
    )
    invoicing_end = forms.DateField(
        required=False,
        label=('Invoicing End'),
        widget=DatePicker()
    )

# Component
class ComponentForm(NetBoxModelForm):
    fieldsets = (
        ('Component', ('serial', 'serial_actual', 'partnumber',
         'asset_number', 'project', 'price', 'vendor', 'quantity')),
        ('Linked', ('order_contract', 'device', 'site', 'location', 'inventory_item')),
        ('Dates', ('warranty_start', 'warranty_end')),
        ('Tag', ('tags',)),
    )

    comments = CommentField(
        label="Comments"
    )

    serial = forms.CharField(
        required=True,
        label='Serial',
        widget=forms.TextInput(attrs={'placeholder': 'Serial'}),
    )

    serial_actual = forms.CharField(
        required=True,
        label='Serial Actual',
        widget=forms.TextInput(attrs={'placeholder': 'Serial Actual'}),
    )

    partnumber = forms.CharField(
        required=False,
        label='Part Number',
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label='Device',
    )

    inventory_item = DynamicModelChoiceField(
        queryset=InventoryItem.objects.all(),
        required=False,
        label='Inventory Item',
    )

    asset_number = forms.CharField(
        required=False,
        label='Inventory / AN',
    )

    project = forms.CharField(
        required=False,
        label='Project',
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label='Site',
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label='Location',
    )

    vendor = forms.CharField(
        required=False,
        label='Vendor',
    )

    quantity = forms.IntegerField(
        required=True,
        label='Items',
        initial=1,
        min_value=1
    )

    price = forms.DecimalField(
        required=True,
        label='Price',
        initial=0,
        min_value=0,
        decimal_places=2,
    )

    order_contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        label='Order Contract',
    )

    warranty_start = forms.DateField(
        required=False,
        label=('Warranty Start'),
        widget=DatePicker()
    )

    warranty_end = forms.DateField(
        required=False,
        label=('Warranty End'),
        widget=DatePicker(),
    )

    class Meta:
        model = Component
        fields = ('serial', 'serial_actual', 'partnumber', 'device', 'asset_number',
                  'site', 'location', 'inventory_item',
                  'project', 'vendor', 'quantity', 'price', 'order_contract',
                  'warranty_start', 'warranty_end', 'comments', 'tags')


class ComponentFilterForm(NetBoxModelFilterSetForm):
    model = Component

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Linked', ('order_contract', 'site', 'location', 'device', 'inventory_item')),
        ('Dates', ('warranty_start', 'warranty_start__gte', 'warranty_start__lte',
         'warranty_end', 'warranty_end__gte', 'warranty_end__lte')),
        ('Component', ('serial', 'serial_actual',
         'partnumber', 'asset_number', 'project', 'vendor',)),
        ('Items', ('quantity', 'quantity__gte', 'quantity__lte')),
        ('Price', ('price', 'price__gte', 'price__lte')),
    )

    serial = forms.CharField(
        required=False
    )

    tag = TagFilterField(model)

    serial_actual = forms.CharField(
        required=False
    )

    partnumber = forms.CharField(
        required=False
    )

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device')
    )

    inventory_item = DynamicModelMultipleChoiceField(
        queryset=InventoryItem.objects.all(),
        required=False,
        label=_('Inventory Item')
    )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )

    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_('Location')
    )

    quantity = forms.IntegerField(
        required=False,
        label='Items'
    )

    quantity__gte = forms.IntegerField(
        required=False,
        label=('Items: From')
    )

    quantity__lte = forms.IntegerField(
        required=False,
        label=('Items: Till')
    )

    asset_number = forms.CharField(
        required=False,
        label='Asset Number',
    )

    project = forms.CharField(
        required=False,
        label='Project',
    )

    vendor = forms.CharField(
        required=False,
        label='Vendor',
    )

    price = forms.DecimalField(
        required=False
    )

    price__gte = forms.DecimalField(
        required=False,
        label=('Price: From'),
    )

    price__lte = forms.DecimalField(
        required=False,
        label=('Price: Till'),
    )

    order_contract = DynamicModelMultipleChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        label=_('Order Contract')
    )

    warranty_start = forms.DateField(
        required=False,
        label=('Warranty Start'),
        widget=DatePicker()
    )

    warranty_start__gte = forms.DateField(
        required=False,
        label=('Warranty Start: From'),
        widget=DatePicker()
    )

    warranty_start__lte = forms.DateField(
        required=False,
        label=('Warranty Start: Till'),
        widget=DatePicker()
    )

    warranty_end = forms.DateField(
        required=False,
        label=('Warranty End'),
        widget=DatePicker()
    )

    warranty_end__gte = forms.DateField(
        required=False,
        label=('Warranty End: From'),
        widget=DatePicker()
    )

    warranty_end__lte = forms.DateField(
        required=False,
        label=('Warranty End: Till'),
        widget=DatePicker()
    )


# ComponentService
class ComponentServiceForm(NetBoxModelForm):
    fieldsets = (
        ('Linked', ('contract', 'component')),
        ('Dates', ('service_start', 'service_end')),
        ('Service Params', ('service_price', 'service_category',
         'service_category_vendor', 'service_param')),
        ('Tag', ('tags',)),
    )

    comments = CommentField(
        label="Comments"
    )

    service_start = forms.DateField(
        required=False,
        label=('Service Start'),
        widget=DatePicker()
    )

    service_end = forms.DateField(
        required=False,
        label=('Service End'),
        widget=DatePicker()
    )

    service_param = forms.CharField(
        required=False,
        label='Service Param',
    )

    service_price = forms.DecimalField(
        required=False,
        label='Service Price',
        initial=0,
        min_value=0,
        decimal_places=2,
    )

    service_category = forms.CharField(
        required=False,
        label='Service Category',
    )

    service_category_vendor = forms.CharField(
        required=False,
        label='Service Category Vendor',
    )

    component = DynamicModelChoiceField(
        queryset=Component.objects.all(),
        required=True,
        label='Service Component',
    )

    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=True,
        label='Service Contract',
    )

    class Meta:
        model = ComponentService
        fields = ('service_start', 'service_end', 'service_param',
                  'service_price', 'service_category', 'service_category_vendor',
                  'component', 'contract', 'comments', 'tags')


class ComponentServiceFilterForm(NetBoxModelFilterSetForm):
    model = ComponentService

    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        ('Linked', ('component', 'contract')),
        ('Dates', ('service_start', 'service_start__gte', 'service_start__lte',
         'service_end', 'service_end__gte', 'service_end__lte')),
        ('Service', ('service_param', 'service_price',
         'service_category', 'service_category_vendor')),
    )

    tag = TagFilterField(model)

    service_start = forms.DateField(
        required=False,
        label=('Service Start'),
        widget=DatePicker()
    )
    service_start__gte = forms.DateField(
        required=False,
        label=('Service Start: From'),
        widget=DatePicker()
    )
    service_start__lte = forms.DateField(
        required=False,
        label=('Service Start: Till'),
        widget=DatePicker()
    )
    service_end = forms.DateField(
        required=False,
        label=('Service End'),
        widget=DatePicker()
    )
    service_end__gte = forms.DateField(
        required=False,
        label=('Service End: From'),
        widget=DatePicker()
    )
    service_end__lte = forms.DateField(
        required=False,
        label=('Service End: Till'),
        widget=DatePicker()
    )
    service_param = forms.CharField(
        required=False,
        label='Service Param',
    )
    service_price = forms.DecimalField(
        required=False,
        label='Service Price',
        initial=0,
        min_value=0,
        decimal_places=2,
    )
    service_category = forms.CharField(
        required=False,
        label='Service Category',
    )
    service_category_vendor = forms.CharField(
        required=False,
        label='Service Category Vendor',
    )

    component = DynamicModelMultipleChoiceField(
        queryset=Component.objects.all(),
        required=False,
        label=_('Component')
    )
    contract = DynamicModelMultipleChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        label=_('Contract')
    )
