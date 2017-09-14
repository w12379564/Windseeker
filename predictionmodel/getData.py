# -*- coding:utf-8 -*-
import urllib.request as urllib2
import urllib
import re
from datetime import datetime

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
                hourlyData[0]=self.title+'-'+re.sub(r'12',"00",timeAM.group(1))
            if timePM:
                sp=timePM.group().split(':')
                hour=int(sp[0])
                if hour!=12:
                    hour+=12
                hourlyData[0]=self.title+'-'+str(hour)+':'+sp[1][:-2]
            hourlyData[index[2]]=re.sub(r'%',"",hourlyData[index[2]])
            #print hourlyData
            dayDataNew.append([hourlyData[i] for i in index])
        return dayDataNew

    def getDaydata(self,date):
        datestr = date.strftime('%Y/%m/%d')
        self.title = date.strftime('%Y-%m-%d')
        page = self.getPage(datestr)
        (dataRaw, index) = self.getContent(page)
        data = self.dataProcess(dataRaw, index)
        
