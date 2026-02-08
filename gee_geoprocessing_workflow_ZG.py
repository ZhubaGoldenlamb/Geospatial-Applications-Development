#Hydrologic and remote sensing analysis of the Walla Walla Basin
#using the Google Earth Engine Python API.
#This script demonstrates vector and raster geoprocessing workflows,
#including hydrologic feature filtering, vegetation index calculation,
#and zonal statistics.

!pip install -q --upgrade earthengine-api

!pip install -q --upgrade geemap

import ee
 import geemap
 import geemap.colormaps as cm
 from google.colab import _frontend

ee.Authenticate()
ee.Initialize(project = "zhubas-project") # Make sure you change for your username!
# https://code.earthengine.google.com/

_frontend.create_scratch_cell("#@title Map\nm = geemap.Map()\nm", False)
#adding front end map console,then the false is to open the frame and not automatically run the code inside.


FAO_GAUL = ee.FeatureCollection("FAO/GAUL/2015/level0")
#defining variables with their file paths or geometric point.
basins = ee.FeatureCollection('WWF/HydroATLAS/v1/Basins/level06')
rivers = ee.FeatureCollection('WWF/HydroSHEDS/v1/FreeFlowingRivers')
wawa = ee.Geometry.Point([-118.3430, 46.0646])
m.set_center(-118.3430, 46.0646, 8)
#above is lat, long, and zoom extent, below is telling Earth Engine to focus on
#the above coordinates. #setCenter() JavaScript API #set_center() Python
#m is the map viewer in Geemap (python), below is adding layers. The Display
#is the Table Properties.
m.add_layer(basins, {'color': 'green'}, 'Basins')
m.add_layer(rivers, {'color': 'blue'}, 'Rivers')
m.add_layer(wawa, {'color': 'black'}, 'Walla Walla')
m.add_layer(FAO_GAUL, {'color': 'cyan'}, 'FAO GAUL')
display(basins.limit(10))
display(rivers.limit(10))
display(wawa)
display(FAO_GAUL.limit(10))

# String expression option.
wawa_basin = basins.filter('HYBAS_ID == 7060382460')
#looks for the basin with specific ID.
# ee.Filter object option. This is the same as the line above.
wawa_basin = basins.filter(ee.Filter.eq('HYBAS_ID', 7060382460))
#adds the layer to the map and assigns it a yellow color.
m.add_layer(wawa_basin, {'color': 'yellow'}, 'Walla Walla basin')

#Get parts of river that are in the Walla Walla Basin. Using the ee.Filter.intersects
#or filterBounds to get the overlap of the river in this basin.

# ee.Filter.intersects option.
wawa_rivers = rivers.filter(
    ee.Filter.intersects(leftField='.geo', rightValue=wawa_basin.geometry(), maxError=1))
#seems like ee. is more granular if needing to be specific, while string method
#is easier
# Shorthand filterBounds option.
wawa_rivers = rivers.filterBounds(wawa_basin)
#adding river layer to map that meets above criteria and coloring it blue
m.add_layer(wawa_rivers, {'color': 'blue'}, 'Rivers')

#see rivers that are near central Walla Wall part of Walla Walla Basin
wawa_rivers_close = rivers.filter(
    ee.Filter.withinDistance(
        distance=10e3, leftField='.geo', rightValue= wawa, maxError=1))
#e3 for 10,000 meters
m.add_layer(wawa_rivers_close, {'color': 'green'}, 'Walla Walla rivers close')

wawa_rivers.reduceColumns(ee.Reducer.minMax(), ['RIV_ORD'])
#search collumn for min and max order number. River does not have anything in the 1-4 order list.

river_order_vis = (
    ee.Image().toByte().paint(wawa_rivers, 'RIV_ORD', 3)
    .visualize(min=5, max=8, palette=['purple', 'blue', 'lightblue', 'white'])
)
#paints min and max with paint tool with three different bands.
m.add_layer(river_order_vis, None, 'River order')
river_order_vis
#calls painted river

main_rivers = wawa_rivers.filter('RIV_ORD <= 6')
#Rivers are already ordered, the filter is just selecting 1-6 order.
m.add_layer(main_rivers, {'color': 'orange'}, 'Main rivers')
main_rivers

wawa_river_length = wawa_rivers.reduceColumns(
    ee.Reducer.sum(), ['LENGTH_KM']).getNumber('sum')
#sums length in in all columns of wawa river and gets number.
wawa_main_river_length = main_rivers.reduceColumns(
    ee.Reducer.sum(), ['LENGTH_KM']).getNumber('sum')
#total length of just the main rivers in orders 5 and 6 only

wawa_main_river_length.divide(wawa_river_length).multiply(100)
#divides main river by total (wawa_river) lengths and turns into percent.
#Rivers in the orders 5 and 6 alone make up 21 percent, so most rivers are tributaries.

riparian = main_rivers.geometry().buffer(100, 1)
m.add_layer(riparian, {'color': 'black'}, 'Main rivers buffer')
#makes 1 100 foot black buffer around the main rivers (5,6 order)

upland = wawa_basin.geometry().difference(riparian) # get it wrong without geometry.
#clipping Walla Walla basin just in the riparian (buffered) zone
m.add_layer(upland, {'color': 'orange'}, 'Upland')

def append_distance(feature):
  #add a distance attribute to the Walla Walla feature class
    distance_km = feature.distance(wawa, 1).divide(1000)
    return feature.set('distance_km', distance_km)

wawa_rivers = wawa_rivers.map(append_distance)

wawa_rivers.limit(10)

wawa_rivers.reduceColumns(reducer=ee.Reducer.mean(), selectors=['distance_km'])
#gets mean distance to central Walla Walla to each river segment

census_tracts = ee.FeatureCollection('TIGER/2020/TRACT');
m.add_layer(census_tracts, {'color': 'purple'}, 'Census tracts')
#adds tigers seen in 2020 to the map

intersect_filter = ee.Filter.intersects(leftField='.geo', rightField='.geo')
save_first_join = ee.Join.saveFirst(matchKey='tract')
wawa_rivers = save_first_join.apply(wawa_rivers, census_tracts, intersect_filter)
wawa_rivers.limit(10)
#joins tiger census with wawa rivers

def copy_properties(feature):
    joined_feature = feature.get('tract')
    return feature.copyProperties(joined_feature, ['TRACTCE', 'NAMELSAD'])
#get secondary features instead of entire tract
wawa_rivers = wawa_rivers.map(copy_properties)
wawa_rivers.limit(10)
#copies into wawa rivers feature class table.

toa_col = (
    ee.ImageCollection('LANDSAT/LC09/C02/T1_TOA')
    .filterDate('2022-04-01', '2022-11-01')
    .filterBounds(wawa_basin)
    .filter('CLOUD_COVER < 1')
)
toa_col
#gets landsat images from dataset between 04 and 11 2022, even though instructions say 2023, haha.

false_color_vis = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.4
}
m.add_layer(toa_col.first(), false_color_vis, 'TOA (first)')
#adds each different band for this specific satelite and stretches the colors from 0-0.4. Then
#adds the bands to the map in two different ways: false color and TOA col (first)

def calc_indices(image):
    # Math method chain option for NDVI.
    nir = image.select('B5')
    red = image.select('B4')
    ndvi = nir.subtract(red).divide(
        nir.add(red)).rename('ndvi')

    # String expression option for NBR.
    nbr = ee.Image().expression(
       'nbr = (nir-swir2)/(nir+swir2)',
       {
          'nir': image.select('B5'),
          'swir2': image.select('B7')
       }
    )

    # New bands are 1st and 2nd bands and then original spectal bands.
    # Empty image.select ensures that original image properties remain.
    return image.select().addBands([ndvi, nbr]).addBands(image.select('B.*'))

toa_col = toa_col.map(calc_indices)
band_names = toa_col.first().bandNames()
band_names
#applying the toal calculations to bands of all names

toa_max = toa_col.reduce(ee.Reducer.max(band_names.size())).rename(band_names)
display(toa_max)
# Create a maximum-value composite by taking the max NDVI value of each band across all images in the TOA collection
#above comment helped by ChatGPT https://chatgpt.com/share/e/6939f5b4-6040-8000-9303-348e5bac811a
m.add_layer(toa_max, false_color_vis, 'TOA max')

toa_max_basin = toa_max.clip(wawa_basin)
#just get the NDVI values and extent within the wawa basin.
ndvi_vis = {
    'bands': ['ndvi'],
    'min': 0,
    'max': 0.7,
    'palette': cm.get_palette('Greens')
}
m.add_layer(toa_max_basin, ndvi_vis, 'NDVI max basin')

toa_riparian = toa_max_basin.reduceRegion(
    reducer=ee.Reducer.median(),
    geometry=riparian,
    scale=100,
    maxPixels=2e8
)
#gets median NDVI values within previously defined riparian areas

toa_upland = toa_max_basin.reduceRegion(
    reducer=ee.Reducer.median(),
    geometry=upland,
    scale=100,
    maxPixels=2e8
)
#gets median NDVI values within upland areas

display('Median riparian NDVI', toa_riparian.getNumber('ndvi'))
#puts the text with the value next to it on the map
display('Median upland NDVI', toa_upland.getNumber('ndvi'))

toa_max_sample = toa_max_basin.sample(
    region=wawa_basin,
    scale=30,
    numPixels=1000
)

toa_max_sample.limit(10)

import pandas
#needed for histogram
df = ee.data.computeFeatures({
    'expression': toa_max_sample,
    'fileFormat': 'PANDAS_DATAFRAME'
})

df

import altair as alt
#makes chart
alt.Chart(df).mark_bar().encode(
    alt.X("ndvi:Q", bin=True),
    y='count()',
)

alt.Chart(df).mark_point().encode(
    x='B4:Q',
    y='B5:Q',
)
#makes scatterplot