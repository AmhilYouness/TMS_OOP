from geojson import MultiPoint
import geojson
import numpy as np


class InputFiles():
    def __init__(self,file_personnes,file_uzine,mongo):
        self.file_personnes = file_personnes
        self.file_uzine = file_uzine
        self.mongo = mongo
        self.mongo.delete_all_input()
        self.generate_cord_personnes()
        self.generate_cord_uzine()

    
    def open_geojsonFile(self,file):
        with open(file) as f:
            gj = geojson.load(f)
        return gj
    
    def generate_cord_personnes(self):
        gj = self.open_geojsonFile(self.file_personnes)
        self.mongo.insert_input(gj)
        self.coordinates = [feature['geometry']['coordinates'] for feature in gj['features']]
        self.coordinates = np.array(self.coordinates)
        self.names = [feature['properties']['Name'] for feature in gj['features']]

    def generate_cord_uzine(self):
        gj = self.open_geojsonFile(self.file_uzine)
        self.mongo.insert_input(gj)
        depart_cord = [feature['geometry']['coordinates'] for feature in gj['features']]
        depart_cord = np.array(depart_cord)
        latt_dis=depart_cord[0][0]
        longg_dis=depart_cord[0][1]
        self.cord_uzine=(latt_dis, longg_dis)
        
    








