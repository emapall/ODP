import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



@login_required
def get_file(request,document_id,filename): #filename may be a filename or a path, but i have not yet implemented the "path" part in the upload phase
    #check whicherver permission
    document = get_object_or_404(Document,pk=document_id)

    if not document.user == request.user:
        raise PermissionDenied
    VA VISTO SE UN UTENTE NON ADMIN PUÒ ACCEDERE AL FILE!
    
    # can access document
    doc_file = document.document
    print("Path calcolata e path documento:")
    real_path = os.path.join(
                settings.MEDIA_ROOT, 
                filename #the name is actually a the path user/file
    )
    print(real_path,doc_file.path, real_path == doc_file.path)

    return sendfile(request,real_path)
