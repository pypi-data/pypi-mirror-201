"""Ingestor for netmiko_cisco_nxos_show_inventory."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"


def ingest(log):
    """Processing parsed output."""
    device_o = log.discoverable.device

    for item in log.parsed_output:
        # See https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_nxos/show_inventory # pylint: disable=line-too-long
        part_description = item.get("name")
        part_serial_number = item.get("sn")
        # part_id = item.get("pid")

        if "chassis" in part_description.lower():
            # Chassis Serial Number
            device_o.serial = part_serial_number
            device_o.save()
            break

    # Update the log
    log.ingested = True
    log.save()
