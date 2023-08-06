"""Schema validation for Device."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from jsonschema import validate, FormatChecker

from dcim.models import (
    DeviceRole as DeviceRole_model,
    DeviceType as DeviceType_model,
    Manufacturer as Manufacturer_model,
    Site,
    Device,
)

from netdoc import utils
from netdoc.schemas import manufacturer as manufacturer_api, devicerole, devicetype


def get_schema():
    """Return the JSON schema to validate Device data."""
    return {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "transform": ["toUpperCase"],
            },
            "device_role_id": {
                "type": "integer",
                "enum": list(
                    DeviceRole_model.objects.all().values_list("id", flat=True)
                ),
            },
            "manufacturer_id": {
                "type": "integer",
                "enum": list(
                    Manufacturer_model.objects.all().values_list("id", flat=True)
                ),
            },
            "device_type_id": {
                "type": "integer",
                "enum": list(
                    DeviceType_model.objects.all().values_list("id", flat=True)
                ),
            },
            "serial_number": {
                "type": "string",
                "transform": ["toUpperCase"],
            },
            "site_id": {
                "type": "integer",
                "enum": list(Site.objects.all().values_list("id", flat=True)),
            },
        },
    }


def get_schema_create():
    """Return the JSON schema to validate new Device objects."""
    schema = get_schema()
    schema["required"] = [
        "name",
        "device_role_id",
        "device_type_id",
        "site_id",
    ]
    return schema


def create(manufacturer="Unknown", **kwargs):
    """Create a Device.

    Before need to get or create Manufacturer, DeviceModel, and DeviceType.
    """
    manufacturer_o = manufacturer_api.get(name=manufacturer)
    if not manufacturer_o:
        manufacturer_o = manufacturer_api.create(name=manufacturer)

    devicerole_o = devicerole.get(name="Unknown")
    if not devicerole_o:
        devicerole_o = devicerole.create(name="Unknown")

    devicetype_o = devicetype.get(model="Unknown", manufacturer_id=manufacturer_o.id)
    if not devicetype_o:
        devicetype_o = devicetype.create(
            model="Unknown", manufacturer_id=manufacturer_o.id
        )

    kwargs.update(
        {
            "device_role_id": devicerole_o.id,
            "device_type_id": devicetype_o.id,
        }
    )

    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema_create(), format_checker=FormatChecker())
    obj = utils.object_create(Device, **kwargs)
    return obj


def get(name):
    """Return a Device."""
    obj = utils.object_get_or_none(Device, name=name)
    return obj


def get_list(**kwargs):
    """Get a list of Device objects."""
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    result = utils.object_list(Device, **kwargs)
    return result


def update(obj, **kwargs):
    """Update a Device."""
    update_if_not_set = ["serial_number"]

    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    kwargs_if_not_set = utils.filter_keys(kwargs, update_if_not_set)
    obj = utils.object_update(obj, **kwargs_if_not_set, force=False)
    return obj


def update_management(obj, discoverable_ip_address):
    """Update primary IP address if match the Discoverable IP address.

    Return True if management IP is set.
    """
    # Set management IP address
    for interface in obj.interfaces.filter(ip_addresses__isnull=False):
        # For each interface
        for ip_address_o in interface.ip_addresses.all():
            # For each configured IP address
            if discoverable_ip_address == str(ip_address_o.address.ip):
                obj.primary_ip4 = ip_address_o
                obj.save()
                return True
    return False
