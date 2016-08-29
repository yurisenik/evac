from django.contrib.gis.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Parking(models.Model):
    id_ext = models.IntegerField(null=True)
    title = models.CharField(null=True, blank=True, max_length=1000)
    geom = models.PointField(null=True)

    def __str__(self):
        return self.title


class Organization(models.Model):
    id_ext = models.IntegerField(null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title


class Mark(models.Model):
    id_ext = models.IntegerField(null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    sort = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Evacuator(models.Model):
    id_ext = models.IntegerField(null=True)
    number = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.number


class Item(models.Model):
    id_ext = models.IntegerField(null=True)
    from_place = models.CharField(null=True, blank=True, max_length=1000)
    geom = models.PointField(null=True)
    evacuator = models.ForeignKey(Evacuator)
    mark = models.ForeignKey(Mark)
    number = models.CharField(max_length=1000, blank=True, null=True)
    organization = models.ForeignKey(Organization)
    parking = models.ForeignKey(Parking)
    active = models.NullBooleanField(null=True)
    to_index = models.NullBooleanField(null=True)
    sort = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_seen_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} ({1})'.format(self.mark.title, self.number)


@receiver(pre_save, sender=Item)
def item_pre_save_handler(sender, instance, **kwargs):
    import requests

    if instance.from_place and (not instance.geom):
        payload = {
            'll': '38.970488999999965,45.026769074573004',
            'spn': '5,5',
            'rspn': '0',
            'lang': 'ru_RU',
            'format': 'json',
            'geocode': instance.from_place
        }

        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload, verify=False)

        data = r.json()
        print(data)

        if int(data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']) > 0:
            feature_member = data['response']['GeoObjectCollection']['featureMember'][0]
            instance.geom = 'POINT({lng_lat})'.format(lng_lat=feature_member['GeoObject']['Point']['pos'])

