from pymongo import MongoClient



class MyMongoDB():
    def __init__(self):
        #client = MongoClient('mongodb+srv://root:root@cluster0.irs5e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['tms']
        print(self.db)

    
    def insert_input(self,file):
        mycollection = self.db['input_files']
        mycollection.insert_one(file)


    def insert_equipes(self,file):
        mycollection = self.db['equipes']
        mycollection.insert_one(file)

    
    def insert_map_equipes(self,file):
        mycollection = self.db['map_equipes']
        mycollection.insert_one(file)

    def insert_excel(self,file):
        mycollection = self.db['excel_files']
        print(file.to_dict('records'))
        mycollection.insert_many(file.to_dict('records'))

    def insert_routes(self,routes):
        mycollection = self.db['routes']
        mycollection.insert_one(routes)



    def delete_all_input(self):
        mycollection = self.db['input_files']
        x = mycollection.delete_many({})

    def delete_all_equipes(self):
        mycollection = self.db['equipes']
        x = mycollection.delete_many({})

    
    def delete_all_map_equipes(self):
        mycollection = self.db['map_equipes']
        x = mycollection.delete_many({})

    def delete_all_excel(self):
        mycollection = self.db['excel_files']
        x = mycollection.delete_many({})





