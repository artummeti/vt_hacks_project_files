from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
from config import SPEECH_KEY, SPEECH_REGION, GEMINI_API
import google.generativeai as genai
import ast

genai.configure(api_key=GEMINI_API)

def analyze_emergency_call(transcription):
    prompt = f"""
    Analyze the following 911 emergency call transcription and extract key information for first responders, no more than one sentence for emergency_details:
    

    Transcription: {transcription}

    Please fill out the information in the dictionary and output
        {{
        'location': "",
        'name': "",
        'age': 0,
        'emergency_details': "",
        'num_people': 1,
        'mentioned_medical': 0,
        'mentioned_violence': 0,
        'mentioned_fire': 0,
        'mentioned_vehicular': 0,
        'mentioned_mental_health': 0,
        'mentioned_natural_disasters': 0,
        'mentioned_environmental_hazards': 0,
        'mentioned_suspicious_activity': 0,
        'mentioned_urgency': 0
        }}
    
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during call: {e}")
        return "Error occurred with the call."

def convert_response_to_dict(transcription):
    analysis = analyze_emergency_call(transcription)
    print(analysis)
    
    analysis = analysis.strip().strip('`')
    analysis = analysis.strip().strip('python')
    
    dictionary = ast.literal_eval(analysis)
    dictionary["timestamp"] = datetime.now()
    dictionary["transcript"] =  transcription
    dictionary['flagged'] = 0

    if dictionary['location'] == '' or dictionary['name'] == '':
        dictionary['needs_review'] = 1
    else:
        dictionary['needs_review'] =  0
        
    print(dictionary)
    return dictionary

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language="es-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Listening for emergency call...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcription = speech_recognition_result.text
        print("Transcription: ", transcription)
        
        print("\nAnalyzing call...")
        dictionary = convert_response_to_dict(transcription)
        return dictionary
    
    else:
        print(f"Speech recognition failed: {speech_recognition_result.reason}")
        return None

# if __name__ == "__main__":
#     stuff = 'I am John, help. My car exploded and is on fire!'
#     #recognize_from_microphone()
#     abc = convert_response_to_dict(stuff)
#     print(abc)
