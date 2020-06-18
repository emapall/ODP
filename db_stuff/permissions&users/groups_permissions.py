# from odp_app.models import *
from django.contrib.auth.models import *
import os
DB_STUFF_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff/permissions&users"


def set_permissions(n):
    f = open(os.path.join(DB_STUFF_PATH,str("permissions_"+n+".txt"),"r")
    g = Group.objects.get(name=n)
    l = f.read().splitlines() #OTHERWISE THERE ARE \N in the strings
    pl = Permssion.objects.filter(name__in=l)
    print("this group has "+str(pl.count())+" permissions")
    
    g.permission.set(pl)
    g.save()


def create_groups():
    Group.objects.create(name="inserimento")
    Group.objects.create(name="admin")
    Group.objects.create(name="management_odp")
    