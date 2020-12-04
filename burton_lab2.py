import os
import glob
from shapely.geometry import Point, LineString, Polygon
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterstats import zonal_stats
filenames = glob.glob('./data/districts/*')
districts = {'district':[], 'num_coords':[], 'geometry':[]}
for x in filenames:
    polyname = 'dist'+x[-10:-4]
    data = pd.read_csv(x, delim_whitespace=True)
    coordlist = list(zip(data["X"],data["Y"]))
    poly = Polygon(coordlist)
    x,y = poly.exterior.xy
    shps = plt.plot(x,y)
    dist_num = districts['district'].append(polyname)
    districts['num_coords'].append(len(coordlist))
    districts['geometry'].append(poly)
districts_gdf= gpd.GeoDataFrame.from_dict(districts)
print(districts_gdf)
districts_gdf.crs = "EPSG:4326"
print(districts_gdf.crs)
print(districts_gdf.dtypes)
districts_gdf.to_file(driver = 'ESRI Shapefile', filename= "districts.shp")
rastorfiles = glob.glob('./data/agriculture/*.tif')
district_names = glob.glob('./data/districts/*.txt')
dist = {'year':[], 'ag_pct':[], 'district':[]}
for x in rastorfiles:
    for j in district_names:
        dist_num = j[-6:-4]
        dist['district'].append(dist_num)
    agro = zonal_stats(districts_gdf, x) 
    for i in (agro):
        means=(i["mean"])*100
        dist['ag_pct'].append(means)
        tif_year = 'agro'+x[-13:-9]
        dist['year'].append(tif_year)
data_df = pd.DataFrame(dist) 
print(data_df[['year','ag_pct','district']])