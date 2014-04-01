# holder.py 

jsonPlaceHolder = """
var places = { data:[
%s
]}
"""

jsonPlaceItem = '''{
    "source": "%s",
    "lat": %s,
    "lon": %s,
    "value": %s,
    "size": %s,
    "arTitle": "%s",
    "translitTitle": "%s",
    "UStranslitTitle": "%s",
    "translitSimpleTitle": "%s",
    "topType": "%s",
    },
''' # sourceFileBase, lat, lon, arabic, translit, UStranslitTitle, translitSimple (for search), topType

jsonRouteHolder = """
var routes = { data:[
%s
]}
"""

jsonRouteItem = '''{
    "RouteID" : "%s",
    "type": "LineString",
    "coordinates": [%s],
    },''' # routeID, type (?), array of coordinates
