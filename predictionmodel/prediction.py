from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.externals import joblib

def train(x_train,y_train):
    ESTIMATORS = {
        "extraTrees": ExtraTreesRegressor(n_estimators=10),
        "knn": KNeighborsRegressor(5,'distance'),
        "linearRegression": LinearRegression(),
        "ridge": RidgeCV(),
    }

    for name, estimator in ESTIMATORS.items():
        regr=estimator.fit(x_train, y_train)
        joblib.dump(regr,'model/'+name+'.model')

def predict(name,x_test):
    estimator = joblib.load('model/' + name + '.model')
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


