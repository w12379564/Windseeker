from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.externals import joblib
from datetime import datetime,timedelta
from predictionmodel.dataPreprocess import Db2ShortTermData,Db2FittingData
import numpy as np
from predictionmodel.models import HistoryData
from django.db.models import Sum
from sklearn.preprocessing import PolynomialFeatures

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

def ShortTerm_Train():
    today = datetime.today()
    print(today)
    endtime = datetime(year=today.year,month=today.month,day=today.day,minute=today.minute)
    #endtime = datetime(year=2016,month=6,day=29,hour=15,minute=45)
    endtime = endtime - timedelta(days=1)
    begtime = endtime - timedelta(days=30)
    dataset = Db2ShortTermData(begtime,endtime)
    x_train = np.array(dataset['x_train'])
    y_train = np.array(dataset['y_train'])
    regr = LinearRegression()
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

def ShortTerm_Predict():
    today = datetime.today()
    endtime = datetime(year=today.year, month=today.month, day=today.day, minute=today.minute)
    begtime = endtime - timedelta(hours=4)
    x = HistoryData.objects.filter(time__gte=begtime).filter(time__lt=endtime).values_list('time').annotate(Power_Sum=Sum('power')).values_list('Power_Sum', flat=True)
    x_predict = np.array(list(x))
    x_predict = x_predict.reshape(1,-1)
    #print(x_predict)
    regr = joblib.load('predictionmodel/model/' + 'ShortTerm' + '.model')
    y_predict = regr.predict(x_predict)
    return y_predict

def FittingCurve():
    numbers = [33,34,35,36,37,38]
    fz = PolynomialFeatures(degree=5)
    for number in numbers:
        dataset=Db2FittingData(number)
        x=dataset[:,0]
        y=dataset[:,1]
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
        x_5 = fz.fit_transform(x)
        regr = LinearRegression()
        regr.fit(x_5, y)
        joblib.dump(regr, 'predictionmodel/model/FittingCurve/' + str(number) + '.model')

def CalExpectPower(windspeed):
    ret=[]
    numbers = [33, 34, 35, 36, 37, 38]
    fz = PolynomialFeatures(degree=5)
    wsp = np.array([[windspeed]])
    wsp_5 = fz.fit_transform(wsp)
    for number in numbers:
        regr = joblib.load('predictionmodel/model/FittingCurve/' + str(number) + '.model')
        y_expect = regr.predict(wsp_5)
        if windspeed <= 3:
            ret.append(0)
        elif windspeed >=12:
            ret.append(2000)
        else:
            ret.append(y_expect[0,0])
    print(ret)