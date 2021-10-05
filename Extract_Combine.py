from Plot_AQI import average_data
import pandas as pd
import requests
import sys
import os
import csv
from bs4 import BeautifulSoup

def met_data(month, year):
    file_html = open('Data/Html_Data/{}/{}.html'.format(year,month), 'rb')
    plain_text = file_html.read()
    temp = []
    final = []
    soup = BeautifulSoup(plain_text,'html.parser')
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                temp.append(a)
    rows = len(temp)/15
    for times in range(round(rows)):
        newtemp = []
        for i in range(15):
            newtemp.append(temp[0])
            temp.pop(0)
        final.append(newtemp)
    length = len(final)
    final.pop(length-1)
    final.pop(0)
    for a in range(len(final)):
        final[a].pop(6)
        final[a].pop(13)
        final[a].pop(12)
        final[a].pop(11)
        final[a].pop(10)
        final[a].pop(9)
        final[a].pop(0)
        final[a].pop(3)
    return final

def data_combine(year, cs):
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist

if __name__ == '__main__':
    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2013, 2019):
        final_data = []
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):
            temp = met_data(month, year)
            final_data = final_data + temp
            
        pm = getattr(sys.modules[__name__], 'average_data')()
        if year == 2013:
            val = pm[0]
        elif year == 2014:
            val = pm[1]
        elif year == 2015:
            val = pm[2]
        elif year == 2016:
            val = pm[3]
        elif year == 2017:
            val = pm[4]
        elif year == 2018:
            val = pm[5]            
        if len(val) == 364:
            val.insert(364, '-')

        for i in range(len(final_data)-1):
            final_data[i].insert(8, val[i])
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)    
                    
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
    data_2017 = data_combine(2017, 600)
    data_2018 = data_combine(2018, 600)  
    
    total=data_2013+data_2014+data_2015+data_2016+data_2017+data_2018
    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv('Data/Real-Data/Real_Combine.csv')
df=df.dropna()
print(df)