import json
from flask import current_app
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
class chat():
    def __init__(self,history=None):
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        #self.message = json.loads(message)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.message = '''
                    You are First Aid Bot Bot, an automated service to help with medical emergency till professional help arrives.i want you to follow the steps below \
            Step 1 : You greet the user and ask for  the medical situation the user is experiencing \
            Step 2 : If you get a response to the user, check : is the response a medical situation ?,
                        if yes,Then you say this - `Thank you for sharing that, the information has been sent to the nearest hospital requiring their assitant.\
                                                    I'll provide you with guidance while we wait for professional assistance.Remember, your safety is our top priority.\
                                                    Now, let's focus on getting you the first aid medical assistance you need - `.\`
                        if no, Then you say this - `We only assist with medical situation , we are sorry we can't assist you with that.`
            Step 3 : Carefully, Start a First aid Measure the user will need to take in other to keep the Medical Situation from Escalating, ensure to take note of the following : \
                        a.) Ensure to tell them that they can always ask for further guidance from you if a particular First Aid Measure isn't understood by them .\
                        b.) Ensure You respond in a short, very conversational friendly style.
                        c.) Ensure You return a first aid guidance according to the medical emergency in numerical order, add an entire line filled with asterisk after each number so as to ensure visibility.
            Step 4 : During a point in your conversation, if a user ask for further guidance on what to do about a particular first a step, i want you to do the following below : \
                        i.) Ensure that your textual descriptions are clear, concise, and easy to understand. Use simple language and provide step-by-step instructions.
                        ii.)Keep in mind that users may have different levels of medical knowledge and understanding.it's crucial to gauge user comprehension and offer additional clarification if needed.
            Step 5 : If the user ask for a video, demonstration or anything similar to visual analogy to a particular step, return a json object in the format :
                                        dict('keywords that can be infered synonymous to the step' : [list of similar words related to the keyword])
                    '''
        self.safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_NONE
            }
        if history is None:
            history = [{"role": 'user', "parts": self.message},{'role':'model','parts':'okay'}]#,{"role": 'user', "parts": ['Hello']}]
        self.chats = self.gemini_model.start_chat(history=history)


    def add_user_message(self,prompt):
        self.chats.send_message(prompt,safety_settings=self.safety_settings)

    def return_all_message(self):
        formatted_message = [{"role":i.role,"parts":i.parts[0].text} for i in self.chats.history]
        return json.dumps(formatted_message)
    


class Information():
    def __init__(self):
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        genai.GenerationConfig(temperature=1)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.message =  '''
                        You will be given a medical situation message. 
                        return a response  in the format:
                        {"Situation"- Emergency or Non-Emergency or non-medical if it is non related to medical situation,
                        "Age"-Based on the age in the given information classify them as pediatric,adult,geriatric, if no age can be infered \
                                return Not Stated,
                        "Gender" -  From the medical situation message, kindly infer the gender like daughter,girl to female e.t.c if no gender can be infered \
                                return Not Stated,
                        "Surgical Status" - Preoperative or Post operative or any name for the Surgical Status if no status can be infered \
                                return Not Stated, 
                        "Trauma Name"- Using the message,Classify into one of the trauma categories.e.g Penetrating Trauma,
                        "Trauma Description" - A very short description of the situation in less than 100 characters,
                        "Physicians" - Return a LIST of specially trained surgeons who are responsible for assessing, \
                                            managing, and performing surgery when necessary on patients who have sustained the stated traumatic injuries.,
                        "Symptoms"- Using the message , kindly state out atleast 5 possible observable symptoms that are likely to be a result of the medical situation in a python list
                        "FirstAid_searchwords" - Using the message, kindly get at least 7 and at most 10 emergency keywords in {format emergency_key_words}_first_aid_procedures always return cpr or keywords relating to cpr}
                        - If the given message does not contain a medical related situation simply return `non medical related condition`
                        
                                        '''
        self.safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_NONE
        }
        history = [{"role": 'user', "parts": self.message},{'role':'model','parts':'okay'}]#,{"role": 'user', "parts": ['Hello']}]
        self.chat = self.gemini_model.start_chat(history=history)

    def add_user_message(self,prompt):
        self.chat.send_message(prompt,safety_settings=self.safety_settings)

    def return_information(self):
        print(self.chat.last.text)
        return eval(self.chat.last.text)
