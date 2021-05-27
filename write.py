import pandas as pd
from BotFinal_healthcare import chatbot_resp
from read import write_excel
data_cat = pd.read_csv('Category.csv')
print(data_cat.columns)
dataf = pd.read_csv('hospitals_display.csv')
# print(dataf)
lang="en"
name1="Kavitha"
age="45"
phone="8456781234"
disease='Fungal infection'
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