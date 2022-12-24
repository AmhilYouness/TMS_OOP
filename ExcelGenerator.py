import pandas as pd
import geojson
from geopy.distance import distance as geodist
import math
from datetime import timedelta
import os






class ExcelGenerator():
    def __init__(self,hour_dep,min_dep,clusters,routes,mongo):
        self.hour_dep = hour_dep
        self.min_dep = min_dep
        self.dict_centers = clusters.dict_centers
        self.dict_first_clustring = clusters.dict_first_clustring
        self.dict_c = clusters.dict_c
        self.file_personnes = clusters.inputFiles.file_personnes
        self.cord_uzine = clusters.inputFiles.cord_uzine
        self.df_total = pd.DataFrame(columns=['Name', 'Values','point_rassemblement','cord_rassemeblement'])
        self.routes = routes
        self.mongo = mongo
        pd.set_option('display.max_columns', None)




    def open_geojsonFile(self,file):
        with open(file) as f:
            gj = geojson.load(f)
        return gj
    
    

    
    def generate_cords(self):
        self.dict_timing={}
        self.dict_cordinates={}
        self.list_depart_=[]
        self.df1 = pd.DataFrame()
        df = pd.DataFrame(columns=['ID','Cord','Cord_Point','ID_equipe'])
        for key in self.dict_centers:
            self.dict_cordinates[key]=[]
            self.dict_cordinates[key]=list(self.dict_centers[key][0])
            self.dict_cordinates[key].append(self.cord_uzine)
            c=self.dict_c[key]
            route = self.routes[key]
            duration = route['features'][0]['properties']['summary']['duration']
            nbr_rassmbl=len(route['features'][0]['properties']['segments'])
            self.dict_timing[key]=[]
            for i in range(nbr_rassmbl):
                self.dict_timing[key].append(route['features'][0]['properties']['segments'][i]['duration']/60)
            dict_test = {}
            for j in range(len(self.dict_centers[key][0])):
                dict_test[j] = []
                for i in range(len(c[0])):
                    if(c[0][i]==j):
                        dict_test[j].append(self.dict_first_clustring[key][i])

            mylist = [(key, x) for key,val in dict_test.items() for x in val]
            df2 = pd.DataFrame(mylist, columns=['Name', 'Values']) 
            df2['point_rassemblement']=(df2['Name'].astype(str)+str(key))
            self.df1 = pd.concat([self.df1, df2], ignore_index=True, sort=False)





    def timing(self):
        for ind in self.dict_timing:
            self.dict_timing[ind].insert(0,sum(self.dict_timing[ind]) )

        self.df_prov=pd.DataFrame(columns=['ID_equipe', 'coords','time'])
        for i in self.dict_timing:
            for j in range(1,len(self.dict_timing[i])-1):
                self.dict_timing[i][j]=self.dict_timing[i][j-1]-self.dict_timing[i][j]
        for k, v in self.dict_timing.items():
            v.pop()
        for k, v in self.dict_cordinates.items():
            v.pop()
        for i in self.dict_timing:
            dff=pd.DataFrame(columns=['ID_equipe', 'coords','time'])
            dff['coords']=self.dict_cordinates[i]
            dff['time']=self.dict_timing[i]
            dff['ID_equipe']=i
            self.df_prov=self.df_prov.append(dff)  
        t1 = timedelta(hours=int(self.hour_dep), minutes=int(self.min_dep))
        self.df_prov=self.df_prov.reset_index()
        list_tmp_arr=[]
        for i in range(self.df_prov.shape[0]):
            t2=timedelta(hours=round(self.df_prov['time'][i])//60,minutes=round(self.df_prov['time'][i])%60)
            list_tmp_arr.append(t1-t2)
        self.df_prov["temps d'arrivé"]=list_tmp_arr
        self.df_prov['coords']=self.df_prov['coords'].astype(str)
        self.df_prov['point_rassemblement'] = self.df_prov.apply(lambda row: str(row['index']) + str(row['ID_equipe']), axis=1)





    
    def final_DF(self):
        gj = self.open_geojsonFile(self.file_personnes)
        coordinates = [feature['geometry']['coordinates'] for feature in gj['features']]
        names = [feature['properties']['Correction_'] for feature in gj['features']]
        self.data_add=pd.DataFrame()
        self.data_add['Adresse']=names
        self.data_add['coordonnées ']=coordinates
        self.data_add['cord'] = [','.join(map(str, l)) for l in self.data_add['coordonnées ']]
        self.data_add=self.data_add.drop_duplicates(subset=['cord'])
        self.df1['cord'] = [','.join(map(str, l)) for l in self.df1['Values']]
        self.df1=self.df1.drop_duplicates(subset=['cord'])
        self.data_add=self.data_add.merge(self.df1, on=['cord'])
        self.data_add = self.data_add.merge(self.df_prov , on = ['point_rassemblement'])
        self.data_add["temps d'arrivé"]=self.data_add["temps d'arrivé"].astype(str).str.split(" ", 2, expand=True)[2]
        self.data_add.drop(['cord', 'index' , 'Name' , 'Values' ], axis = 1,inplace = True)
        self.data_add=self.data_add.sort_values(['ID_equipe','point_rassemblement'])
        self.data_add = self.data_add[['Adresse', 'point_rassemblement', "temps d'arrivé", 'time',  'ID_equipe' ]]




    def export(self):
        self.mongo.delete_all_excel()
        self.generate_cords()
        self.timing()
        self.final_DF()
        self.current_directory = os.getcwd()
        self.excel_files = os.path.join(self.current_directory, r'excel_files')
        for i in self.data_add['ID_equipe'].unique():
            self.data_add.loc[self.data_add['ID_equipe'] == i].to_excel(self.excel_files+'/equipe_'+str(i)+'.xslx',index=False)
        result = self.data_add
        self.mongo.insert_excel(result)
        