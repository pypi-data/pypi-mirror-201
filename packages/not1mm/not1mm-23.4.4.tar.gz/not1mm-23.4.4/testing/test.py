import great_circle_calculator.great_circle_calculator as gcc
from json import loads, dumps

LOCATION = "/home/mbridak/Nextcloud/dev/not1mm/not1mm/data/cty.json"

ctyfile = {}

with open(LOCATION, "r") as fd:
    ctyfile = loads(fd.read())

""""""


def cty_lookup(callsign: str):
    callsign = callsign.upper()
    for x in reversed(range(len(callsign))):
        searchitem = callsign[: x + 1]
        result = {key: val for key, val in ctyfile.items() if key == searchitem}
        if not result:
            continue
        if result.get(searchitem).get("exact_match"):
            if searchitem == callsign:
                return result
            else:
                continue
        return result


def gridtolatlon(maiden):
    """
    Converts a maidenhead gridsquare to a latitude longitude pair.
    """
    maiden = str(maiden).strip().upper()

    chars_in_grid_square = len(maiden)
    if not 8 >= chars_in_grid_square >= 2 and chars_in_grid_square % 2 == 0:
        return 0, 0

    lon = (ord(maiden[0]) - 65) * 20 - 180
    lat = (ord(maiden[1]) - 65) * 10 - 90

    if chars_in_grid_square >= 4:
        lon += (ord(maiden[2]) - 48) * 2
        lat += ord(maiden[3]) - 48

    if chars_in_grid_square >= 6:
        lon += (ord(maiden[4]) - 65) / 12 + 1 / 24
        lat += (ord(maiden[5]) - 65) / 24 + 1 / 48

    if chars_in_grid_square >= 8:
        lon += (ord(maiden[6])) * 5.0 / 600
        lat += (ord(maiden[7])) * 2.5 / 600

    return lat, lon


result = cty_lookup("g0upl")

print(result)
# print(result.keys())
# print(result.items())
# print(result.values())
for a in result.items():
    print(a[0])
    print(a[1].get("entity"))
    print(a[1].get("cq"))
    print(a[1].get("itu"))
    print(a[1].get("continent"))
    print(a[1].get("lat"))
    print(a[1].get("long"))
    print(a[1].get("primary_pfx"))
    hislat = a[1].get("lat")
    hislon = a[1].get("long")
    hislon = hislon * -1

mylat, mylon = gridtolatlon("DM13at")
# mylon = 117.9583
print(f"mylat:{mylat} mylon:{mylon}")
print(f"hislat:{hislat} hislon:{hislon}")

distance = gcc.distance_between_points(
    (mylon, mylat), (hislon, hislat), unit="meters", haversine=True
)
print(f"Dist: {int(distance/1000)}km {int((distance/1000)*0.621371)}mi")
