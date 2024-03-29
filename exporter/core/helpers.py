from dateutil.parser import parse
from html import escape
from typing import List

from django.template.defaultfilters import safe
from django.templatetags.tz import localtime
from django.utils.safestring import mark_safe

from exporter.core import decorators
from exporter.core import constants
from core.builtins.custom_tags import default_na
from exporter.organisation.roles.services import get_user_permissions


class Section:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles


class Tile:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def str_to_bool(v, invert_none=False):
    if v is None:
        return invert_none
    if isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str_date_only(value):
    return localtime(parse(value)).strftime("%d %B %Y")


def generate_notification_string(notifications, case_types):
    notification_count = notifications["notifications"]
    notification_count_sum = sum([count for case_type, count in notification_count.items() if case_type in case_types])
    return generate_notification_total_string(notification_count_sum)


def generate_notification_total_string(notification_count):
    if not notification_count:
        return ""
    elif notification_count == 1:
        return f"You have {notification_count} new notification"
    else:
        return f"You have {notification_count} new notifications"


def convert_to_link(address, name=None, classes="", include_br=False):
    """
    Returns a correctly formatted, safe link to an address
    Returns default_na if no address is provided
    """
    if not address:
        return default_na(None)

    if not name:
        name = address

    address = escape(address)
    name = escape(name)

    br = "<br>" if include_br else ""

    return safe(f'<a href="{address}" class="govuk-link govuk-link--no-visited-state {classes}">{name}</a>{br}')


def remove_prefix(json, prefix):
    post_data = {}
    for k in json:
        if k.startswith(prefix):
            field = k[len(prefix) :]
            post_data[field] = json[k]
    return post_data


def has_permission(request, permission):
    """
    Returns true if the user has a given permission, else false
    """
    user_permissions = get_user_permissions(request)
    return permission in user_permissions, user_permissions


def decorate_patterns_with_permission(patterns, permission, ignore: List[str] = None):
    def _wrap_with_permission(_permission, view_func=None):
        actual_decorator = decorators.has_permission(_permission)

        if view_func:
            return actual_decorator(view_func)
        return actual_decorator

    if ignore is None:
        ignore = []

    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        if pattern.name in ignore:
            continue
        pattern.callback = _wrap_with_permission(permission, callback)
        pattern._callback = _wrap_with_permission(permission, callback)
        decorated_patterns.append(pattern)
    return decorated_patterns


def add_validate_only_to_data(data):
    data = data.copy()
    data["validate_only"] = True

    return data


def convert_control_list_entries(control_list_entries):
    return default_na(
        mark_safe(  # nosec
            ", ".join(
                [
                    "<span data-definition-title='"
                    + clc["rating"]
                    + "' data-definition-text='"
                    + clc.get("text", "")
                    + "'>"
                    + clc["rating"]
                    + "</span>"
                    for clc in control_list_entries
                ]
            )
        )
    )


def get_firearms_subcategory(type):
    is_firearm = type == constants.FIREARMS
    is_firearm_ammunition_or_component = type in constants.FIREARM_AMMUNITION_COMPONENT_TYPES
    is_firearms_accessory = type == constants.FIREARMS_ACCESSORY
    is_firearms_software_or_tech = type in constants.FIREARMS_SOFTWARE_TECH
    return is_firearm, is_firearm_ammunition_or_component, is_firearms_accessory, is_firearms_software_or_tech
