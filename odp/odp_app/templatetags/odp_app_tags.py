import logging
import os

from django import template
from django.conf import settings
from django.urls import reverse

from odp_app.models import Sentenza

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def sentenza_file_url(sent_id, field_name):
    try:
        return reverse('odp_app:sfs-get-file', kwargs={
            'sent_id': sent_id,
            'field_name': field_name,
        })
    except:
        # Wrong format
        logger.warning("Could not convert file path: %s" % relpath)
        return None
