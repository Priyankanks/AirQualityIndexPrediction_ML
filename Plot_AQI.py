import pandas as pd
import matplotlib.pyplot as plt

def average_data():
    temp_i = 0
    average = []
    for year in range(2013,2019):
        avg_list = []
        for rows in pd.read_csv('Data/AQI/aqi{}.csv'.format(year), chunksize=24):
            avg = 0.0
            add_var = 0
            data = []
            df = pd.DataFrame(data = rows)
            for index,row in df.iterrows():
                data.append(row['PM2.5'])
            for i in data:
                if type(i) is float or type(i) is int:
                    add_var = add_var+i
                elif type(i) is str:
                    if i!='NoData' and i!='PwrFail' and i!='- - -' and i!='InVld':
                        temp = float(i)
                        add_var = add_var+temp
            avg = round(add_var/24,2)
            temp_i =  temp_i+1
            average.append(avg)
            avg_list.append(average)
        return avg_list
        
if __name__ == '__main__':
    lst_2013 = average_data()[0]
    lst_2014 = average_data()[1]
    lst_2015 = average_data()[2]
    lst_2016 = average_data()[3]
    lst_2017 = average_data()[4]
    lst_2018 = average_data()[5]