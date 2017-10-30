from django.db import models
from django.conf import settings

import pycountry


class Ship(models.Model):
    name = models.CharField(max_length=128)
    imo = models.SmallIntegerField()
    mmsi = models.SmallIntegerField()
    marine_traffic_id = models.SmallIntegerField()
    length = models.SmallIntegerField(null=True, blank=True)
    flag = models.CharField(max_length=2, null=True, blank=True)

    @property
    def flag_url(self):
        return "/static/flags/%s.gif" % str(self.flag).lower()

    @property
    def country(self):
        if self.flag:
            country = pycountry.countries.get(alpha_2=self.flag)
            if country:
                return country.name

    def __str__(self):
        return "%s (%d)" % (self.name, self.mmsi)


class ShipImport(models.Model):
    created_ts = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", null=True, blank=True, on_delete=models.CASCADE)
    completed_ts = models.DateTimeField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    @property
    def successful(self):
        return self.completed_ts != None and self.error == None

    @property
    def ships(self):
        return Ship.objects.filter(id__in=self.ship_records.all().values('ship__id'))

    def __str__(self):
        if self.successful:
            return "%s: Success" % self.created_ts
        return "%s: Error" % self.created_ts


class ShipRecord(models.Model):
    ship_import = models.ForeignKey(ShipImport, on_delete=models.CASCADE)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    course = models.SmallIntegerField(null=True, blank=True)
    speed = models.SmallIntegerField(null=True, blank=True)
    latitude  = models.FloatField()
    longitude = models.FloatField()

    @property
    def record_ts(self):
        return self.ship_import.created_ts

    @property
    def location_str(self):
        return "%sn %sw" % (self.latitude, self.longitude)

    def __str__(self):
        return "%s: %s at %s" % (self.record_ts, self.ship, self.location_str)
