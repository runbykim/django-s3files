from django.contrib.admin.views.main import PAGE_VAR
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def s3files_paginator_number(paginator, page_num, i, current_path):
    """
    Generate an individual page index link in a paginated list.
    """
    ELLIPSIS = _("…")
    if i == ELLIPSIS:
        return format_html("{} ", ELLIPSIS)
    elif i == page_num:
        return format_html('<span class="this-page">{}</span> ', i)
    else:
        return format_html(
            '<a href="?path={}&{}={}"{}>{}</a> ',
            current_path,
            PAGE_VAR,
            i,
            mark_safe(' class="end"' if i == paginator.num_pages else ""),
            i,
        )