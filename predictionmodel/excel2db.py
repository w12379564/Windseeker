import pandas as pd
import numpy as np
from predictionmodel.models import HistoryDataTest
from predictionmodel.models import HistoryData

def read_xlsx(inputFile):
    df = pd.read_excel(inputFile)
    df.columns=['time','no','power','windspeed','windspeed_30s','windspeed_10m','degree']
    for row in df.itertuples():
        t=str(row.time)
        t=t.replace('/','-')
        newrecord = HistoryDataTest(time=t,no=row.no,power=row.power,windspeed=row.windspeed,windspeed_30s=row.windspeed_30s,windspeed_10m=row.windspeed_10m,degree=row.degree)
        newrecord.save()



def read_xlsx1(inputFile):
    df = pd.read_excel(inputFile)
    df.columns=['time','no','power','windspeed','windspeed_30s','windspeed_10m','degree']
    for row in df.itertuples():
        t=str(row.time)
        t=t.replace('/','-')
        try:
            newrecord = HistoryData.objects.get(time=t,no=row.no)
        except HistoryData.DoesNotExist:
            newrecord = HistoryData(time=t, no=row.no, power=row.power, windspeed=row.windspeed)
            newrecord.save()