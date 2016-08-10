from django.contrib import admin
from backend.models import Parking, Organization, Mark, Evacuator, Item
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.


admin.site.register(Organization, OSMGeoAdmin)
admin.site.register(Parking, OSMGeoAdmin)
admin.site.register(Evacuator, OSMGeoAdmin)
admin.site.register(Mark, OSMGeoAdmin)
admin.site.register(Item, OSMGeoAdmin)
