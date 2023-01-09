import datetime
from BMI_writeXcel import write_excel
import speech_recognition as sr
import os
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import numpy as np
tr = Translator()
lang="en"
def translation_user(text, src_lang, dest_lang):
    translatedText = tr.translate(text, src=src_lang, dest=dest_lang)
    print(translatedText.text)
    translatedSpeech = gTTS(translatedText.text, lang=dest_lang)
    file1 = "svo_output.mp3"
    translatedSpeech.save(file1)
    playsound(file1)
    os.remove(file1)
    return translatedText.text

def translation(text, lang):
    translatedText = tr.translate(text, dest=lang)
    print(translatedText.text)
    translatedSpeech = gTTS(translatedText.text, lang=lang)
    file1 = "svo_output.mp3"
    translatedSpeech.save(file1)
    playsound("svo_output.mp3")
    # os.remove(file1)
    # file1 = str("hello" + str(i) + ".mp3")
    #   tts.save(file1)
    # playsound.playsound(file1, True)
    print('after')
    os.remove(file1)


def chatbot_resp(text1, lang):
    # text to speech conversion
    if lang!="en":
        translation(text1, lang);
    else:
        translatedText = tr.translate(text1, dest=lang)
        print(translatedText.text)
        translatedSpeech = gTTS(text1, lang=lang)
        file1 = "svo_output.mp3"
        translatedSpeech.save(file1)
        playsound("svo_output.mp3")
        print('after')
        os.remove(file1)

def user_resp(lang):   #speech to text
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # audio = r.listen(source)
        audio = r.listen(source, None, 8)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language=lang)
            #chatbot_resp("So your main symptom is "+query,lang)
            if lang!="en":
                query = translation_user(query, lang, "en")
            print('You Said:', query)
        except Exception:
            chatbot_resp('Say that again, please',lang)
            return "Say Again", 1
        return query, 0

def user_respinfo(lang):   #speech to text
    lang="en"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # audio = r.listen(source)
        audio = r.listen(source, None, 8)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio)
            #chatbot_resp("So your main symptom is "+query,lang)
            print('You Said:', query)
        except Exception:
            chatbot_resp('Say that again, please',lang)
            return "Say Again", 1
        return query, 0

def getInfo1(lang):
    # name=input("Name:")
    global name2,age2,ht,wt,bmi,status
    i=1
    while i==1:
        chatbot_resp("Name",lang)
        name,i=user_respinfo("en")
        name2 = name
        print(name2)

        chatbot_resp("Hello "+name2,"en")
    i=1
    while i==1:
        chatbot_resp("Age",lang)
        age2,i=user_resp("en")

    i=1
    while i==1:
        chatbot_resp("height (in feet)",lang)
        ht,i=user_resp("en")
        print(ht)
    i = 1
    while i == 1:
        chatbot_resp("weight (in kg)", lang)
        wt, i = user_resp("en")
        print(wt)

    height=float(ht)
    height=height*0.3048
    weight=float(wt)
    bmi = weight / (height ** 2)

    # conditions
    if (bmi < 16):
        status = "severely underweight"
        chatbot_resp("severely underweight",lang)

    elif (bmi >= 16 and bmi < 18.5):
        status = "underweight"
        chatbot_resp("underweight",lang)

    elif (bmi >= 18.5 and bmi < 25):
        status = "healthy"
        chatbot_resp("Healthy",lang)

    elif (bmi >= 25 and bmi < 30):
        status = "overweight"
        chatbot_resp("overweight",lang)

    elif (bmi >= 30):
        status="severely overweight"
        chatbot_resp("severely overweight",lang)


if __name__ == "__main__":

    getInfo1("en")
    anganwaadi="Anganwaadi Parkala"
    write_excel(anganwaadi,name2,age2,wt,ht,bmi,status)
