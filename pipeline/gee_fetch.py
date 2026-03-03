import ee
import geopandas as gpd


# --------------------------------------------------
# KML → EE GEOMETRY
# --------------------------------------------------
def load_aoi_from_kml(kml_path: str) -> ee.Geometry:
    gdf = gpd.read_file(kml_path)
    if gdf.empty:
        raise ValueError("KML file contains no geometry")

    geom = gdf.geometry.iloc[0]
    return ee.Geometry(geom.__geo_interface__)


# --------------------------------------------------
# SENTINEL-2 CLOUD MASK
# --------------------------------------------------
def mask_s2_clouds(image: ee.Image) -> ee.Image:
    qa = image.select("QA60")
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11

    mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )

    return (
        image
        .updateMask(mask)
        .divide(10000)
        .select(["B2", "B3", "B4", "B8", "B11"])
        .copyProperties(image, ["system:time_start"])
    )


# --------------------------------------------------
# FETCH SENTINEL-2 COMPOSITE
# --------------------------------------------------
def fetch_sentinel2(
    aoi: ee.Geometry,
    start_date: str,
    end_date: str
) -> ee.Image:
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_s2_clouds)
    )

    if collection.size().getInfo() == 0:
        raise ValueError("No Sentinel-2 images found for given dates")

    return collection.median().clip(aoi)
