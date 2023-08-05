from dcim.api.serializers import (NestedDeviceSerializer,
                                  NestedLocationSerializer,
                                  NestedSiteSerializer)
from netbox.api.serializers import (NetBoxModelSerializer,
                                    WritableNestedSerializer)
from rest_framework import serializers

from ..models import (Component, ComponentService, Contract, Contractor,
                      Invoice, Probe)


class ProbeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:probe-detail'
    )
    device = NestedDeviceSerializer()
    site = NestedSiteSerializer(allow_null=True)
    location = NestedLocationSerializer(allow_null=True)

    class Meta:
        model = Probe
        fields = [
            'id',
            'url',
            'display',
            'name',
            'time',
            'serial',
            'part',
            'device_descriptor',
            'device',
            'site_descriptor',
            'site',
            'location_descriptor',
            'location',
            'description',
            'category',
            'discovered_data',
            'tags',
            'comments',
            'custom_fields',
            'creation_time'
        ]


class NestedProbeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:probe-detail'
    )

    class Meta:
        model = Probe
        fields = ['id', 'url', 'display', 'name', 'serial', 'time', 'creation_time']


class ContractorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:contractor-detail'
    )

    class Meta:
        model = Contractor
        fields = [
            'id',
            'url',
            'display',
            'name',
            'company',
            'address',
            'tags',
            'comments',
            'custom_fields',
        ]


class NestedContractorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:contractor-detail'
    )

    class Meta:
        model = Contractor
        fields = ['id', 'display', 'url', 'name', 'company', 'address']


class NestedContractSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:contract-detail'
    )

    contractor = NestedContractorSerializer()

    class Meta:
        model = Contract
        fields = ['id', 'url', 'display', 'name', 'name_internal', 'contractor', 'type',
                  'price', 'signed', 'accepted', 'invoicing_start', 'invoicing_end', 'parent']


class ContractSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:contract-detail'
    )
    contractor = NestedContractorSerializer()
    parent = NestedContractSerializer(allow_null=True)

    class Meta:
        model = Contract
        fields = [
            'id',
            'url',
            'display',
            'name',
            'name_internal',
            'contractor',
            'type',
            'contract_type',
            'price',
            'signed',
            'accepted',
            'invoicing_start',
            'invoicing_end',
            'parent',
            'tags',
            'comments',
            'custom_fields',
        ]


class InvoiceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:invoice-detail'
    )
    contract = NestedContractSerializer()

    class Meta:
        model = Invoice
        fields = [
            'id',
            'url',
            'display',
            'name',
            'name_internal',
            'project',
            'contract',
            'price',
            'invoicing_start',
            'invoicing_end',
            'tags',
            'comments',
            'custom_fields',
        ]


class NestedInvoiceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:invoice-detail'
    )

    class Meta:
        model = Invoice
        fields = ['id', 'url', 'display', 'name', 'name_internal']


class ComponentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:component-detail'
    )
    order_contract = NestedContractSerializer()

    class Meta:
        model = Component
        fields = [
            'id',
            'url',
            'display',
            'serial',
            'serial_actual',
            'partnumber',
            'asset_number',
            'project',
            'vendor',
            'quantity',
            'price',
            'warranty_start',
            'warranty_end',
            'order_contract',
            'tags',
            'comments',
            'custom_fields',
        ]


class NestedComponentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:component-detail'
    )
    order_contract = NestedContractSerializer()

    class Meta:
        model = Component
        fields = [
            'id',
            'url',
            'display',
            'serial',
            'serial_actual',
            'partnumber',
            'asset_number',
            'quantity',
            'price',
            'order_contract',
        ]


class ComponentServiceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:componentservice-detail'
    )
    contract = NestedContractSerializer()
    component = NestedComponentSerializer()

    class Meta:
        model = ComponentService
        fields = [
            'id',
            'url',
            'display',
            'service_start',
            'service_end',
            'service_param',
            'service_price',
            'service_category',
            'service_category_vendor',
            'component',
            'contract',
            'tags',
            'comments',
            'custom_fields',
        ]


class NestedComponentServiceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:inventory_monitor-api:componentservice-detail'
    )
    contract = NestedContractSerializer()
    component = NestedComponentSerializer()

    class Meta:
        model = ComponentService
        fields = [
            'id',
            'url',
            'display',
            'service_start',
            'service_end',
            'service_price',
            'component',
            'contract',
        ]
