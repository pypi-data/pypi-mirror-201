from extras.plugins import PluginMenu, PluginMenuItem

menu = PluginMenu(
    label='Inventory Monitor',
    icon_class="mdi mdi-monitor",
    groups=(
        ("Network Probe",
         (
             PluginMenuItem(
                 link="plugins:inventory_monitor:probe_list", link_text="Probes"),
         ),
         ),
        ("Contracts",
         (
             PluginMenuItem(
                 link='plugins:inventory_monitor:contractor_list', link_text='Contractors'),
             PluginMenuItem(
                 link='plugins:inventory_monitor:contract_list', link_text='Contracts'),
             PluginMenuItem(
                 link='plugins:inventory_monitor:invoice_list', link_text='Invoices'),
         ),
         ),
        ("Components",
         (
             PluginMenuItem(
                 link='plugins:inventory_monitor:component_list', link_text='Components'),
             PluginMenuItem(
                 link='plugins:inventory_monitor:componentservice_list', link_text='Services'),
         ),
         ),
    ),
)
