from dcim.models import InventoryItem
from django.db.models import Count, OuterRef, Subquery
from extras.plugins import PluginTemplateExtension

from .models import Probe

# from django.conf import settings
# plugin_settings = settings.PLUGINS_CONFIG.get('inventory_monitor', {})


class DeviceProbeList(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        obj = self.context['object']

        # Latest inventory overall
        # latest_inventory_pks = Probe.objects.all()\
        #    .distinct('serial')\
        #    .order_by('serial', '-time')\
        #    .values('pk')

        # Latest inventory per device
        latest_inventory_pks = Probe.objects.all().order_by(
            'serial', 'device_id', '-time').distinct('serial', 'device_id').values('pk')

        device_probes = Probe.objects.filter(device=obj, pk__in=latest_inventory_pks)\
            .prefetch_related('tags', 'device')

        return self.render(
            'inventory_monitor/device_probes_include.html',
            extra_context={
                'device_probes': device_probes.order_by('-time')[:10],
                'total_device_probes_count': device_probes.count(),
            }
        )


class InventoryItemDuplicates(PluginTemplateExtension):
    model = 'dcim.inventoryitem'

    def right_page(self):
        obj = self.context['object']

        inv_duplicates = InventoryItem.objects.filter(serial=obj.serial)\
            .exclude(id=obj.id).order_by('-custom_field_data__inventory_monitor_last_probe')

        return self.render(
            'inventory_monitor/inventory_item_duplicates_include.html',
            extra_context={
                'current_inv': obj,
                'inv_duplicates': inv_duplicates,
                'inv_duplicates_count': inv_duplicates.count(),
            }
        )


class ImportComponentScriptButton(PluginTemplateExtension):
    model = 'inventory_monitor.component'

    def list_buttons(self):
        return self.render('inventory_monitor/import_component_button.html',
                           extra_context={
                               'url': '/extras/scripts/component_import.ImportComponent/'}
                           )


template_extensions = [DeviceProbeList,
                       InventoryItemDuplicates, ImportComponentScriptButton]
