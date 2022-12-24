import pandas as pd
import geojson
import openrouteservice as ors
from datetime import timedelta



#prepare excel file

df['Personne_cord']=df['Personne_cord'].astype(str)

df['coords'] = df['Personne_cord'].str.strip('\[|\]')\
                                                 .str.split(',', expand=True)

df[['latt','long']]=df['coords'].str.split(" ", 1, expand=True)     

df['latt']=df['latt'].astype(float)
df_pers['latt']=df_pers['latt'].astype(float)


excel_fil = pd.merge(df_pers, df,
                      on=['latt'], how='inner')
excel_fil=excel_fil.sort_values(['ID_equipe','latt'])





#timing
dict_timing={}
dict_cordinates={}
for file_ind in df['ID_equipe'].unique():
    dict_cordinates[file_ind]=[]
    map_eq = map_file+'map_equipe_'+str(file_ind)+'.geojson'
    with open(map_eq) as f:
        gj = geojson.load(f)
    coordinates = gj['coordinates']
    dict_cordinates[file_ind]=coordinates


    

    route = client.directions(
        coordinates=coordinates,
        profile='driving-car',
        format='geojson',
        preference = 'fastest',
        validate=False,
        radiuses=1000,
        optimize_waypoints=False
    )

    
    
    
    dict_timing[file_ind]=[]
    nbr_rassmbl=len(route['features'][0]['properties']['segments'])
    for i in range(nbr_rassmbl):
      dict_timing[file_ind].append(route['features'][0]['properties']['segments'][i]['duration']/60)


    
    #list_tour.append(route['features'][0]['properties']['summary']['duration']/60)
    
 # print('les temps de tournées sont',list_tour)
  #time_calc=max(list_tour)
  #Nbr_bus=Nbr_bus+1
  
    
#  map_UMM 

for ind in dict_timing:
  dict_timing[ind].insert(0,sum(dict_timing[ind]) )

df_prov=pd.DataFrame(columns=['ID_equipe', 'coords','time'])


for i in dict_timing:
  for j in range(1,len(dict_timing[i])-1):
    dict_timing[i][j]=dict_timing[i][j-1]-dict_timing[i][j]
  
for k, v in dict_timing.items():
    v.pop()

for k, v in dict_cordinates.items():
    v.pop()

for i in dict_timing:
  dff=pd.DataFrame(columns=['ID_equipe', 'coords','time'])
  dff['coords']=dict_cordinates[i]
  dff['time']=dict_timing[i]
  dff['ID_equipe']=i
  df_prov=df_prov.append(dff)



t1 = timedelta(hours=int(hour_dep), minutes=int(min_dep))
df_prov=df_prov.reset_index()

list_tmp_arr=[]
for i in range(df_prov.shape[0]):
  t2=timedelta(hours=round(df_prov['time'][i])//60,minutes=round(df_prov['time'][i])%60)
  list_tmp_arr.append(t1-t2)

df_prov['temps d"arrivé']=list_tmp_arr



df_prov['coords']=df_prov['coords'].astype(str)

df_prov[['latt','long']]=df_prov['coords'].str.strip('\[|\]')\
                                              .str.split(',', expand=True)  



excel_fil['Point_rass_cord']=excel_fil['Point_rass_cord'].astype(str)

excel_fil['coords'] = excel_fil['Point_rass_cord'].str.strip('\[|\]')\
                                                 .str.split(',', expand=True)

excel_fil[['latt','long']]=excel_fil['coords'].str.split(" ", 1, expand=True)   


excel_fil['ID_equipe']=excel_fil['ID_equipe'].astype(int)
df_prov['ID_equipe']=df_prov['ID_equipe'].astype(int)

excel_total=pd.merge(excel_fil, df_prov,  how='left', on = ['latt','ID_equipe'])
excel_total=excel_total.sort_values(['ID_equipe','temps d"arrivé'])
excel_total = excel_total.loc[:,~excel_total.columns.duplicated()]

excel_total=excel_total[['Matricule ','Nom Et prénom ','Point  de ramassage ','Point_rass_cord','time','temps d"arrivé','ID_equipe']]
#excel_total.drop(columns=excel_total.columns[excel_total.columns.duplicated()], inplace=True)


excel_total['temps d"arrivé']=excel_total['temps d"arrivé'].astype(str).str.split(" ", 2, expand=True)[2]



#generate excel files 
for i in excel_total['ID_equipe'].unique():
  excel_total.loc[excel_total['ID_equipe'] == i].to_excel(excel_files+'equipe'+str(i)+'.xlsx',index=False)
