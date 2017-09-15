# -*- coding:utf-8 -*-
import urllib.request as urllib2
import urllib
import re
from datetime import datetime,timedelta
from predictionmodel.models import weathertest

class weatherHis:
    def __init__(self):
        self.headers={'User-Agent' :'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' ,
                      'Referer': 'https://www.wunderground.com',
                      }
        self.title = None


    def getPage(self,datestr):
        try:
            url='https://www.wunderground.com/history/airport/ZSSS/'+datestr+'/DailyHistory.html?req_city=Shanghai&req_statename=China'
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError as e:
            if hasattr(e,"reason"):
                print (u"Connecting failed, ERROR:",e.reason)
                return None

    def getContent(self,page):
        titlePattern = re.compile('<div id="observations_details".*?<tr>(.*?)</tr>', re.S)
        colPattern = re.compile('.*?<th>(.*?)<', re.S)

        titleContent =re.search(titlePattern,page).group(1)
        colNames=re.findall(colPattern,titleContent)
        for i in range(0,len(colNames)):
            colNames[i]=colNames[i].strip()
        #print colNames
        index=[colNames.index('Time'),colNames.index('Temp.'),colNames.index('Humidity'),colNames.index('Pressure'),colNames.index('Wind Dir'),colNames.index('Wind Speed'),colNames.index('Conditions')]
        #print index

        pattern1 = re.compile('<tr class="no-metars">(.*?)</tr>',re.S)
        pattern2 = re.compile('<td.*?>(.*?)</td>', re.S)
        pattern3 = re.compile('<.*?"wx-value">(.*?)</span>', re.S)
        dayData=re.findall(pattern1,page)
        day = []
        #self.file = open(self.title + ".txt", "w+")
        for hourlyData in dayData:
            hour=[]
            items=re.findall(pattern2,hourlyData)
            for item in items:
                #print item
                value=re.search(pattern3,item)
                if value:
                    #print value.group(1)
                    modified_value=re.sub(r'\s',"",value.group(1))
                    hour.append(modified_value)
                    #hour.append(modified_value)
                else:
                    modified_item=re.sub(r'\s',"",item)
                    hour.append(modified_item)
                    #hour.append(modified_item)
            day.append(hour)
        return day,index

    def dataProcess(self,dayData,index):
        dayDataNew=[]
        for hourlyData in dayData:
            if not re.match(r'\d',hourlyData[index[5]]):
                hourlyData[index[5]]="0"
            timeAM = re.search(r'(.*?)AM',hourlyData[index[0]])
            timePM = re.search(r'(.*?)PM', hourlyData[index[0]])
            if timeAM:
                hourlyData[0] = datetime.strptime(self.title + ' ' + re.sub(r'12', "00", timeAM.group(1)),
                                                  '%Y-%m-%d %H:%M')
            if timePM:
                sp=timePM.group().split(':')
                hour=int(sp[0])
                if hour!=12:
                    hour+=12
                hourlyData[0] = datetime.strptime(self.title + ' ' + str(hour) + ':' + sp[1][:-2], '%Y-%m-%d %H:%M')
            hourlyData[index[2]]=re.sub(r'%',"",hourlyData[index[2]])
            #print hourlyData
            dayDataNew.append([hourlyData[i] for i in index])
        return dayDataNew

    def dealwithMissing(self,dayData):

        if dayData == []:return []
        begtime = datetime(dayData[0][0].year,dayData[0][0].month,dayData[0][0].day,0,0)
        endtime = datetime(dayData[0][0].year,dayData[0][0].month,dayData[0][0].day,23,59)
        timeindex = begtime

        l = len(dayData)
        i = 0
        while timeindex<endtime:
            if i >= l:
                toInsert = dayData[l - 1][:]
                toInsert[0] = timeindex
                dayData.append(toInsert)
                timeindex += timedelta(minutes=30)
            else:
                hourlyData = dayData[i]
                if hourlyData[0] == timeindex:
                    timeindex += timedelta(minutes=30)
                    i += 1
                    continue
                else:
                    if i == 0:
                        toInsert = dayData[i + 1][:]
                    else:
                        toInsert = dayData[i - 1][:]
                    toInsert[0] = timeindex
                    dayData.append(toInsert)
                    timeindex += timedelta(minutes=30)

        dayData = sorted(dayData,key=lambda hourly:hourly[0])
        return dayData


    def getDaydata(self,date):
        datestr = date.strftime('%Y/%m/%d')
        self.title = date.strftime('%Y-%m-%d')
        page = self.getPage(datestr)
        (dataRaw, index) = self.getContent(page)
        data = self.dataProcess(dataRaw, index)
        data = self.dealwithMissing(data)
        for record in data:
            newrecord = weathertest(time=record[0],temp=record[1],hum=record[2],press=record[3],dir=record[4],windspeed=record[5],condition=record[6])
            newrecord.save()
