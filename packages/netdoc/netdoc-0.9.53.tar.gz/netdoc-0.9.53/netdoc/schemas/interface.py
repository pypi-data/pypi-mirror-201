"""Schema validation for Interface."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from jsonschema import validate, FormatChecker

from ipam.models import VLAN as VLAN_model, VRF as VRF_model
from dcim.models import Device as Device_model, Interface as Interface_model
from dcim.choices import (
    InterfaceTypeChoices,
    InterfaceDuplexChoices,
    InterfaceModeChoices,
)

from netdoc import utils
from netdoc.schemas import vlan, prefix, ipaddress


def get_interface_types():
    """Return Interface types."""
    types = []
    for key, value in InterfaceTypeChoices():  # pylint: disable=unused-variable
        for key1, value1 in value:  # pylint: disable=unused-variable
            types.append(key1)
    return types


def get_schema():
    """Return the JSON schema to validate Device data."""
    return {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "device_id": {
                "type": "integer",
                "enum": list(Device_model.objects.all().values_list("id", flat=True)),
            },
            "type": {
                "type": "string",
                "enum": get_interface_types(),
            },
            "speed": {
                "type": "integer",
            },
            "duplex": {
                "type": "string",
                "enum": [key for key, value in InterfaceDuplexChoices()],
            },
            "vrf_id": {
                "type": "integer",
                "enum": list(VRF_model.objects.all().values_list("id", flat=True)),
            },
            "mac_address": {
                "type": "string",
            },
            "mtu": {
                "type": "integer",
            },
            "enabled": {
                "type": "boolean",
            },
            "parent_id": {
                "type": "integer",
                "enum": list(
                    Interface_model.objects.all().values_list("id", flat=True)
                ),
            },
            "bridge_id": {
                "type": "integer",
                "enum": list(
                    Interface_model.objects.all().values_list("id", flat=True)
                ),
            },
            "lag_id": {
                "type": "integer",
                "enum": list(
                    Interface_model.objects.all().values_list("id", flat=True)
                ),
            },
            "mode": {
                "type": "string",
                "enum": [key for key, value in InterfaceModeChoices()],
            },
            "untagged_vlan_id": {
                "type": "integer",
                "enum": list(VLAN_model.objects.all().values_list("vid", flat=True)),
            },
            "tagged_vlan_ids": {
                "type": "array",
                "item": {
                    "type": "integer",
                    "enum": list(
                        VLAN_model.objects.all().values_list("vid", flat=True)
                    ),
                },
            },
        },
    }


def get_schema_create():
    """Return the JSON schema to validate new Device objects."""
    schema = get_schema()
    schema["required"] = [
        "name",
        "type",
        "device_id",
    ]
    return schema


def create(int_type="other", **kwargs):
    """Create an Interface."""
    # The following are updated in update_mode
    if "mode" in kwargs:
        del kwargs["mode"]
    if "untagged_vlan_id" in kwargs:
        del kwargs["untagged_vlan_id"]
    if "tagged_vlan_ids" in kwargs:
        del kwargs["tagged_vlan_ids"]

    data = {
        **kwargs,
        "type": int_type,  # Default type is other
        "label": utils.normalize_interface_label(kwargs.get("name")),  # Set label
    }

    data = utils.delete_empty_keys(data)
    obj = utils.object_create(Interface_model, **data)
    return obj


def get(device_id, label):
    """Return an Interface."""
    obj = utils.object_get_or_none(Interface_model, device__id=device_id, label=label)
    return obj


def get_list(**kwargs):
    """Get a list of Interface objects."""
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    result = utils.object_list(Interface_model, **kwargs)
    return result


def update(obj, **kwargs):
    """Update an Interface."""
    update_always = [
        "name",
        "description",
        "speed",
        "duplex",
        "vrf_id",
        "mac_address",
        "mtu",
        "enabled",
        "parent_id",
        "bridge_id",
        "lag_id",
        "parent_id",
        "bridge_id",
        "lag_id",
        "label",
    ]
    if obj.type == "other":
        # Updating Interface type only if current value is other
        # to avoid overwriting custom options.
        update_always.append("type")

    data = {
        **kwargs,
        "label": utils.normalize_interface_label(kwargs.get("name"))
        if kwargs.get("name")
        else None,  # Set label if name is updated
    }

    data = utils.delete_empty_keys(data)
    validate(data, get_schema(), format_checker=FormatChecker())
    kwargs_always = utils.filter_keys(data, update_always)
    obj = utils.object_update(obj, **kwargs_always)
    return obj


def update_mode(obj, mode=None, untagged_vlan=None, tagged_vlans=None):
    """Update an Interface mode.

    VLANs must exist.
    """
    if not tagged_vlans:
        tagged_vlans = []

    if mode == "tagged" and tagged_vlans and len(tagged_vlans) >= 4093:
        # Trunk with all VLANs (override mode)
        # In some switch the trunk is excluding native VLAN, so total is 4093.
        obj.mode = "tagged-all"
        obj.save()
    elif mode == "tagged" and tagged_vlans:
        # Trunk with some VLANs
        # Get current VLAN IDs and compare them with tagged_vlans
        for vid in tagged_vlans:
            # Add missing VLANs
            if not obj.tagged_vlans.filter(vid=vid):
                vlan_qs = vlan.get_list(vid=vid)
                if vlan_qs:
                    vlan_o = vlan_qs.pop()
                else:
                    # VLAN does not exist, creating one with default name
                    vlan_o = vlan.create(vid=vid, name=f"VLAN{vid:04d}")
                obj.tagged_vlans.add(vlan_o)

        for vlan_o in obj.tagged_vlans.all():
            # Remove unconfigured VLANs
            if vlan_o.vid not in tagged_vlans:
                obj.tagged_vlans.remove(vlan_o)
        obj.mode = mode
        obj.save()

    if untagged_vlan and mode in ["tagged", "access"]:
        # Get current VLAN IDs and compare them with untagged_vlan
        if not obj.untagged_vlan or obj.untagged_vlan != untagged_vlan:
            # A VLAN with a different VLAN ID is set
            vlan_qs = vlan.get_list(vid=untagged_vlan)
            if vlan_qs:
                vlan_o = vlan_qs.pop()
            else:
                # VLAN does not exist, creating one with default name
                vlan_o = vlan.create(vid=untagged_vlan, name=f"VLAN{untagged_vlan:04d}")
            data = {
                "mode": mode,
                "untagged_vlan": vlan_o,
            }
            obj = utils.object_update(obj, **data, force=False)

    return obj


def update_addresses(obj, ip_addresses=None):
    """Update Interface IP Addresses."""
    previous_ip_addresses_qs = obj.ip_addresses.all()
    previous_ip_addresses = [str(ip.address) for ip in previous_ip_addresses_qs]
    site_id = obj.device.site.id if obj.device.site else None
    vrf_id = obj.vrf.id if obj.vrf else None

    for ip_address in ip_addresses:
        if not ip_address:
            # Skip empty IP addresses
            continue
        # Get or create Prefix
        prefix_o = prefix.get(prefix=ip_address)
        if not prefix_o:
            prefix.create(prefix=ip_address, vrf_id=vrf_id, site_id=site_id)

        if ip_address not in previous_ip_addresses:
            # Get or create IPAddress
            ip_address_list = ipaddress.get_list(address=ip_address, vrf_id=vrf_id)
            if ip_address_list:
                ip_address_o = ip_address_list.pop()
            else:
                ip_address_o = ipaddress.create(address=ip_address, vrf_id=vrf_id)

            # Add missing IP address
            obj.ip_addresses.add(ip_address_o)

    for ip_address in previous_ip_addresses_qs:
        if str(ip_address) not in ip_addresses:
            # Get Interface IP Address objects
            ip_address_o = obj.ip_addresses.get(
                address__net_contains_or_equals=ip_address
            )
            # Remove unconfigured IP Address
            obj.ip_addresses.remove(ip_address_o)

    obj.save()
    return obj
