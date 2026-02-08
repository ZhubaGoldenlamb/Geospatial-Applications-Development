"""
Hydrologic and remote sensing analysis of the Walla Walla Basin (Washington, USA)
using the Google Earth Engine Python API.

This script demonstrates vector and raster geoprocessing workflows, including:
- Hydrologic feature filtering and spatial relationships
- Stream order–based main channel selection
- Riparian buffering and upland delineation
- Derived attribute calculation (distance to study point)
- Spatial joins with U.S. Census tracts
- Landsat 9 filtering, vegetation index calculation, and compositing
- Zonal statistics and exploratory sampling
"""

import ee
import geemap
import geemap.colormaps as cm
import pandas as pd
import altair as alt


# ---------------------------------------------------------------------
# Earth Engine initialization
# ---------------------------------------------------------------------
# Attempts to initialize Earth Engine; if authentication is required,
# the browser-based authentication flow will be triggered.
try:
    ee.Initialize(project="zhubas-project")
except Exception:
    ee.Authenticate()
    ee.Initialize(project="zhubas-project")


# ---------------------------------------------------------------------
# Map setup
# ---------------------------------------------------------------------
# Initialize the geemap map object for visual inspection of layers.
m = geemap.Map()


# ---------------------------------------------------------------------
# Vector data sources and study area definition
# ---------------------------------------------------------------------
# Administrative boundaries for geographic context.
FAO_GAUL = ee.FeatureCollection("FAO/GAUL/2015/level0")

# Hydrologic basin polygons (HydroATLAS Level 6).
basins = ee.FeatureCollection("WWF/HydroATLAS/v1/Basins/level06")

# Free-flowing river network (HydroSHEDS).
rivers = ee.FeatureCollection("WWF/HydroSHEDS/v1/FreeFlowingRivers")

# Central Walla Walla, Washington, used as a reference point for distance queries.
wawa = ee.Geometry.Point([-118.3430, 46.0646])

# Center the map on the study area.
m.set_center(-118.3430, 46.0646, 8)

# Add base layers for visual context.
m.add_layer(basins, {"color": "green"}, "Basins")
m.add_layer(rivers, {"color": "blue"}, "Rivers")
m.add_layer(wawa, {"color": "black"}, "Study Point (Walla Walla)")
m.add_layer(FAO_GAUL, {"color": "cyan"}, "FAO GAUL")


# ---------------------------------------------------------------------
# Basin filtering
# ---------------------------------------------------------------------
# Select the Walla Walla Basin using the HydroATLAS basin identifier.
# The explicit ee.Filter form is preferred for clarity and robustness.
wawa_basin = basins.filter(ee.Filter.eq("HYBAS_ID", 7060382460))

# Add the selected basin to the map.
m.add_layer(wawa_basin, {"color": "yellow"}, "Walla Walla Basin")


# ---------------------------------------------------------------------
# River filtering and spatial relationships
# ---------------------------------------------------------------------
# Filter river segments to those intersecting the Walla Walla Basin.
# This constrains analysis to hydrologically relevant features.
wawa_rivers = rivers.filterBounds(wawa_basin)
m.add_layer(wawa_rivers, {"color": "blue"}, "Rivers in Basin")

# Identify river segments within 10 km of the study point.
# This demonstrates proximity-based spatial filtering.
wawa_rivers_close = rivers.filter(
    ee.Filter.withinDistance(
        distance=10e3,
        leftField=".geo",
        rightValue=wawa,
        maxError=1,
    )
)
m.add_layer(wawa_rivers_close, {"color": "green"}, "Rivers within 10 km")


# ---------------------------------------------------------------------
# Stream order analysis
# ---------------------------------------------------------------------
# Query minimum and maximum river order values to understand attribute range.
_ = wawa_rivers.reduceColumns(ee.Reducer.minMax(), ["RIV_ORD"])

# Visualize river order to verify spatial continuity and hierarchy.
river_order_vis = (
    ee.Image()
    .toByte()
    .paint(wawa_rivers, "RIV_ORD", 3)
    .visualize(
        min=5,
        max=8,
        palette=["purple", "blue", "lightblue", "white"],
    )
)
m.add_layer(river_order_vis, {}, "River Order")

# Select main river channels based on stream order.
# Stream orders ≤ 6 are retained to focus analysis on dominant hydrologic corridors.
main_rivers = wawa_rivers.filter("RIV_ORD <= 6")
m.add_layer(main_rivers, {"color": "orange"}, "Main Rivers (RIV_ORD ≤ 6)")


# ---------------------------------------------------------------------
# River length statistics
# ---------------------------------------------------------------------
# Calculate total river length within the basin.
wawa_river_length = wawa_rivers.reduceColumns(
    ee.Reducer.sum(), ["LENGTH_KM"]
).getNumber("sum")

# Calculate total length of main rivers only.
wawa_main_river_length = main_rivers.reduceColumns(
    ee.Reducer.sum(), ["LENGTH_KM"]
).getNumber("sum")

# Compute the percentage of total river length represented by main rivers.
main_river_percentage = (
    wawa_main_river_length.divide(wawa_river_length).multiply(100)
)


# ---------------------------------------------------------------------
# Riparian buffering and upland delineation
# ---------------------------------------------------------------------
# Create a 100 m buffer around main river channels to approximate riparian zones.
riparian = main_rivers.geometry().buffer(100, 1)
m.add_layer(riparian, {"color": "black"}, "Riparian Buffer (100 m)")

# Derive upland areas by subtracting riparian zones from the basin geometry.
upland = wawa_basin.geometry().difference(riparian)
m.add_layer(upland, {"color": "orange"}, "Upland Areas")


# ---------------------------------------------------------------------
# Derived attributes
# ---------------------------------------------------------------------
# Add a distance-to-study-point attribute (kilometers) to each river segment.
def append_distance(feature):
    distance_km = feature.distance(wawa, 1).divide(1000)
    return feature.set("distance_km", distance_km)


wawa_rivers = wawa_rivers.map(append_distance)

# Calculate the mean distance of river segments from the study point.
mean_distance = wawa_rivers.reduceColumns(
    reducer=ee.Reducer.mean(),
    selectors=["distance_km"],
)


# ---------------------------------------------------------------------
# Spatial join with census tracts
# ---------------------------------------------------------------------
# Load U.S. Census tract boundaries (TIGER 2020).
census_tracts = ee.FeatureCollection("TIGER/2020/TRACT")
m.add_layer(census_tracts, {"color": "purple"}, "Census Tracts")

# Perform an intersection-based spatial join, saving the first matching tract.
intersect_filter = ee.Filter.intersects(leftField=".geo", rightField=".geo")
save_first_join = ee.Join.saveFirst(matchKey="tract")

wawa_rivers = save_first_join.apply(
    wawa_rivers, census_tracts, intersect_filter
)

# Copy selected census tract attributes into the river features.
def copy_properties(feature):
    joined_feature = feature.get("tract")
    return feature.copyProperties(joined_feature, ["TRACTCE", "NAMELSAD"])


wawa_rivers = wawa_rivers.map(copy_properties)


# ---------------------------------------------------------------------
# Raster analysis: Landsat 9 TOA
# ---------------------------------------------------------------------
# Load Landsat 9 TOA imagery and filter by date, basin extent, and cloud cover.
toa_col = (
    ee.ImageCollection("LANDSAT/LC09/C02/T1_TOA")
    .filterDate("2022-04-01", "2022-11-01")
    .filterBounds(wawa_basin)
    .filter("CLOUD_COVER < 1")
)

# Visualization parameters for false-color display.
false_color_vis = {
    "bands": ["B5", "B4", "B3"],
    "min": 0,
    "max": 0.4,
}

m.add_layer(toa_col.first(), false_color_vis, "Landsat TOA (False Color)")


# ---------------------------------------------------------------------
# Spectral indices
# ---------------------------------------------------------------------
# Calculate NDVI and NBR for each image in the collection.
def calc_indices(image):
    # NDVI calculation using NIR and Red bands.
    nir = image.select("B5")
    red = image.select("B4")
    ndvi = nir.subtract(red).divide(nir.add(red)).rename("ndvi")

    # NBR calculation using NIR and SWIR2 bands.
    nbr = ee.Image().expression(
        "nbr = (nir - swir2) / (nir + swir2)",
        {
            "nir": image.select("B5"),
            "swir2": image.select("B7"),
        },
    ).rename("nbr")

    # Preserve original image properties while adding new bands.
    return image.select().addBands([ndvi, nbr]).addBands(image.select("B.*"))


toa_col = toa_col.map(calc_indices)


# ---------------------------------------------------------------------
# Image compositing and clipping
# ---------------------------------------------------------------------
# Create a maximum-value composite across the image collection.
band_names = toa_col.first().bandNames()
toa_max = toa_col.reduce(ee.Reducer.max(band_names.size())).rename(band_names)

m.add_layer(toa_max, false_color_vis, "TOA Max Composite")

# Clip the composite to the Walla Walla Basin.
toa_max_basin = toa_max.clip(wawa_basin)

# NDVI visualization parameters.
ndvi_vis = {
    "bands": ["ndvi"],
    "min": 0,
    "max": 0.7,
    "palette": cm.get_palette("Greens"),
}

m.add_layer(toa_max_basin, ndvi_vis, "NDVI Max (Basin)")


# ---------------------------------------------------------------------
# Zonal statistics
# ---------------------------------------------------------------------
# Calculate median NDVI values for riparian and upland zones.
toa_riparian = toa_max_basin.reduceRegion(
    reducer=ee.Reducer.median(),
    geometry=riparian,
    scale=100,
    maxPixels=2e8,
)

toa_upland = toa_max_basin.reduceRegion(
    reducer=ee.Reducer.median(),
    geometry=upland,
    scale=100,
    maxPixels=2e8,
)


# ---------------------------------------------------------------------
# Sampling and exploratory analysis
# ---------------------------------------------------------------------
# Sample random pixels from the composite for exploratory analysis.
toa_sample = toa_max_basin.sample(
    region=wawa_basin,
    scale=30,
    numPixels=1000,
)

# Convert sampled data to a Pandas DataFrame.
df = ee.data.computeFeatures(
    {"expression": toa_sample, "fileFormat": "PANDAS_DATAFRAME"}
)

if not isinstance(df, pd.DataFrame):
    df = pd.DataFrame(df)

# Generate and save exploratory plots as HTML files.
ndvi_hist = alt.Chart(df).mark_bar().encode(
    alt.X("ndvi:Q", bin=True),
    y="count()",
).properties(title="NDVI Distribution")

ndvi_hist.save("ndvi_histogram.html")

band_scatter = alt.Chart(df).mark_point().encode(
    x="B4:Q",
    y="B5:Q",
).properties(title="Red vs NIR Reflectance")

band_scatter.save("b4_b5_scatter.html")


# ---------------------------------------------------------------------
# Console output (useful if script is run locally)
# ---------------------------------------------------------------------
print("Mean river distance to study point (km):", mean_distance.get("mean").getInfo())
print("Main rivers as % of total river length:", main_river_percentage.getInfo())
print("Median riparian NDVI:", toa_riparian.getNumber("ndvi").getInfo())
print("Median upland NDVI:", toa_upland.getNumber("ndvi").getInfo())
print("Saved charts: ndvi_histogram.html, b4_b5_scatter.html")

# Display map in interactive environments (no effect in terminal execution).
try:
    display(m)
except Exception:
    pass