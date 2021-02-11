import logging
import os

from django import template
from django.conf import settings
from django.urls import reverse

#from odp_app.models import Sentenza, #TODO Ctu

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def sentenza_file_url(obj_id, obj_name, field_name): #TODO UPDATE DEL FILE PER LA CTU, CON UPDATE ANCHE NELLE ALTRE FUNZIONI
    """
    Given the id of an object and the filend name associated with a file field of a model object,
    retrurns the url correspoding to the view serving THAT specific file.

    The model object is specified via the name. Possible names:
        - s (odp_app.models.Sentenza)
        - c (odp_app.models.Ctu)

    NOTE: yes it could have been done with an hard encoded url 
    in the template, but this is more changable in the future
    (indeed it was helpful)
    """
    
    try:
        return reverse('odp_app:get-file', kwargs={
            'obj_id': obj_id,
            'obj_name': obj_name,
            'field_name': field_name,
        })
    except:
        # Wrong format
        logger.warning("Could not convert %s for object of type %s and id %s" %(field_name,str(obj_name),str(obj_id)))
        # TODO return a 404, 503 or something like that
        return None
