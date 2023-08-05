from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from netbox.models.features import (CustomFieldsMixin, CustomLinksMixin,
                                    CustomValidationMixin,
                                    ExportTemplatesMixin, JournalingMixin,
                                    TagsMixin, WebhooksMixin)
from utilities.choices import ChoiceSet
from utilities.querysets import RestrictedQuerySet


class ContractTypeChoices(ChoiceSet):
    key = 'Contract.type'

    CHOICES = [
        ('supply', 'Supply Contract', 'green'),
        ('order', 'Order', 'red'),
        ('service', 'Service Contract', 'orange'),
        ('other', 'Other', 'blue')
    ]


class Probe(CustomFieldsMixin, CustomLinksMixin, CustomValidationMixin, ExportTemplatesMixin, JournalingMixin, TagsMixin, WebhooksMixin, models.Model):
    objects = RestrictedQuerySet.as_manager()

    time = models.DateTimeField()
    
    creation_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    device_descriptor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    site_descriptor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    location_descriptor = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    part = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=255
    )

    serial = models.CharField(
        max_length=255
    )

    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    location = models.ForeignKey(
        to='dcim.Location',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    discovered_data = models.JSONField(
        default=dict,
        blank=True
    )
    category = models.CharField(
        blank=True,
        null=True,
        max_length=255
    )

    class Meta:
        ordering = ('name', 'serial', 'time', 'part', 'description', 'device_descriptor', 'device',
                    'site_descriptor', 'site', 'location_descriptor', 'location', 'category', 'discovered_data',)

    def __str__(self):
        return f'{self.serial} - {self.name}'

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:probe', args=[self.pk])


class Contractor(NetBoxModel):
    objects = RestrictedQuerySet.as_manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name', 'company', 'address', 'comments',)

    def __str__(self):
        if self.company:
            return f'{self.name}: {self.company}'
        else:
            return f'{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:contractor', args=[self.pk])


class Contract(NetBoxModel):
    objects = RestrictedQuerySet.as_manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    name_internal = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    contractor = models.ForeignKey(
        to='inventory_monitor.contractor',  # Contractor,
        on_delete=models.PROTECT,
        related_name="contracts",
        blank=True,
        null=True,
    )

    type = models.CharField(
        max_length=50,
        choices=ContractTypeChoices
    )

    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )

    signed = models.DateField(
        blank=True,
        null=True,
    )

    accepted = models.DateField(
        blank=True,
        null=True,
    )

    invoicing_start = models.DateField(
        blank=True,
        null=True,
    )

    invoicing_end = models.DateField(
        blank=True,
        null=True,
    )

    parent = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='subcontracts',
        null=True,
        blank=True,
        verbose_name='Parent contract'
    )

    comments = models.TextField(
        blank=True
    )

    @property
    def contract_type(self):
        if self.parent:
            return "subcontract"
        else:
            return "contract"

    class Meta:
        ordering = ('name', 'name_internal', 'contractor', 'type', 'price',
                    'signed', 'accepted', 'invoicing_start', 'invoicing_end')

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        else:
            return f"{self.name}"

    def get_type_color(self):
        return ContractTypeChoices.colors.get(self.type)

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:contract', args=[self.pk])

    def clean(self):
        super().clean()

        # Validate - subcontract cannot set parent which is subcontract
        if self.parent and self.parent.parent:
            raise ValidationError(
                {'parent': "Subcontract cannot be set as Parent Contract"}
            )

        # Validate - if parent contract has different contractor
        if self.parent and self.parent.contractor != self.contractor:
            raise ValidationError(
                {'contractor': f"Contractor must be same as Parent contractor: {self.parent.contractor}"}
            )

        # Validate invoicing_start and invoicing_end
        if self.invoicing_start and self.invoicing_end and self.invoicing_start > self.invoicing_end:
            raise ValidationError(
                {'invoicing_start': f"Invoicing Start cannot be set after Invoicing End"}
            )


class Invoice(NetBoxModel):
    objects = RestrictedQuerySet.as_manager()

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    name_internal = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    project = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    contract = models.ForeignKey(
        to='inventory_monitor.contract',  # Contractor,
        on_delete=models.PROTECT,
        related_name="invoices",
        blank=False,
        null=False
    )

    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        blank=False,
        null=False,
        validators=[MinValueValidator(0)],
        default=0
    )

    invoicing_start = models.DateField(
        blank=True,
        null=True,
    )

    invoicing_end = models.DateField(
        blank=True,
        null=True,
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name', 'name_internal', 'contract',
                    'price', 'invoicing_start', 'invoicing_end')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:invoice', args=[self.pk])

    def clean(self):
        super().clean()

        # Validate invoicing_start and invoicing_end
        if self.invoicing_start and self.invoicing_end and self.invoicing_start > self.invoicing_end:
            raise ValidationError(
                {'invoicing_start': f"Invoicing Start cannot be set after Invoicing End"}
            )


class Component(NetBoxModel):
    objects = RestrictedQuerySet.as_manager()

    serial = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    serial_actual = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    partnumber = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    device = models.ForeignKey(
        to='dcim.device',
        on_delete=models.PROTECT,
        related_name="components",
        blank=True,
        null=True
    )

    # TODO: Asset Number
    asset_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    project = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )

    site = models.ForeignKey(
        to='dcim.site',  # Locality,
        on_delete=models.PROTECT,
        related_name="components",
        blank=True,
        null=True
    )

    location = models.ForeignKey(
        to='dcim.location',
        on_delete=models.PROTECT,
        related_name="components",
        blank=True,
        null=True
    )

    inventory_item = models.ForeignKey(
        to="dcim.inventoryitem",
        on_delete=models.PROTECT,
        related_name="components",
        blank=True,
        null=True
    )

    vendor = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=1,
        validators=[MinValueValidator(0)],
    )

    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        default=0
    )

    order_contract = models.ForeignKey(
        to='inventory_monitor.contract',  # Contractor,
        on_delete=models.PROTECT,
        related_name="components",
        blank=True,
        null=True
    )

    warranty_start = models.DateField(
        blank=True,
        null=True,
    )

    warranty_end = models.DateField(
        blank=True,
        null=True,
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('serial', 'serial_actual', 'partnumber',
                    'device', 'asset_number', 'project', 'site',
                    'location', 'inventory_item',
                    'vendor', 'quantity', 'price', 'order_contract',
                    'warranty_start', 'warranty_end')

    def __str__(self):
        return f"{self.serial}"

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:component', args=[self.pk])

    def clean(self):
        super().clean()


# Add Services class
"""
TODO:
CREATE TABLE `services` (
  PRIMARY KEY (`serviceId`),
  UNIQUE KEY `componentId_contract_id_serviceStart` (`componentId`,`contract_id`,`serviceStart`),
"""


class ComponentService(NetBoxModel):
    objects = RestrictedQuerySet.as_manager()

    service_start = models.DateField(
        blank=True,
        null=True,
    )

    service_end = models.DateField(
        blank=True,
        null=True,
    )

    service_param = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )

    service_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        default=0
    )

    service_category = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    service_category_vendor = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    component = models.ForeignKey(
        to='inventory_monitor.component',
        on_delete=models.PROTECT,
        related_name="services",
        blank=True,
        null=True
    )

    contract = models.ForeignKey(
        to='inventory_monitor.contract',
        on_delete=models.PROTECT,
        related_name="services",
        blank=True,
        null=True
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('service_start', 'service_end', 'service_param',
                    'service_price', 'service_category', 'service_category_vendor',
                    'component', 'contract')

    def __str__(self):
        return f"{self.pk}"

    def get_absolute_url(self):
        return reverse('plugins:inventory_monitor:componentservice', args=[self.pk])

    def clean(self):
        super().clean()
