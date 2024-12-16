import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv 
from datetime import datetime
from Incident import Incident
from bson.objectid import ObjectId
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise Exception("MONGO_URI not found in environment variables")
        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['Incidents']
        self.collection = self.db['IncidentReports']

    def serialize(self, data):
        # Convert ObjectId and datetime to JSON-compatible formats
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                elif isinstance(value, datetime):
                    data[key] = value.isoformat()
        return data

    def fetch_random_user(self):
        try:
            # Fetch a single random document from the collection
            user = self.collection.find_one({"name": "Daniel"})
            if user:
                return self.serialize(user)
            return None
        except Exception as e:
            raise Exception(f"Error fetching random user: {e}")

    def insert_incident(self,incident_data: dict):
        self.collection.insert_one(incident_data)

        # incident_id = result.inserted_id

        # return new_incident
    
    def get_incident_by_id(self, incident_id: str)->dict:
        incident_document = self.collection.find_one("_id", ObjectId(incident_id))

        incident_document = self.serialize(incident_document)

        return incident_document
    
    def get_incidents_by_feature(self, feature: str) -> list:
        query = {feature: 1}
        relevant_incidents = self.collection.find(query)

        relevant_incidents = list(relevant_incidents)

        incident_list = []

        for incident in relevant_incidents:

            new_incident = self.serialize(incident)

            incident_list.append(new_incident)
        
            
        return incident_list
    
    def clear_database(self):
        self.collection.delete_many({})
        # print(f"Deleted {result.deleted_count} documents from the collection.")
    
    def get_ordered_by_severity(self) -> list:
        incidents = self.collection.find()
        
        # Define severity order and scores
        # severity_info = {
        #     'critical': {'order': 0, 'score': 100, 'highlight': True},
        #     'high': {'order': 1, 'score': 75, 'highlight': True},
        #     'medium': {'order': 2, 'score': 50, 'highlight': False},
        #     'low': {'order': 3, 'score': 25, 'highlight': False}
        # }
        
        incident_list = []
        for incident in incidents:
            new_incident = self.serialize(incident)
            severity = incident['severity']
            dt: datetime = incident['timestamp']
            # info = severity_info.get(severity, {'order': 4, 'score': 0, 'highlight': False})
            
            # Add score and highlight information to the incident
            # new_incident['severity_score'] = info['score']
            # new_incident['highlight'] = info['highlight']
            
            incident_list.append((severity,dt, new_incident))
        
        # Sort by severity order (ascending) and then by timestamp (descending) if severities are equal
        incident_list.sort(key=lambda x: (-x[0], x[1]))
        
        # Extract just the incident data, discarding the order value used for sorting
        result = [incident for _,_, incident in incident_list]
        
        return result
    
    def resolve_incident(self, incident_id: str):
        self.collection.update_one(
            {"_id": ObjectId(incident_id)},
            {
                "$set": {
                    "flagged": 1,
                    "needs_review": 0
                }
            }
        )

    def is_empty(self) -> bool:
        return self.collection.count_documents({}) == 0    

    def get_ordered_by_time(self)->list:
        incidents = self.collection.find()

        incident_list = []

        for incident in incidents:
            # new_incident = Incident(
            # incident_id = incident.get("_id"),
            # user_name= incident['name'],
            # incident_info = incident['emergency_details'],
            # severity_score=incident['severity'],
            # location = incident['location'],
            # timestamp = incident['timestamp'],
            # transcribed_call = incident['transcript']
            # )

            new_incident = self.serialize(incident)

            dt: datetime = incident['timestamp']

            incident_list.append((dt, new_incident))

        incident_list.sort()

        result = [incident for _, incident in incident_list]

        return result
    
    # def update_collection(self):
    #     result = self.collection.update_many(
    #             {},  # This empty filter matches all documents
    #             {"$set": {"flagged": 0}},  # Set 'flagged' to 0 for all documents
    #             upsert=False  # Don't create new documents if they don't exist
    #         )

        
            

# db = DatabaseManager()
# db.update_collection()

#db.clear_database()




    

