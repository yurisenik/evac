from django.contrib.gis.db import models


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
    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} ({1})'.format(self.mark.title, self.number)