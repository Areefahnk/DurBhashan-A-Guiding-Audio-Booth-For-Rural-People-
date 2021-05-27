import datetime
import csv
import warnings
from read import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, _tree

#initializing variables that needed to be stored
id=''
dcat=''
hname=''
dname=''
hadd=''
time=''
mn=''


warnings.filterwarnings("ignore", category=DeprecationWarning)

training = pd.read_csv('Training.csv')
testing= pd.read_csv('Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y


reduced_data = training.groupby(training['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']
testy    = le.transform(testy)


clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
y_pred = clf.predict(x_test)
accuracy = (y_pred == y_test).mean()


print("Score:", accuracy)
print("Accuracy: ",accuracy*100)

model=SVC()
model.fit(x_train,y_train)
print("for svm: ")
print(model.score(x_test,y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols



#################################################
import speech_recognition as sr
import os
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
tr = Translator()


myName = "robo"

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
        os.remove(file1)

def wishme(lang):
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour <= 12:
        chatbot_resp('Good Morning', lang)
    elif hour > 12 and hour < 18:
        chatbot_resp('Good Afternoon', lang)
    else:
        chatbot_resp('Good evening', lang)
    chatbot_resp(f'Iam {myName}, Nice to meet you!', lang)


def user_resp(lang):   #speech to text
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # audio = r.listen(source)
        audio = r.listen(source, None, 8)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language=lang)
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

def userSelectLanguage():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # audio = r.listen(source)
        audio = r.listen(source, None, 10)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in')

            print('You Said:', query)
        except Exception:
            print('Say that again, please')
            return "Say Again", 1
        return query, 0
###########################################


severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()

symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index
def calc_condition(exp,days,lang):
    days=2
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        chatbot_resp("You should take the consultation from doctor. ",lang)
    else:
        chatbot_resp("It might not be that bad but you should take precautions.",lang)

#########################################
def getDescription():
    global description_list
    with open('symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)




def getSeverityDict():
    global severityDictionary
    with open('symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)

###############################################################
def chatbot_respinfo(param, param1):
    pass


def getInfo(lang):
    # name=input("Name:")
    global name1,age,phone
    i=1
    while i==1:
        chatbot_resp("Your Name",lang)
        name,i=user_respinfo("en")
        name1 = name
        print(name)

        chatbot_resp("Hello "+name,"en")
    i=1
    while i==1:
        chatbot_resp("Your Age",lang)
        age,i=user_resp("en")

    i=1
    while i==1:
        chatbot_resp("Phone number",lang)
        phone,i=user_resp("en")
        phone = phone.replace(" ", "")
        print(phone)




def check_pattern(dis_list,inp):
    import re
    pred_list=[]
    ptr=0
    patt = "^" + inp + "$"
    regexp = re.compile(inp)  #if the input symptom there in the string of symptoms in the symptoms list
    for item in dis_list:

        # print(f"comparing {inp} to {item}")
        if regexp.search(item):
            pred_list.append(item)
            # return 1,item
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return ptr,item

def sec_predict(symptoms_exp):
    df = pd.read_csv('Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {}

    for index, symptom in enumerate(X):
        symptoms_dict[symptom] = index

    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1


    return rf_clf.predict([input_vector])

def print_disease(node):
    #print(node)
    node = node[0]
    #print(len(node))
    val  = node.nonzero()
    # print(val)
    disease = le.inverse_transform(val[0])
    return disease
####################################################################
def cityinput():
    import requests
    city = input("Enter your city: ")
    api_key1 = 'ad62ecebb7931902c9fdbfefb78f3277'  # generates latitude and longitude based on city input
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, api_key1)
    res = requests.get(url)  # response object
    data = res.json()
    if data['cod'] == '404':
        print("Invalid City: {}".format(city))
    else:
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        nearbyhospitals(latitude,longitude)

def nearbyhospitals(latitude,longitude):
    import urllib, json
    numberofhospitals = 10
    api_key = 'bx6Xc7UdH96ZiMdcNr85VkI2fOjLADr0'

    # latitude = 17.979097
    # longitude = 79.574362

    json_url = urllib.request.urlopen(
        f'https://api.tomtom.com/search/2/search/hospitals.json?key={api_key}&lat={latitude}&lon={longitude}&limit={numberofhospitals}')
    hospital_data = json.loads(json_url.read())
    for hospital in hospital_data['results']:
        try:
            print(hospital['poi']['name'])
        except:
            print('Name not available')
        try:
            print(hospital['poi']['phone'])
        except:
            print('Phone number not available')
        try:
            print(hospital['address']['freeformAddress'])
        except:
            print('Address not available')
        print()

####################################################################################

def tree_to_code(tree, feature_names,lang):
    tree_ = tree.tree_
    # print(tree_)
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")   #symtoms list
    symptoms_present = []


    # conf_inp=int()
    while True:
        i=1
        while i==1:
            chatbot_resp("Enter the symptom you are experiencing",lang)
            disease_input,i = user_resp(lang)
            #major sym
            if disease_input=='stomach ache':
                disease_input="stomach_pain"
            disease_input=disease_input.replace(" ","_")
            disease_input = disease_input.lower()
        '''for i in disease_input:
            if i==" ":
                i.replace(" ","_")'''
        conf,cnf_dis=check_pattern(chk_dis,disease_input)
        if conf==1:
            chatbot_resp("searches related to input: ",lang) #Stopped here Areefa
            for num,it in enumerate(cnf_dis):
                chatbot_resp(str(num)+")"+it,lang)
            if num!=0:     #if for the 1st symp given by user, we get multiple matches, we ask user to select one what they meant--like fever high/low
                i=1
                while i==1:
                    chatbot_resp(f"Select the one you meant (0 - {num}): Tell number only!  ", lang)
                    conf_inp,i = user_resp(lang)
                    if conf_inp == 'Zero':
                        conf_inp = int(0)
                    elif conf_inp == 'one':
                        conf_inp = int(1)
                    print(conf_inp)
                    conf_inp = int(conf_inp)
            else:
                conf_inp=0

            disease_input=cnf_dis[conf_inp]
            break
            # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
            # conf_inp = input("")
            # if(conf_inp=="yes"):
            #     break
        else:
            print("Enter valid symptom.")

    while True:
        try:
            i=1
            while i==1:
                chatbot_resp("Okay. From how many days ? : ",lang)
                num_days,i = user_resp(lang)   #defect code 2
                #num={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20}
                #num_days =int(num[num_days])
                if "one".swapcase() in num_days or '1' in num_days:
                    num_days = int(1)
                elif "two".swapcase() in num_days or '2' in num_days:
                    num_days = int(2)
                elif "three" in num_days or '3' in num_days:
                    num_days = int(3)
                elif "four" in num_days or '4' in num_days:
                    num_days = int(4)
                elif "five" in num_days or '5' in num_days:
                    num_days = int(5)
                elif "six" in num_days or '6' in num_days:
                    num_days = int(6)
                elif "seven" in num_days or '7' in num_days:
                    num_days = int(7)
                elif "eight" in num_days or '8' in num_days:
                    num_days = int(8)
                elif "nine" in num_days or '9' in num_days:
                    num_days = int(9)
                elif "ten" in num_days or '10' in num_days:
                    num_days = int(10)
                elif "eleven" in num_days or '11' in num_days:
                    num_days = int(11)
                elif "twelve" in num_days or '12' in num_days:
                    num_days = int(12)
                elif "tirtheen" in num_days or '13' in num_days:
                    num_days = int(13)
                elif "fourteen" in num_days or '14' in num_days:
                    num_days = int(14)
                elif "fifteen" in num_days or '15' in num_days:
                    num_days = int(15)
                print(num_days)
            break
        except:
            print("Enter number of days.")
    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            # print( "You may have " +  present_disease )
            red_cols = reduced_data.columns
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            # dis_list=list(symptoms_present)
            # if len(dis_list)!=0:
            #     print("symptoms present  " + str(list(symptoms_present)))
            # print("symptoms given "  +  str(list(symptoms_given)) )
            chatbot_resp("Are you experiencing any ",lang)
            symptoms_exp=[]
            for syms in list(symptoms_given):
                i=1
                while i==1:
                    inp=""
                    chatbot_resp(syms.replace("_"," "),lang)  #defect code 3
                    while True:
                        inp,i=user_resp(lang)
                        if("yes" in inp or "Yes" in inp):
                            inp="yes"
                        elif("no" in inp or "No" in inp):
                            inp="no"
                        print(inp)
                        if(inp.casefold()=="yes" or inp.casefold()=="no" ):
                            break
                        else:
                            chatbot_resp("provide proper answers i.e. (yes/no) : ",lang)
                            i=1
                            break
                if(inp=="yes"):
                    symptoms_exp.append(syms)

            second_prediction=sec_predict(symptoms_exp)
            # print(second_prediction)
            calc_condition(symptoms_exp,num_days,lang)
            if(present_disease[0]==second_prediction[0]):
                chatbot_resp("You may have "+present_disease[0].replace("_"," "),lang)

                chatbot_resp(description_list[present_disease[0]],lang)

                # readn(f"You may have {present_disease[0]}")
                # readn(f"{description_list[present_disease[0]]}")
                disease_pred=present_disease[0]
            else:
                chatbot_resp("You may have "+present_disease[0].replace("_"," ")+"or "+second_prediction[0].replace("_"," "),lang)
                chatbot_resp(description_list[present_disease[0]].replace("_"," "),lang)
                chatbot_resp(description_list[second_prediction[0]].replace("_"," "),lang)

            # print(description_list[present_disease[0]])
            precution_list=precautionDictionary[present_disease[0]]
            chatbot_resp("Take following measures : ",lang)
            for  i,j in enumerate(precution_list):
                #print(i+1,")",j)
                chatbot_resp(str(i)+"step",lang)
                chatbot_resp(j,lang)
            print("Do you want to know the nearby hospitals (say yes/no)")
            hosp = input()

            if hosp.__contains__('yes') or hosp.__contains__('Yes'):
                cityinput()

                disease = present_disease[0]
                print(disease)

                import pandas as pd
                data_cat = pd.read_csv('Category.csv')
                print(data_cat.columns)
                dataf = pd.read_csv('hospitals_display.csv')
                # print(dataf)
                print(dataf.columns)
                print(disease)
                predict_category = data_cat.loc[data_cat['Disease'] == disease, 'Doctor_category'].iloc[0]
                print(predict_category)
                chatbot_resp(predict_category, "en")

                # print(Doctor)
                dataf = pd.read_csv('hospitals_display.csv')
                # Doctor_Name,Hospital_Name,Hospital_Address,Doctor_category,MobileNo,Timings
                try:
                    i = 0
                    rows = len(dataf.axes[0])
                    print(rows)
                    while i < rows:
                        id = dataf.loc[dataf['Doctor_category'] == predict_category, 'ID'].iloc[i]
                        dname = dataf.loc[dataf['Doctor_category'] == predict_category, 'Doctor_Name'].iloc[i]
                        hname = dataf.loc[dataf['Doctor_category'] == predict_category, 'Hospital_Name'].iloc[i]
                        hadd = dataf.loc[dataf['Doctor_category'] == predict_category, 'Hospital_Address'].iloc[i]
                        dcat = dataf.loc[dataf['Doctor_category'] == predict_category, 'Doctor_category'].iloc[i]
                        mn = dataf.loc[dataf['Doctor_category'] == predict_category, 'MobileNo'].iloc[i]
                        time = dataf.loc[dataf['Doctor_category'] == predict_category, 'Timings'].iloc[i]

                        chatbot_resp("Hospital name " + dname, lang)
                        chatbot_resp("Doctor name " + hname, lang)
                        chatbot_resp("Hospital address " + hadd, lang)
                        chatbot_resp("doctor category " + dcat, lang)
                        chatbot_resp("Mobile " + mn, lang)
                        chatbot_resp("Timings " + time, lang)
                        i += 1

                except:
                    print("Take care")
                mn = mn.replace(" ", "")
                print("ANALYSIS DATA OF PATIENT - FINAL")
                print("ID: ",id)
                print("Patient Name: ",name1)
                print("Patient Age: ",age)
                print("Patient phone: ",phone)
                print("Doctor Category to consult: ",dcat)
                print("Hospital Name: ",dname)
                print("Doctor Name: ",hname)
                print("Timings: ",time)
                print("Hospital Phone: ",mn)
                write_excel(id,name1,age,phone,dcat,hname,dname,hadd,time,mn)
                print('Successfully Stored!')
            elif hosp.__contains__('no') or hosp.__contains('No'):
                print("Good Bye! Take care")
            # confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
            # print("confidence level is " + str(confidence_level))
    recurse(0, 1)
'''
lang = 'te'
getSeverityDict()
getDescription()
getprecautionDict()
getInfo(lang)
tree_to_code(clf,cols,lang)
'''
####################################################