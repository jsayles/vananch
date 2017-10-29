from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def ship_info(ship):
    name = ship.name
    mmsi = ship.mmsi
    imo = ship.imo
    length = ship.length
    flag_url = ship.get_flag_url()
    country = ship.country

    html = f' \
        <div><strong>{ name }</strong></div>\
        <div><img src="{ flag_url }"/> { country }</div>\
        <div>MMSI={ mmsi }</div> \
        <div>IMO={ imo }</div> \
        <div>Length: { length }</div> \
    '
    return mark_safe(html)
