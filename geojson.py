# utils/geojson.py

import ee
import json


def featurecollection_to_geojson(fc):
    """
    Converts ee.FeatureCollection to GeoJSON dict.

    Args:
        fc (ee.FeatureCollection)

    Returns:
        dict: GeoJSON FeatureCollection
    """

    geojson = fc.getInfo()

    # Safety check
    if "features" not in geojson:
        return {
            "type": "FeatureCollection",
            "features": []
        }

    return geojson


def featurecollection_to_geojson_string(fc):
    """
    Converts ee.FeatureCollection to GeoJSON string.

    Returns:
        str
    """

    geojson_dict = featurecollection_to_geojson(fc)
    return json.dumps(geojson_dict)
