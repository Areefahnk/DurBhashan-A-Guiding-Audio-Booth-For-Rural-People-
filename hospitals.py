from BotFinal_healthcare import chatbot_resp

disease = 'Fungal infection'
import pandas as pd
data_cat = pd.read_csv('Category.csv')
print(data_cat.columns)
dataf = pd.read_csv('hospitals_display.csv')
#print(dataf)
print(dataf.columns)
predict_category = data_cat.loc[data_cat['Disease'] == disease, 'Doctor_category'].iloc[0]
chatbot_resp(predict_category,"en")

#print(Doctor)
dataf = pd.read_csv('hospitals_display.csv')
#Doctor_Name,Hospital_Name,Hospital_Address,Doctor_category,MobileNo,Timings
i=0
rows=len(dataf.axes[0])
print(rows)
while i<rows:
    dname=dataf.loc[dataf['Doctor_category'] == predict_category,'Doctor_Name'].iloc[i]
    hname=dataf.loc[dataf['Doctor_category'] == predict_category, 'Hospital_Name'].iloc[i]
    hadd=dataf.loc[dataf['Doctor_category'] == predict_category, 'Hospital_Address'].iloc[i]
    dcat=dataf.loc[dataf['Doctor_category'] == predict_category, 'Doctor_category'].iloc[i]
    mn=dataf.loc[dataf['Doctor_category'] == predict_category, 'MobileNo'].iloc[i]
    time=dataf.loc[dataf['Doctor_category'] == predict_category, 'Timings'].iloc[i]
    chatbot_resp("Hospital name "+dname,"hi")
    chatbot_resp("Doctor name "+hname,"hi")
    chatbot_resp("Hospital address "+hadd,"hi")
    chatbot_resp("doctor category "+dcat,"hi")
    chatbot_resp("Mobile "+mn,"hi")
    chatbot_resp("Timings "+time,"hi")
    i+=1


