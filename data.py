"""Mine data and helpers."""
import geopandas as gpd
from shapely.geometry import Polygon

MINE_AREAS = [
    {"name": "Balaghat Belt (MOIL – Largest)", "coords": [[21.805,80.155],[21.825,80.165],[21.830,80.195],[21.815,80.210],[21.795,80.195],[21.790,80.170]],
     "type": "MOIL Underground", "importance": 0.98, "district": "Balaghat", "state": "Madhya Pradesh", "status": "Active", "center": [21.82, 80.18]},
    {"name": "Ukwa Mine (MOIL)", "coords": [[21.935,80.430],[21.955,80.440],[21.960,80.465],[21.945,80.475],[21.925,80.460],[21.930,80.435]],
     "type": "MOIL Underground", "importance": 0.90, "district": "Balaghat", "state": "Madhya Pradesh", "status": "Active", "center": [21.95, 80.45]},
    {"name": "Tirodi Mine (MOIL)", "coords": [[21.685,79.695],[21.705,79.705],[21.710,79.730],[21.695,79.740],[21.675,79.725],[21.680,79.700]],
     "type": "MOIL", "importance": 0.88, "district": "Balaghat", "state": "Madhya Pradesh", "status": "Active", "center": [21.70, 79.72]},
    {"name": "Sitapatore Mine (MOIL)", "coords": [[21.665,79.655],[21.680,79.665],[21.685,79.685],[21.670,79.695],[21.655,79.680]],
     "type": "MOIL", "importance": 0.82, "district": "Balaghat", "state": "Madhya Pradesh", "status": "Active", "center": [21.68, 79.67]},
    {"name": "Chhindwara (MP)", "coords": [[22.035,78.930],[22.055,78.945],[22.060,78.970],[22.045,78.980],[22.025,78.960]],
     "type": "Exploration", "importance": 0.70, "district": "Chhindwara", "state": "Madhya Pradesh", "status": "Exploration", "center": [22.05, 78.95]},
    {"name": "Dongri Buzurg (MOIL)", "coords": [[21.335,79.825],[21.355,79.840],[21.360,79.870],[21.345,79.880],[21.325,79.860],[21.330,79.835]],
     "type": "MOIL Opencast", "importance": 0.92, "district": "Bhandara", "state": "Maharashtra", "status": "Active", "center": [21.35, 79.85]},
    {"name": "Chikla Mine (MOIL)", "coords": [[21.385,79.685],[21.405,79.695],[21.410,79.720],[21.395,79.730],[21.375,79.710]],
     "type": "MOIL", "importance": 0.85, "district": "Bhandara", "state": "Maharashtra", "status": "Active", "center": [21.40, 79.70]},
    {"name": "Kandri–Munsar Cluster", "coords": [[21.430,79.030],[21.455,79.045],[21.460,79.075],[21.440,79.085],[21.420,79.060]],
     "type": "MOIL", "importance": 0.87, "district": "Nagpur", "state": "Maharashtra", "status": "Active", "center": [21.45, 79.05]},
    {"name": "Nagpur–Bhandara Cluster", "coords": [[21.230,79.130],[21.260,79.145],[21.270,79.180],[21.250,79.195],[21.220,79.165]],
     "type": "MOIL Multiple", "importance": 0.95, "district": "Nagpur / Bhandara", "state": "Maharashtra", "status": "Active", "center": [21.25, 79.15]},
    {"name": "Sandur Belt (Karnataka)", "coords": [[15.085,76.520],[15.115,76.535],[15.125,76.570],[15.100,76.585],[15.075,76.555]],
     "type": "Major Belt", "importance": 0.78, "district": "Ballari", "state": "Karnataka", "status": "Active", "center": [15.10, 76.55]},
    {"name": "Bonai–Keonjhar (Odisha)", "coords": [[21.830,85.220],[21.860,85.240],[21.870,85.280],[21.850,85.295],[21.820,85.265]],
     "type": "Major Belt", "importance": 0.80, "district": "Sundargarh / Keonjhar", "state": "Odisha", "status": "Active", "center": [21.85, 85.25]},
    {"name": "Joda–Barbil (Odisha)", "coords": [[22.020,85.420],[22.050,85.440],[22.060,85.480],[22.040,85.495],[22.010,85.460]],
     "type": "Major Belt", "importance": 0.72, "district": "Keonjhar", "state": "Odisha", "status": "Active", "center": [22.05, 85.45]},
    {"name": "Srikakulam (AP)", "coords": [[18.280,83.870],[18.305,83.885],[18.315,83.920],[18.295,83.935],[18.270,83.905]],
     "type": "Major Belt", "importance": 0.68, "district": "Srikakulam", "state": "Andhra Pradesh", "status": "Partially Active", "center": [18.30, 83.90]},
]


def calculate_accurate_area_km2(coords):
    try:
        poly = Polygon([(lon, lat) for lat, lon in coords])
        gdf = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
        return round(gdf.to_crs(gdf.estimate_utm_crs()).geometry.area.iloc[0] / 1_000_000, 3)
    except Exception:
        return 0.0


def get_mine_areas_with_area():
    mines = [dict(m) for m in MINE_AREAS]
    for m in mines:
        if "area_km2" not in m:
            m["area_km2"] = calculate_accurate_area_km2(m["coords"])
    return mines