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
    """
    Given the id of a sentenza and the filend name associated with a file,
    retrurns the url correspoding to the view serving THAT specific file.

    NOTE: yes it could have been done with an hard encoded url 
    in the template, but this is more changable in the future
    """
    try:
        return reverse('odp_app:get-file', kwargs={
            'sent_id': sent_id,
            'field_name': field_name,
        })
    except:
        # Wrong format
        logger.warning("Could not convert %s for sentenza %s" %(field_name,str(sent_id)))
        # TODO return a 404, 503 or something like that
        return None
