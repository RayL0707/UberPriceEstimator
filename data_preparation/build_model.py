from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext

from sklearn import linear_model
import scipy.io
import numpy as np
import pandas as pd
from pandas import DataFrame
import math
import os.path
from os import listdir
import sklearn.externals
from sklearn.externals import joblib
import time

conf = SparkConf().setAppName("cc_project")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

train_data = []
train_labels = []
temp_data = []

store_dir = 'testdir/'
weather_files_prefix = 'weather/'

def parsePickUpTime(col):
    time = col.split()[1]
    first = int(time.split(':')[0])
    return first/3 + 1

def convertTimeStrToInt(time):
    token = time.split(':')
    return token[0]

def getFileName(s):
    token = s.split()
    fileName = token[0]
    time = token[1]
    fileName += '-' + convertTimeStrToInt(time)
    return fileName

def appendAB(a, b):
    if(type(a) is list and type(b) is not list):
        a.append(b)
        return a
    elif(type(b) is list and type(a) is not list):
        b.append(a)
        return b
    elif(type(a) is list and type(b) is list):
        return a + b
    else:
        row = [a]
        row.append(b)
        return row

def getDaysOfMonth(y,m):
    if m == 1 or m == 3 or m == 5 or m == 7 or m ==8 or m == 10 or m == 12:
        return 31
    elif m == 2:
        if y == 2015:
            return 28
        else:
            return 29
    else:
        return 30

def parseNumber(i):
    if(i < 10):
        return '0'+str(i)
    else:
        return str(i)

def getFileNameByYMD(y,m,d):
    return str(y) + '-' + parseNumber(m) + '-' + parseNumber(d)

def getWeatherFilePath(y,m,d):
    return weather_files_prefix + str(y) + '-' + parseNumber(m) + '/' + getFileNameByYMD(y,m,d) + '.csv'

def addColumnsToFile(fileName,row):
    time = row[0].split()[0]
    temp = row[1]
    wind = row[2]
    weather = row[3]

    fileName += '-' + convertTimeStrToInt(time)
   
    if(os.path.exists(store_dir + fileName + '.csv')):            
        pre_df = pd.read_csv(store_dir + fileName + '.csv')
        pre_df['temp'] = temp
        pre_df['wind'] = wind
        pre_df['weather'] = weather
        pre_df.to_csv(path_or_buf=store_dir + fileName + '.csv', index=False)

def joinOrginalDataAndWeatherData():
    taxiDataPrefix = 'taxi_data/'
    y = 2015
    m = 7
    while(True):
        fileName = str(y) + '-' + parseNumber(m) + '.csv'

        taxiFile = sc.textFile(taxiDataPrefix + fileName)
        taxiFileHeader = taxiFile.filter(lambda l: 'tpep_pickup_datetime' in l)
        taxiFileContent = taxiFile.subtract(taxiFileHeader)
        
        taxiFilePPRDD = taxiFileContent.map(lambda line: line.split(','))
        .map(lambda cols: (getFileName(cols[0]),(parsePickUpTime(cols[0]), int(cols[1]), float(cols[2]), float(cols[3]))))
        .reduceByKey(lambda a, b: appendAB(a,b))
        # taxiFilePPRDD.saveAsTextFile("test")
        
        sqlDF = sqlContext.createDataFrame(taxiFilePPRDD, ['fileName','data'])
        dfMatrix = sqlDF.toPandas().as_matrix()

        for i in range(0,dfMatrix.shape[0]):
            row = dfMatrix[i]
            df = DataFrame(row[1], columns=['tpep_pickup_datetime','passenger_count','trip_distance','total_amount'])
            df.to_csv(path_or_buf=store_dir + row[0] + '.csv', index=False)

        m += 1
        if(m == 13):
            y = 2016
            m = 1
        elif(m == 7):
            break

    print 'finished splitting files'

    y = 2015
    m = 7
    while(True):
        for d in range(1,getDaysOfMonth(y,m) + 1):
            path = getWeatherFilePath(y,m,d)
            temp_data = pd.read_csv(path, usecols=['time','temp','wind','weather'])
            matrix_temp_data = temp_data.as_matrix()
            for i in range(0,matrix_temp_data.shape[0]):
                row = matrix_temp_data[i]
                addColumnsToFile(getFileNameByYMD(y,m,d),row)
        m += 1
        if(m == 13):
            y = 2016
            m = 1
        elif(m == 7):
            break

def saveModel():
    train_data_df = pd.DataFrame()
    train_lable_df = pd.DataFrame()
    train_data_df_list = []
    train_lable_df_list = []
    
    for f in os.listdir('newTestDir/'):
        if(f != '.DS_Store'):
            try:
                df = pd.read_csv(store_dir+f,usecols=['tpep_pickup_datetime','passenger_count','trip_distance','total_amount'],header=0) 
                train_data_df_list.append(df[['tpep_pickup_datetime','passenger_count','trip_distance']])
                train_lable_df_list.append(df[['total_amount']])
            except:
                pass
    print 'finished importing data to DataFrame'
    
    train_data_df = pd.concat(train_data_df_list)
    train_lable_df = pd.concat(train_lable_df_list)
    print 'finished concatinating'
    
    train_data = train_data_df.as_matrix()
    train_labels = train_lable_df.values.flatten()
    print 'finished converting to matrix'

    clf = linear_model.LinearRegression()
    model = clf.fit(train_data, train_labels) 
    print 'finished training'
    
    joblib.dump(model, 'model.pkl') 
    print 'finished dumping'

def main():
    joinOrginalDataAndWeatherData()
    saveModel()   

if __name__ == '__main__':
    main()