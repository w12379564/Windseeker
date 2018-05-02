from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.externals import joblib
from datetime import datetime,timedelta
from predictionmodel.dataPreprocess import Db2ShortTermData,Db2FittingData,Db2LongTermData,GetX_Predict_LongTerm,GetX_Predict_LongTerm_Naive,GetX_Predict_ShortTerm,Get_Realtime_WindSpeed
import numpy as np
from predictionmodel.models import HistoryData,PredictionResult_16points,PredictionResult_288points
from django.db.models import Sum
from sklearn.preprocessing import PolynomialFeatures
from predictionmodel.WriteRealtime import WriteDB_16points,WriteDB_288points,WriteDB_288points_Naive,WriteExpect,WriteDB_16points1,WriteDB_288points_Naive1
from predictionmodel.ReadRealtime import GetGenerationStatus,GetRealTimePowerSum,GetRealTimeStatus

numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
           31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,
           58,59,60,61,62]


def train(x_train,y_train):
    ESTIMATORS = {
        "extraTrees": ExtraTreesRegressor(n_estimators=10),
        "knn": KNeighborsRegressor(5,'distance'),
        "linearRegression": LinearRegression(),
        "ridge": RidgeCV(),
    }

    for name, estimator in ESTIMATORS.items():
        regr=estimator.fit(x_train, y_train)
        joblib.dump(regr,'predictionmodel/model/'+name+'.model')

def predict(name,x_test):
    estimator = joblib.load('predictionmodel/model/' + name + '.model')
    return estimator.predict(x_test)

def mixPredict(x_train,y_train,x_test,c1=0.5,c2=0.5):
    estimator1 = KNeighborsRegressor(5, 'distance').fit(x_train,y_train)
    estimator2 = LinearRegression().fit(x_train,y_train)

    return c1*estimator1.predict(x_test)+c2*estimator2.predict(x_test)

def check(y_target,y_predict):
    y_target += 1
    y_predict += 1
    reError=abs(y_target-y_predict)/y_target
    reError_sample=reError.sum(axis=1)/reError.shape[1]
    reError_total=reError_sample.sum(axis=0)/reError_sample.shape[0]
    return reError_sample,reError_total

def ShortTerm_Train(begtime,endtime):
    dataset = Db2ShortTermData(begtime,endtime)
    x_train = np.array(dataset['x_train'])
    y_train = np.array(dataset['y_train'])
    regr = LinearRegression()
    #regr = KNeighborsRegressor(5, 'distance')
    regr.fit(x_train,y_train)
    joblib.dump(regr, 'predictionmodel/model/' + 'ShortTerm' + '.model')

def ShortTerm_Predictts(endtime):
    begtime = endtime - timedelta(hours=4)
    x = HistoryData.objects.filter(time__gte=begtime).filter(time__lt=endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True)
    x_predict = np.array(list(x))
    x_predict = x_predict.reshape(1,-1)
    #print(x_predict)
    regr = joblib.load('predictionmodel/model/' + 'ShortTerm' + '.model')
    y_predict = regr.predict(x_predict)
    return y_predict

def ShortTerm_Predict(nowtime):
    b1 = 1
    e1 = 34
    b2 =35
    e2 = 62

    regr = joblib.load('predictionmodel/model/' + 'ShortTerm' + '.model')
    predict_time = nowtime + timedelta(minutes=15)

    x = GetX_Predict_ShortTerm(nowtime,b1,e1)
    x_predict = np.array(x)
    x_predict = x_predict.reshape(1,-1)
    #print(x_predict)
    y_predict = regr.predict(x_predict)
    #print(y_predict)
    WriteDB_16points(predict_time, y_predict)

    x1 = GetX_Predict_ShortTerm(nowtime,b2,e2)
    x_predict1 = np.array(x1)
    x_predict1 = x_predict1.reshape(1,-1)
    #print(x_predict)
    y_predict1 = regr.predict(x_predict1)
    #print(y_predict)
    WriteDB_16points1(predict_time, y_predict1)


def FittingCurve():
    fz = PolynomialFeatures(degree=5)
    for number in numbers:
        dataset=Db2FittingData(number)
        if len(dataset) == 0: continue
        dataset = np.array(dataset)
        x=dataset[:,0]
        y=dataset[:,1]
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        x_5 = fz.fit_transform(x)
        regr = LinearRegression()
        regr.fit(x_5, y)
        joblib.dump(regr, 'predictionmodel/model/FittingCurve/' + str(number) + '.model')

def CalExpectPower(): #use realtime windspeed
    windspeed=Get_Realtime_WindSpeed()
    ExpectPower=[]
    fz = PolynomialFeatures(degree=5)
    wsp = np.array([[windspeed]])
    wsp_5 = fz.fit_transform(wsp)
    for number in numbers:
        regr = joblib.load('predictionmodel/model/FittingCurve/' + str(number) + '.model')
        y_expect = regr.predict(wsp_5)
        if windspeed <= 3:
            ExpectPower.append(0)
        elif windspeed >=12:
            ExpectPower.append(2000)
        else:
            if y_expect[0,0]>0:
                ExpectPower.append(y_expect[0,0])
            else:
                ExpectPower.append(0)
    #print(ExpectPower)
    ExpectSum = 0
    UsableSum = 0
    Capacity = 0
    RunningStatus = GetRealTimeStatus()
    len1=len(ExpectPower)
    len2=len(RunningStatus)
    len0=min(len1,len2)
    for i in range(len0):
        ExpectSum = ExpectSum + ExpectPower[i]
        if RunningStatus[i] == 1:
            UsableSum = UsableSum + ExpectPower[i]
            Capacity = Capacity + 2000

    LimitSum = ExpectSum - UsableSum
    RealTimePowerSum = GetRealTimePowerSum()
    WriteExpect(RealTimePowerSum,Capacity,ExpectSum, UsableSum, LimitSum)


def LongTerm_Train(begtime,endtime):
    dataset = Db2LongTermData(begtime,endtime)
    x_train = np.array(dataset['x_train'])
    y_train = np.array(dataset['y_train'])
    regr = KNeighborsRegressor(5, 'distance')
    regr.fit(x_train,y_train)
    joblib.dump(regr, 'predictionmodel/model/' + 'LongTerm' + '.model')

def LongTerm_Predict(nowtime):
    x_predict = GetX_Predict_LongTerm(nowtime)
    if len(x_predict)!=4*288:
        return
    x_predict = np.array(x_predict)
    x_predict = x_predict.reshape(1, -1)
    regr = joblib.load('predictionmodel/model/' + 'LongTerm' + '.model')
    y_predict = regr.predict(x_predict)
    predict_time = nowtime + timedelta(minutes=15)
    WriteDB_288points(predict_time, y_predict)


def LongTerm_Predict_Naive(nowtime):
    x_predict = GetX_Predict_LongTerm_Naive(nowtime)
    if len(x_predict)!=288:
        return False
    fz = PolynomialFeatures(degree=5)
    regr={}
    for number in numbers:
        regr[number] = joblib.load('predictionmodel/model/FittingCurve/' + str(number) + '.model')
    y_predict = []
    y_predict1 = []
    for wsp in x_predict:
        wsp_5 = fz.fit_transform(wsp)
        powersum = 0
        powersum1 = 0
        for number in numbers:
            if number < 35:
                powersum = powersum + regr[number].predict(wsp_5)
            else:
                powersum1 = powersum1 + regr[number].predict(wsp_5)
        if powersum < 0:
            powersum = 0
        if powersum1 < 0:
            powersum1 = 0
        y_predict.append(powersum)
        y_predict1.append(powersum1)

    predict_time = nowtime + timedelta(minutes=15)
    WriteDB_288points_Naive(predict_time, y_predict)
    WriteDB_288points_Naive1(predict_time, y_predict1)

