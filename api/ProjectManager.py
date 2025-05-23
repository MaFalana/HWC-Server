import azure.functions as func
import logging
import pymongo

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="HttpExample")
@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")

def HWC_Project(object):
    def __init__(self):
        self.name = ""
        self.jobNumber = ""
        self.acquisitionDate = Date
        self.client = ""

    def createProject(self):
        pass

    def readProject(self, id):
        pass

    def updateProject(self, id):
        pass

    def deleteProject(self, id):
        pass




def HttpExample(req: func.HttpRequest, msg: func.Out [func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        msg.set(name)
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


'''
Name: DB.py
Description: Database connection manager for
'''

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()



class DatabaseManager:
    def __init__(self, db_name):
        user = os.getenv("MONGO_USER")
        pwd = os.getenv("MONGO_PASS")
        host = os.getenv("MONGO_HOST")
        connection = f"mongodb+srv://{user}:{pwd}@{host}/"
        
        self.client = MongoClient(connection)
        self.db = self.client[db_name]
        print(f'Connected to {db_name} database') 
        self.project = self.db['Project'] # Get the Project collection from the database

    def query(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def insert(self, collection_name, document):
        collection = self.db[collection_name]
        collection.insert_one(document)
        #result = collection.insert_one(document)
        #return result.inserted_id

    def __del__(self):
        self.client.close()
        


    def addProject(self, project): # Cretes a new project in the database - CREATE
        if self.exists('Project', project): # Query the database to see if the project already exists
            self.updateProject(project) # If it does, update the project
            print(f"Updated project: {project['title']} from {project['source']}")
        else:
            self.project.insert_one(project)  # If it doesn't, add the project
            print(f"Added project: {project['title']} from {project['source']}")


    def getProject(query): # Gets a project from the database - READ
        project = self.project.query('Project',query)
        print(f"Found project: {project['title']}")
        return project


    def updateProject(self, project): # Updates a project in the database - UPDATE
        # if cover is different or number of chapters is different, update
        self.project.update_one({'id': project['id']}, {'$set': project})
        print(f"Updated project: {project['title']} from {project['source']}")


    def deleteProject(self, project): # Deletes a project from the database - DELETE
        self.project.delete_one({'_id': project['_id']})
        print(f"Deleted project: {project['title']} from {project['source']}")



    def exists(self, collection_name, query): # Checks if a document exists in the database, return boolean
        collection = self.db[collection_name]
        return collection.find_one(query) != None