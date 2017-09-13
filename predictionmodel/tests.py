from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Windseeker.settings")
django.setup()

from frontend.models import number
from predictionmodel.dataPreprocess import db2dataset
from predictionmodel.prediction import train,predict,check
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.externals import joblib
# Create your tests here.
size=48
data = db2dataset(size,0)

x=data[:,size:]
y=data[:,:size]

x_train=x[:-101,:]
y_train=y[:-101,:]

x_test=x[-100:,:]
y_target=y[-100:,:]

joblib.dump(x_test,'predictionmodel/data/'+'x_test.data')
joblib.dump(y_target,'predictionmodel/data/'+'y_target.data')

testsize=x_test.shape[0]
figsize=int(sqrt(testsize))+1
ESTIMATORS = ["extraTrees", "knn", "linearRegression","ridge"]
train(x_train,y_train)

for name in ESTIMATORS:
    plt.figure(name)
    y_ = predict(name,x_test)
    reError_sample, reError_total=check(y_target,y_)
    print(name)
    print(reError_sample)
    print(reError_total)
    print(82 * '_')

    for i in range(testsize):
        plt.subplot(figsize, figsize, i+1)
        plt.plot(y_[i, :])
        plt.plot(y_target[i, :])
    plt.show()