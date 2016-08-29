from django.contrib import admin
from backend.models import Parking, Organization, Mark, Evacuator, Item
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.


admin.site.register(Organization, OSMGeoAdmin)
admin.site.register(Parking, OSMGeoAdmin)
admin.site.register(Evacuator, OSMGeoAdmin)
admin.site.register(Mark, OSMGeoAdmin)


class ItemAdmin(OSMGeoAdmin):
    readonly_fields = ('create_date', 'last_seen_date')


admin.site.register(Item, ItemAdmin)
