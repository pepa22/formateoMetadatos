
#from geopandas import GeoDataFrame
from shapely import wkt
import glob
import os
    
import geopandas as gpd


path = '/metadatos/'
archivos = glob.glob(os.path.join(path, '*.csv'))


  

for archivo in archivos:
    #df = pd.read_csv(archivo)
    df= gpd.read_file(archivo, encoding='utf-8')
    # Lee el archivo CSV
    
  # Convierte la columna WKT a geometrías Shapely
    df['geometry'] = df['wkt'].apply(wkt.loads)

    # Crea un GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    #gdf1 = gdf[['id', 'path-row', 'fecha', 'modo', 'submodo', 'polarizacion', 'mirada', 'orbita']]
    if 'wkt' in gdf.columns:
        gdf1 = gdf.drop('wkt', axis =1)
    # Guarda el GeoDataFrame en un archivo shapefile
    shape = archivo[:-4]+'.shp'  
    #print(gdf1.columns)
    gdf1.to_file(shape)
