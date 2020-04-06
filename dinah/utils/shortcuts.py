from functools import partial as _partial
from typing import Any, Dict

from django.shortcuts import render

# NOTE: Enum class `status`, `content_type`
from django.template.loader import render_to_string


def render_mako(
    request,
    template_name: str,
    context: dict = None,
    content_type: str = None,
    status: int = None,
):
    return render(
        request=request,
        template_name=template_name,
        context=context,
        content_type=content_type,
        status=status,
        using="mako",
    )


def render_mako_to_string(template_name: str, context: dict = None, request=None):
    return render_to_string(
        request=request, template_name=template_name, context=context, using="mako",
    )
