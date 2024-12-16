import os
from speech import recognize_from_microphone, convert_response_to_dict
from xgb import xgb_predict
from DatabaseManager import DatabaseManager

# speech_to_text_dict = recognize_from_microphone()

# print("speech to text dict")
# print(speech_to_text_dict)
# print()

#def insert_data_from_txt(description: str):
speech_to_text_dict = recognize_from_microphone()

prediction_dict = {
    'age': [speech_to_text_dict['age']],
    'num_people': [speech_to_text_dict['num_people']],
    'mentioned_medical': [speech_to_text_dict['mentioned_medical']],
    'mentioned_violence': [speech_to_text_dict['mentioned_violence']],
    'mentioned_fire': [speech_to_text_dict['mentioned_fire']],
    'mentioned_vehicular': [speech_to_text_dict['mentioned_vehicular']],
    'mentioned_mental_health': [speech_to_text_dict['mentioned_mental_health']],
    'mentioned_natural_disasters': [speech_to_text_dict['mentioned_natural_disasters']],
    'mentioned_environmental_hazards': [speech_to_text_dict['mentioned_environmental_hazards']],
    'mentioned_suspicious_activity': [speech_to_text_dict['mentioned_suspicious_activity']],
    'mentioned_urgency': [speech_to_text_dict['mentioned_urgency']]
}


# print("dict to be used to get severity score")
# print(prediction_dict)
severity_score = float(xgb_predict.predict_severity(prediction_dict))
# print("severity of incident:", severity_score)
# print()

speech_to_text_dict["severity"] = severity_score

# print("document dict to be inserted into db")
# print(speech_to_text_dict)
# print()


dbm = DatabaseManager()
dbm.insert_incident(speech_to_text_dict)

    # print(result.inserted_id)

# descriptions = []
# backend_dir = os.path.dirname(os.path.abspath(__file__))

# for i in range(9,11):
#     txt_path = os.path.join(backend_dir, 'testcases', f'test{i}.txt')
    
#     with open(txt_path, 'r', encoding='utf-8') as file:
#         case_data = file.read()

#         descriptions.append(case_data)

#     # print(case_data)

# for description in descriptions:
#     insert_data_from_txt(description)