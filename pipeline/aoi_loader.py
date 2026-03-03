import ee
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon


def load_aoi(kml_path: str) -> ee.Geometry:
    gdf = gpd.read_file(kml_path)

    if gdf.empty:
        raise ValueError("Uploaded AOI file is empty")

    gdf = gdf.to_crs(epsg=4326)
    geom = gdf.geometry.iloc[0]

    # 🔴 Handle Google Earth GeometryCollection
    if geom.geom_type == "GeometryCollection":
        geom = next(g for g in geom.geoms if g.geom_type in ["Polygon", "MultiPolygon"])

    # 🔴 Drop altitude (Z) coordinates
    if geom.geom_type == "Polygon":
        coords = [[(x, y) for x, y, *_ in geom.exterior.coords]]
    elif geom.geom_type == "MultiPolygon":
        coords = [[(x, y) for x, y, *_ in geom.geoms[0].exterior.coords]]
    else:
        raise ValueError("AOI must be Polygon or MultiPolygon")

    return ee.Geometry.Polygon(coords)
