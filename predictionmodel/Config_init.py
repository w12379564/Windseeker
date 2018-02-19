from predictionmodel.models import Config

def init_config_windspeed():
    name = ['windspeed_real_','windspeed_avg_','windspeed_max_','windspeed_min_','windspeed_sigma_']
    #100m
    idx=10001
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'100m')
        CONFIG.save()
    #90m
    idx=10006
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'90m')
        CONFIG.save()
    #80m
    idx=10011
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'80m')
        CONFIG.save()
    #70m
    idx=10016
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'70m')
        CONFIG.save()
    #50m
    idx=10021
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'50m')
        CONFIG.save()
    #30m
    idx=10026
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'30m')
        CONFIG.save()
    #10m
    idx=10031
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'10m')
        CONFIG.save()


def init_config_winddir():
    name = ['dir_real_', 'dir_avg_', 'dir_max_', 'dir_min_', 'dir_sigma_']
    CONFIG = Config(DataID=10036, configname='null')
    CONFIG.save()
    #100m
    idx=10037
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'100m')
        CONFIG.save()
    #90m
    idx=10042
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'90m')
        CONFIG.save()
    #80m
    idx=10047
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'80m')
        CONFIG.save()
    #10m
    idx=10052
    for i in range(0,5):
        CONFIG = Config(DataID=idx+i,configname=name[i]+'10m')
        CONFIG.save()


def init_config_gendata():
    name = ['windspeed','power','reactivate power','voltage','current','frequency','null','null','null','null']
    for i in range(20001, 20241):
        idx = (i-20001)%10
        no = int((i-20001)/10)+1
        r = Config(DataID = i,configname = name[idx] + "#"+str(no))
        r.save()

def init_config_genstatus():
    name = ['stopping','running','error','waiting','null']
    for i in range(30001,30121):
        idx = (i - 30001) % 5
        no = int((i-30001)/5) + 1
        r = Config(DataID = i,configname = name[idx] + "#"+str(no))
        r.save()

