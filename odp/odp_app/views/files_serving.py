import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.conf import settings

from odp_app.models import Sentenza

from sendfile import sendfile


@login_required
def get_file(request,sent_id,field_name): #filename may be a filename or a path, but i have not yet implemented the "path" part in the upload phase
    #check whicherver permission
    sent = get_object_or_404(Sentenza,pk=sent_id)

    # security check
    if sent.forza_esclusione and (not request.user.is_staff):
        raise PermissionDenied
    if not request.user.is_staff:
        for infortunato in sent.infortunati.all():
            if not infortunato.pubblicabile:
                raise PermissionDenied

    # can access document
    doc = getattr(sent,field_name)
    filename = doc.name
    real_path = os.path.join(
                settings.MEDIA_ROOT, 
                filename #the name is actually a the path (immagine-scheda-commento)/file
    )

    return sendfile(request,real_path)
