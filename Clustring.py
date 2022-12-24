from collections import Counter
from k_means_constrained import KMeansConstrained
from sklearn.cluster import KMeans
from geopy.distance import distance as geodist
from scipy.spatial.distance import pdist, squareform
import math




class Clustring():
    def __init__(self,inputFiles,nbr_places_max,bus_temp,distance_marche_max):
        self.inputFiles = inputFiles
        self.nbr_places_max = nbr_places_max
        self.distance_marche_max = distance_marche_max
        #self.Nbr_bus=round(len(self.inputFiles.coordinates)/int(self.nbr_places_max)+1)+bus_temp
        self.Nbr_bus=math.ceil(len(self.inputFiles.coordinates)/int(self.nbr_places_max)) + bus_temp


    
    def firstClustring(self):
        algo = KMeansConstrained(n_clusters=self.Nbr_bus,size_max=self.nbr_places_max)
        algo.fit(self.inputFiles.coordinates)
        c=algo.predict(self.inputFiles.coordinates)
        most_common,num_most_common = Counter(c).most_common(1)[0]
        self.dict_first_clustring = {}
        for j in range(self.Nbr_bus):
            self.dict_first_clustring[j] = []
            for i in range(len(c)):
                if(c[i]==j):
                    self.dict_first_clustring[j].append(self.inputFiles.coordinates[i])


    
    def secondClustring(self):
        self.dict_centers = {}
        self.dict_c={}
        self.dict_first_clustring_two = {}
        for i in range(len(self.dict_first_clustring)):
            n=0
            dist=2000
            size_group = len(self.dict_first_clustring[i])
            while dist > int(self.distance_marche_max)*2 and n < size_group :
                n=n+1
                kmeans = KMeans(n_clusters=n)
                kmeans.fit(self.dict_first_clustring[i])
                self.dict_centers[i]=[]
                dic_prov = {}
                ml=0
                c=kmeans.predict(self.dict_first_clustring[i])
                for k in range(int(len(kmeans.cluster_centers_))):
                    lsst=[]
                    for p in range(len(c)):
                        if(c[p]==k):
                            lsst.append(self.dict_first_clustring[i][p])
                    if (len(lsst)!=0):
                        dic_prov[ml]=lsst
                        ml=ml+1
                list_distance=[]
                for l in range(len(dic_prov)):
                    if(len(dic_prov[l])>1):
                        dist=pdist(dic_prov[l],lambda u, v: geodist(u, v).meters).max()
                        list_distance.append(dist)

                if(len(list_distance)!=0):
                    dist=max(list_distance)

            self.dict_centers[i]=[]
            self.dict_centers[i].append(kmeans.cluster_centers_)
            self.dict_c[i]=[]
            self.dict_c[i].append(c)
            most_common,num_most_common = Counter(c).most_common(1)[0]
            self.dict_two = {}
            for b in range(n):
                self.dict_two[b] = []
                for a in range(len(c)):
                    if(c[a]==b):
                        self.dict_two[b].append(self.inputFiles.coordinates[a])
            self.dict_first_clustring_two[i] = self.dict_two
        # self.dict_first_clustring_two its dict which generate each group with all points that he has

    

    


            

       
        
           

    



