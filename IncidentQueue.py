from Incident import Incident
from collections import defaultdict
import heapq

class IncidentQueue:
    def __init__(self):
        self.priority_queue = []

        self.location_frequency_counter = defaultdict(list)
        self.most_freq_location = ''
        self.max_location_frequency = 0

    # add the incident to the queue
    def add_incident(self, incident: Incident):
        severity = -incident.get_severity_score()
        time = incident.get_timestamp()  
        item = (severity, time, incident)  

        heapq.heappush(self.priority_queue, incident)

        location = incident.get_location()
        self.location_frequency_counter[location].append(incident)
        # update the most frequent location if necessary
        if len(self.location_frequency_counter[location]) > self.max_location_frequency:
            self.most_freq_location = location
            self.max_location_frequency = len(self.location_frequency_counter[location])

    def get_most_frequent_location(self):
        return self.most_freq_location 

    def get_most_severe(self):
        if not self.priority_queue:
            return None
        return self.priority_queue[0]

    def get_queue_size(self):
        return len(self.priority_queue)

    def get_incidents_at_location(self, location: str)->list:
        if location not in self.location_frequency_counter:
            return None
        
        return self.location_frequency_counter[location]
        