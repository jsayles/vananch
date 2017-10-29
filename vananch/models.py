from django.db import models
from django.conf import settings


class Ship(models.Model):
    name = models.CharField(max_length=128)
    imo = models.SmallIntegerField()
    mmsi = models.SmallIntegerField()
    marine_traffic_id = models.SmallIntegerField()
    length = models.SmallIntegerField(null=True, blank=True)
    flag = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return "%s (%d)" % (self.name, self.mmsi)

    def get_flag_url(self):
        return "/static/flags/%s.gif" % str(self.flag).lower()


class ShipRecord(models.Model):
    record_ts = models.DateTimeField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    course = models.SmallIntegerField(null=True, blank=True)
    speed = models.SmallIntegerField(null=True, blank=True)
    latitude  = models.FloatField()
    longitude = models.FloatField()

    def location_str(self):
        return "%sn %sw" % (self.latitude, self.longitude)

    def __str__(self):
        return "%s: %s at %s" % (self.record_ts, self.ship, self.location_str())
