# -*- coding: utf-8 -*-
__author__ = 'JosefinaOtero'

from bs4 import BeautifulSoup
import csv
import re
import json
import glob
import os

# abro el archivo html de los metadatos del mosaico de saocom
#archivo = 'LA_RIOJA_map.html'
path = '/saocom_mosaico/metadatos/'
archivos = glob.glob(os.path.join(path, '*.html'))
print(archivos)
for archivo in archivos:
    prov = archivo.split('\\')[-1]
    with open(archivo, 'r', encoding='utf-8') as file:
        html_content = file.read()

        # se parsea como formato html , se saca la informqacion del script 
        #y se identifica la data a obtener de los metadatos
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script')

        info = str(scripts[5])
        #print(info)
        J1 = info.split('"geometry"')

        print("cantidad de huellas del mosaico: ", len(J1))

        #data en el objeto qe guarda la infroamcion importante
        metadatos = [] 
        for l in J1[2:] :
            la = str(l)
            #saco la informacion de las coordenadas 
            coordenadas= re.search(r'({.*})', la)
            dic_coordenadas = coordenadas.group(1)

            dic_= json.loads(dic_coordenadas[:-49])
            lista_de_valores = list(dic_.values())
            lista_de_valores0 = str(lista_de_valores)
            lista_de_valores1 = lista_de_valores0.replace(",", "")
            lista_de_valores2 = lista_de_valores1.replace("] [", ", ")
            lista_de_valores3 = lista_de_valores2.replace("[[[[", "POLYGON ((")
            lista_de_valores4 = lista_de_valores3.replace("]]] ", "))")
            lista_de_valores5 = lista_de_valores4.replace("'Polygon']", "")
            #print(lista_de_valores5)
        # print(la)
            soup = BeautifulSoup(l, 'html.parser')

            # Extract information from the table
            data = []
            data2 = ('wkt', lista_de_valores5)
            table_tag = soup.find('table')
            data = []
            data.append(data2)
            if table_tag:
                    table_rows = table_tag.find_all('tr')
                    
                    for row in table_rows:
                        th = row.find('th')
                        td = row.find('td')
                        if th and td:
                            data.append((th.text, td.text))
            
            metadatos.append(data)

        #print(metadatos)
        
        csv_file_path = path + 'metadatos_mosaicoSAOCOM_'+ prov[:-9]+'_2023.csv'
       # print(prov[:-9])    
       # Write to CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file )

            # Write header
            csv_writer.writerow(['wkt','id', 'path-row', 'fecha', 'modo', 'submodo', 'polarizacion', 'mirada', 'orbita'])
            for row in metadatos:
                csv_writer.writerow([value for key, value in row])
                
