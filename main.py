from ExcelGenerator import ExcelGenerator
from InputFiles import InputFiles
from OutputFiles import OutPutFiles
from Clustring import Clustring
from Routing import Routing
from map import Map
from mapAll import MapAll
from mongo import MyMongoDB


file_personnes = 'vrie_cord.geojson'
test = 'test.geojson'
uzinetest = 'uzine2.geojson'
file_uzine = 'usine_cord.geojson'
bus_temp = 0
nbr_places_max = 15
hour_dep = 8
min_dep = 0
time_max = 100
time_round = time_max + 100
distance_marche_max = 600
ORS_key1 = '5b3ce3597851110001cf6248c40727486c3b4440a5338bb9cc551c58'
ORS_key2 = '5b3ce3597851110001cf624873cfc5a6a9e34d7eba09987f00e30062'
preference = 'recommended'
profile = 'driving-car' 
CASAlocation = (33.58762271434954, -7.604319220333975) 
tanger = (35.76269678487231, -5.821119224475683)


mongo = MyMongoDB()

inputFiles = InputFiles(file_personnes,file_uzine,mongo)

while time_round > int(time_max) :
  MyClusters = Clustring(inputFiles,nbr_places_max,bus_temp,distance_marche_max)
  MyClusters.firstClustring()
  MyClusters.secondClustring()
  MyRoutes = Routing(MyClusters , preference , profile ,ORS_key2 )
  time_round = MyRoutes.time_calc
  bus_temp=bus_temp+1




if(time_round!=0):
  print('successfully, besoin de ',len(MyClusters.dict_centers),'bus au total')

for key, value in MyRoutes.routes.items():
  mongo.insert_routes(value)



"""
outPut = OutPutFiles(MyClusters,mongo)
outPut.export_all()





excel = ExcelGenerator(hour_dep,min_dep,MyClusters , MyRoutes.routes, mongo)
excel.export()
"""

"""
map = Map(CASAlocation,MyClusters.dict_centers,MyClusters.inputFiles.cord_uzine,MyRoutes.routes)
map.export_all_maps()



mapAll = MapAll(CASAlocation)
mapAll.showMap()

"""
