from datetime import datetime

class Incident:
    def __init__(self, incident_id: str, user_name: str, incident_info: str, severity_score: float, location: str, timestamp: datetime, transcribed_call: str):
        self.incident_id = incident_id
        self.user_name = user_name
        self.incident_info = incident_info
        self.severity_score = severity_score
        self.location = location
        self.timestamp = timestamp
        self.transcribed_call = transcribed_call


    # incident = {
    # "Location": string of location: string,
    # "Age": age of caller: int,
    # "emergency_details": what is the emergency: string,
    # "num_people": number of people in incident: int,
    # 1 if the incident is described by this word, 0 if not
    # "medical": 1 or 0,
    # "violence": 1 or 0,
    # "fire_and_hazards": 1 or 0,
    # "vehicular": 1 or 0,
    # "mental_health": 1 or 0,
    # "natural_disasters": 1 or 0,
    # "environmental_hazards": 1 or 0,
    # "suspicious_activity": 1 or 0,
    # "urgency": 1 or 0,
    # "timestamp": datetime function,
    # "severity": score to show how important incident is: float
    # }

    def get_severity_score(self) -> float:
        return self.severity_score

    def get_location(self) -> str:
        return self.location

    def get_timestamp(self):
        return self.timestamp

    def get_transcript(self):
        return self.transcribed_call

    def __str__(self) -> str:
        return f"Incident(ID: {self.incident_id}, Title: {self.incident_info}, Severity: {self.severity_score}, Location: {self.location}, Time: {self.timestamp})\nTranscribed call: {self.transcribed_call}"

    def __lt__(self, other):
        if self.severity_score != other.severity_score:
            return self.severity_score > other.severity_score

        return self.timestamp < other.timestamp
    
    # def compare_by_time_then_severity(self, other):
    #     if self.timestamp != other.timestamp:
    #         return self.timestamp < other.timestamp
    #     return self.severity_score > other.severity_score
    
