# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from webpack_bridge.manifest import EntrypointResolver
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_webpack_entry(entry, **tag_attrs):
    """
    Renders the html required to import the bundles associated with the
    'entry' entrypoint.
    'tag_attrs' can be used to provide attributes for the rendered html.
    They are grouped by file extension.
    """
    resolver = EntrypointResolver(settings.STATICFILES_DIRS)
    bundles = resolver.resolve(entry)

    parsed_html = ""
    for entry_bundle in bundles:
        if entry_bundle['ext'] in tag_attrs:
            bundle_html = entry_bundle['tag'].format(
                attributes=tag_attrs[entry_bundle['ext']]
            )
        else:
            bundle_html = entry_bundle['tag'].format(attributes="")
        parsed_html += bundle_html + '\n'

    return mark_safe(parsed_html)
