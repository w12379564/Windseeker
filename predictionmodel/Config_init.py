from predictionmodel.models import Config
import pandas as pd

def init_config_windtower():
    df = pd.read_excel('/home/futuregadget013/donghai_config_windtower.xlsx')
    df.columns = ['ID', 'description', 'unit', 'category', 'frequency']
    for row in df.itertuples():
        ID = int(row.ID)
        name = str(row.description)
        name = name.replace('米','m')
        name = name.replace('风速','_windspeed')
        name = name.replace('温度', '_temp')
        name = name.replace('气压', '_press')
        name = name.replace('湿度', '_hum')
        name = name.replace('风向','_dir')
        name = name.replace('实时值', '_real')
        name = name.replace('最大值', '_max')
        name = name.replace('平均值', '_avg')
        name = name.replace('最小值', '_min')
        name = name.replace('标准差', '_sigma')
        name = name.replace('最大阵风', '_maxWind')
        r = Config(DataID = ID, configname = name)
        r.save()


def init_config_generation():
    df = pd.read_excel('/home/futuregadget013/donghai_config_generations.xlsx')
    df.columns = ['ID', 'description', 'unit', 'category', 'frequency']
    for row in df.itertuples():
        ID = int(row.ID)
        name = str(row.description)
        name = name.replace('风机PLC状态', 'status')
        name = name.replace('风机风速', 'windspeed')
        name = name.replace('风机有功', 'power')
        name = name.replace('风机无功', 'reactive power')
        name = name.replace('风机电网电压1', 'voltage')
        name = name.replace('风机电网电流1', 'current')
        name = name.replace('风机频率', 'frequency')

        name = name.replace('风机状态', 'status')
        name = name.replace('风机瞬时风速', 'windspeed')
        name = name.replace('风机A相电压', 'voltage')
        name = name.replace('风机A相电流', 'current')
        name = name.replace('风机电网频率', 'frequency')
        r = Config(DataID = ID, configname = name)
        r.save()