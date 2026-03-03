# utils/validators.py

import os
import datetime
import ee


# ---------------------------
# KML VALIDATION
# ---------------------------

def validate_kml_file(file):
    """
    Validates uploaded KML file.

    Args:
        file (FileStorage)

    Raises:
        ValueError
    """

    if not file:
        raise ValueError("No KML file uploaded")

    filename = file.filename.lower()

    if not filename.endswith(".kml"):
        raise ValueError("Only .kml files are supported")

    if os.path.getsize(file.stream.name) == 0:
        raise ValueError("Uploaded KML file is empty")


# ---------------------------
# DATE VALIDATION
# ---------------------------

def validate_dates(date_t1, date_t2):
    """
    Validates temporal inputs.

    Args:
        date_t1 (str): YYYY-MM-DD
        date_t2 (str): YYYY-MM-DD

    Raises:
        ValueError
    """

    try:
        d1 = datetime.datetime.strptime(date_t1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(date_t2, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")

    if d1 >= d2:
        raise ValueError("T1 must be earlier than T2")


# ---------------------------
# AOI VALIDATION
# ---------------------------

def validate_aoi(aoi):
    """
    Validates ee.Geometry AOI.

    Args:
        aoi (ee.Geometry)

    Raises:
        ValueError
    """

    try:
        area = aoi.area().getInfo()
    except Exception:
        raise ValueError("Invalid AOI geometry")

    if area <= 0:
        raise ValueError("AOI area must be positive")

    if area > 1e10:
        raise ValueError("AOI too large (limit exceeded)")
