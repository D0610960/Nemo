# In[1]:

import re
import time
import datetime
import numpy as np
import pandas as pd
import random
import json
import urllib.request
import urllib.parse
import requests.packages.urllib3
import os
requests.packages.urllib3.disable_warnings()

cityTable = {
    '宜蘭縣': '003',
    '桃園市': '007',
    '新竹縣': '011',
    '苗栗縣': '015',
    '彰化縣': '019',
    '南投縣': '023',
    '雲林縣': '027',
    '嘉義縣': '031',
    '屏東縣': '035',
    '臺東縣': '039',
    '花蓮縣': '043',
    '澎湖縣': '047',
    '基隆市': '051',
    '新竹市': '055',
    '嘉義市': '059',
    '臺北市': '063',
    '高雄市': '067',
    '新北市': '071',
    '臺中市': '075',
    '臺南市': '079',
    '連江縣': '083',
    '金門縣': '087'
}

wxTable_en = {
    '01': 'Sunny',
    '02': 'Mostly sunny',
    '03': 'Partly sunny',
    '04': 'Partly cloudy',
    '05': 'Mostly cloudy',
    '06': 'Mostly cloudy',
    '07': 'Cloudy',
    '08': 'Cloudy showers',
    '09': 'Cloudy showers',
    '10': 'Overcast showers',
    '11': 'Overcast showers',
    '12': 'Cloudy showers',
    '13': 'Cloudy showers',
    '14': 'Overcast showers',
    '15': 'Showers',
    '16': 'Cloudy showers',
    '17': 'Cloudy showers',
    '18': 'Rainy',
    '19': 'Locally rainy',
    '20': 'Locally rainy',
    '21': 'Locally showers',
    '22': 'Locally showers',
    '23': 'Rainy or snowy',
    '24': 'Sunny with fog',
    '25': 'Sunny with fog',
    '26': 'Cloudy with fog',
    '27': 'Cloudy with fog',
    '28': 'Cloudy with fog',
    '29': 'Locally showers',
    '30': 'Locally showers',
    '31': 'Locally rainy',
    '32': 'Locally rainy',
    '33': 'Thundershowers',
    '34': 'Thundershowers',
    '35': 'Thunderstorms',
    '36': 'Thunderstorms',
    '37': 'Rainy or snowy',
    '38': 'Showers with fog',
    '39': 'Rainy with fog',
    '41': 'Rainy with fog',
    '42': 'Snowy'
}

wxTable_ch = {
    '01': '晴天',
    '02': '晴時多雲',
    '03': '多雲時晴',
    '04': '多雲',
    '05': '多雲時陰',
    '06': '陰時多雲',
    '07': '陰天',
    '08': '多雲短暫陣雨',
    '09': '多雲短暫陣雨',
    '10': '陰短暫陣雨',
    '11': '陰短暫陣雨',
    '12': '多雲陣雨',
    '13': '多雲陣雨',
    '14': '陰陣雨',
    '15': '陣雨',
    '16': '多雲有雨',
    '17': '陰有雨',
    '18': '有雨',
    '19': '晴午後局部降雨',
    '20': '多雲午後局部降雨',
    '21': '晴午後局部陣雨',
    '22': '多雲午後局部陣雨',
    '23': '有雨或雪',
    '24': '晴有霧',
    '25': '晴時多雲有霧',
    '26': '多雲時晴有霧',
    '27': '多雲有霧',
    '28': '陰有霧',
    '29': '多雲局部陣雨',
    '30': '陰局部陣雨',
    '31': '多雲局部降雨',
    '32': '陰局部降雨',
    '33': '雷陣雨',
    '34': '局部雷陣雨',
    '35': '雷雨',
    '36': '局部雷雨',
    '37': '有雨或雪',
    '38': '短暫陣雨有霧',
    '39': '陣雨有霧',
    '41': '有雨有霧',
    '42': '下雪'
}


Breakfast = []
Brunch = []
Lunch = []
Snack = []
Dessert = []
Dinner = []
MidnightSnack = []
Drink = []
Alcohol = []
Soup = []
locSites = []
locNum = []

tmpData = {
    'pop': 'None',
    'wx': 'None',
    'minC': 'None',
    'maxC': 'None',
    'avgC': 'None',
    'uv': 'None',
    'ci': 'None',
    'ws': 'None'
}


# In[2]:


def wxSelect(front, back):
    if front >= back:
        return front
    else:
        return back


def CtoF(degree):
    ans = float(degree) * 9 / 5 + 32
    if ans * 10 % 10 >= 5:
        return format(int(ans) + 1, '.0f')
    else:
        return format(int(ans), '.0f')


def countAvg(maxT, minT):
    ans = (float(maxT) + float(minT)) / 2
    if ans * 10 % 10 >= 5:
        return format(int(ans) + 1, '.0f')
    else:
        return format(int(ans), '.0f')


def aqDesc_en(value):
    if value < 51:
        return 'Good'
    elif value < 101:
        return 'Moderate'
    elif value < 151:
        return 'Poor'
    elif value < 201:
        return 'Unhealthy'
    elif value < 301:
        return 'Terrible'
    else:
        return 'Hazardous'


def aqDesc_ch(value):
    if value < 51:
        return '良好'
    elif value < 101:
        return '普通'
    elif value < 151:
        return '不佳'
    elif value < 201:
        return '不健康'
    elif value < 301:
        return '非常不健康'
    else:
        return '危害'


def ciDescMerge_en(min, max):
    if min == max:
        return min
    else:
        return min + ' to ' + max


def ciDescMerge_ch(min, max):
    if min == max:
        return min
    else:
        return min + '至' + max


def ciDesc_en(value):
    value = int(value)
    if value < 11:
        return 'Freezing'
    elif value < 16:
        return 'Cold'
    elif value < 20:
        return 'Chilly'
    elif value < 22:
        return 'Cool'
    elif value < 25:
        return 'Confort'
    elif value < 26:
        return 'Warm'
    elif value < 31:
        return 'Sultry'
    else:
        return 'Extremely hot'


def ciDesc_ch(value):
    value = int(value)
    if value < 11:
        return '寒冷'
    elif value < 16:
        return '冷'
    elif value < 20:
        return '微涼'
    elif value < 22:
        return '涼爽'
    elif value < 25:
        return '舒適'
    elif value < 26:
        return '溫暖'
    elif value < 31:
        return '悶熱'
    else:
        return '極熱'


def uvDesc_en(value):
    if value != 'X':
        value = int(value)
    else:
        return 'No data'

    if value < 3:
        return 'Low'
    elif value < 6:
        return 'Medium'
    elif value < 8:
        return 'High'
    elif value < 11:
        return 'Very high'
    else:
        return 'Extreme'


def uvDesc_ch(value):
    if value != 'X':
        value = int(value)
    else:
        return '無'

    if value < 3:
        return '微量級'
    elif value < 6:
        return '低量級'
    elif value < 8:
        return '中量級'
    elif value < 11:
        return '過量級'
    else:
        return '危險級'


def popDesc_en(value):
    if value == 'X':
        return 'Unknown'
    else:
        return value


def popDesc_ch(value):
    if value == 'X':
        return '未知'
    else:
        return value


def dataMerge(front, back):
    if front == 'X' and back == 'X':
        return 'X'
    elif front == 'X':
        return back
    elif back == 'X':
        return front
    else:
        a = int(front)
        b = int(back)
        ans = int((a+b) / 2)
        return ans

# In[3]:


# load location and sites list
def loadAQ():
    global locSites
    global locNum
    loc = []
    num = []
    
    # load the file of the station corresponding to each area
    data_csv = pd.read_csv('sites.csv', encoding='utf-8')
    data_csv.shape
    data_csv = data_csv.fillna(0)
    citys = data_csv['縣市']
    dists = data_csv['區']

    for i, j, k, l, m, n, o, p, q in zip(data_csv['代號1'], data_csv['代號2'], data_csv['代號3'], data_csv['代號4'], data_csv['代號5'], data_csv['代號6'], data_csv['代號7'], data_csv['代號8'], data_csv['代號9']):
        locSites.append([int(i), int(j), int(k), int(
            l), int(m), int(n), int(o), int(p), int(q)])

    for i in locSites:
        for j in range(8, 0, -1):
            if i[j] == 0:
                i.pop()
                
    for (i, j) in zip(citys, dists):
        loc.append(i + j)
    for i in range(368):
        num.append(i)

    locNum = dict(zip(loc, num))


loadAQ()


# get air quality from opendata
def getAQ():
    value = []
    site = []

    # data from https://data.epa.gov.tw/
    url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?&api_key=0c76703a-6b3c-4e82-a7e0-ebe86aa7480e'
    req = urllib.request.urlopen(url)
    dataAQ = json.loads(req.read().decode('utf-8'))

    for i in dataAQ['records']:
        value.append(i['AQI'])
        site.append(i['SiteId'])

    return site, value


# calculate the average air quality value of a certain area
def countAvgAQ(loc, aqData):
    global locSites
    global locNum
    value = 0
    siteLen = len(locSites[locNum[loc]])

    for i in range(len(aqData[0])):
        for site in locSites[locNum[loc]]:
            if site == int(aqData[0][i]):
                value += int(aqData[1][i])
                break

    avg = int(value/siteLen)
    return avg


# get local air quality
def airQuality(city, dist, choose):
    loc = city + dist
    aqData = getAQ()
    result = countAvgAQ(loc, aqData)
    if choose:
        return aqDesc_en(result)
    else:
        return aqDesc_ch(result)


# In[4]:


def modifyData(pos):
    global tmpData
    tmpData['pop'] = pos[2]
    tmpData['wx'] = pos[3]
    tmpData['minC'] = pos[4]
    tmpData['maxC'] = pos[5]
    tmpData['avgC'] = pos[6]
    tmpData['uv'] = pos[7]
    tmpData['ci'] = pos[8]
    tmpData['ws'] = pos[9]


# get weather data from opendata
def getWeather(cityName, locName, mode):
    info = ['PoP12h', 'MinCI', 'Wx', 'MaxCI', 'MinT', 'MaxT', 'UVI', 'WS']
    startTime = []
    endTime = []
    PoP12h = []
    MinCI = []
    Wx = []
    MaxCI = []
    MinT_C = []
    MaxT_C = []
    AvgT_C = []
    UVI = []
    CI = []
    WS = []

    Day_Date = []
    Day_Pop = []
    Day_Temp = []
    Day_Uvi = []
    Day_Ws = []
    Day_Wx = []

    # data from https://opendata.cwb.gov.tw/index
    # Authorization :　CWB-C751C800-0151-417D-AB7E-98357FC0CDC6
    if locName != '':
        cityNo = cityTable[cityName]
        district = urllib.parse.quote(locName.encode('utf8'))
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-' + cityNo + \
            '?Authorization=CWB-C751C800-0151-417D-AB7E-98357FC0CDC6&locationName=' + district
    else:
        city = urllib.parse.quote(cityName.encode('utf8'))
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-C751C800-0151-417D-AB7E-98357FC0CDC6&locationName=' + city

    req = urllib.request.urlopen(url)
    dataWeather = eval(req.read())
    # print(dataWeather)

    data_rows = 0
    data_cols = 0
    # put time into data
    for t in dataWeather['records']['locations'][0]['location'][0]['weatherElement'][0]['time']:
        data_rows += 1
        startTime.append(t['startTime'])
        endTime.append(t['endTime'])

    # put weather information into data
    for i in dataWeather['records']['locations'][0]['location'][0]['weatherElement']:
        tag = i['elementName']
        if tag in info:
            data_cols += 1

            if tag == 'Wx':
                index = 1
            else:
                index = 0

            for t in i['time']:
                temp = t['elementValue'][index]['value']
                if temp == ' ':
                    temp = 'X'
                else:
                    pass

                if tag == info[0]:
                    PoP12h.append(temp)
                elif tag == info[1]:
                    MinCI.append(temp)
                elif tag == info[2]:
                    Wx.append(temp)
                elif tag == info[3]:
                    MaxCI.append(temp)
                elif tag == info[4]:
                    MinT_C.append(temp)
                elif tag == info[5]:
                    MaxT_C.append(temp)
                elif tag == info[6]:
                    UVI.append(temp)
                    UVI.append('X')
                elif tag == info[7]:
                    WS.append(temp)
                else:
                    pass
        else:
            pass

    if data_rows % 2 == 1:
        UVI.insert(0, 'X')
    else:
        pass

    # merge data for whole day weather information
    for i in range(data_rows):
        if startTime[i][:10] == startTime[i+1][:10]:
            startTime.append(startTime[i])
            endTime.append(endTime[i+1])
            PoP12h.append(dataMerge(PoP12h[i], PoP12h[i+1]))
            Wx.append(wxSelect(Wx[i], Wx[i+1]))
            MinT_C.append(dataMerge(MinT_C[i], MinT_C[i+1]))
            MaxT_C.append(dataMerge(MaxT_C[i], MaxT_C[i+1]))
            UVI.append(dataMerge(UVI[i], UVI[i+1]))
            MinCI.append(dataMerge(MinCI[i], MinCI[i+1]))
            MaxCI.append(dataMerge(MaxCI[i], MaxCI[i+1]))
            WS.append(dataMerge(WS[i], WS[i+1]))
            i += 1

        elif data_rows % 2 == 1 and (i == data_rows or i == 0):
            startTime.append(startTime[i])
            endTime.append(endTime[i])
            PoP12h.append(PoP12h[i])
            Wx.append(Wx[i])
            MinT_C.append(MinT_C[i])
            MaxT_C.append(MaxT_C[i])
            UVI.append(UVI[i])
            MinCI.append(MinCI[i])
            MaxCI.append(MaxCI[i])
            WS.append(WS[i])

    if mode:
        # data for website
        for i in range(data_rows, len(startTime)):
            Day_Date.append(startTime[i][:10])
            Day_Pop.append(PoP12h[i])
            Day_Uvi.append(uvDesc_en(UVI[i]))
            Day_Ws.append(WS[i])
            Day_Wx.append(Wx[i])
            avgC = countAvg(MinT_C[i], MaxT_C[i])
            tmpC = str(MinT_C[i]) + ',' + str(avgC) + ',' + str(MaxT_C[i])
            Day_Temp.append(tmpC)
            
        return (Day_Date, Day_Pop, Day_Temp, Day_Uvi, Day_Ws, Day_Wx)
    else:
        # calculate average temperature and change weather information to chinese text description
        for i in range(len(startTime)):
            PoP12h[i] = popDesc_ch(PoP12h[i])
            CI.append(ciDescMerge_ch(ciDesc_ch(MinCI[i]), ciDesc_ch(MaxCI[i])))
            Wx[i] = wxTable_ch[Wx[i]]
            AvgT_C.append(countAvg(MinT_C[i], MaxT_C[i]))
            UVI[i] = uvDesc_ch(UVI[i])

        return data_rows, (startTime, endTime, PoP12h, Wx, MinT_C, MaxT_C, AvgT_C, UVI, CI, WS)


# get specified weather information
def weatherInfo(tarCity, tarDist, tarSession, tarDay):
    diff, weatherData = getWeather(tarCity, tarDist, False)
    tarWeatherArr = np.array(weatherData).T
    if tarSession == 0:
        modifyData(tarWeatherArr[0])
    elif tarSession == 1:
        for i in tarWeatherArr[:diff]:
            if (str(tarDay) in i[0]) and ('18:00:00' in i[1]):
                modifyData(i)
                break
    elif tarSession == 2:
        for i in tarWeatherArr[:diff]:
            if (str(tarDay) in i[0]) and ('18:00:00' in i[0]):
                modifyData(i)
                break
    else:
        for i in tarWeatherArr[diff:]:
            if str(tarDay) in i[0]:
                modifyData(i)
                break

    return tmpData


# In[5]:


# translate language selector
def selectLanguage(content):
    if '英文' in content or '英語' in content:
        language = 'en'
    elif '日文' in content or '日語' in content:
        language = 'ja'
    elif '韓文' in content or '韓語' in content:
        language = 'ko'
    elif '中文' in content:
        language = 'zh-tw'
    elif '阿拉伯文' in content or '阿拉伯語' in content:
        language = 'ar'
    elif '荷蘭文' in content or '荷蘭語' in content:
        language = 'nl'
    elif '法文' in content or '法語' in content:
        language = 'fr'
    elif '德文' in content or '德語' in content:
        language = 'de'
    elif '義大利文' in content or '義大利語' in content:
        language = 'it'
    elif '拉丁文' in content or '拉丁語' in content:
        language = 'la'
    elif '葡萄牙文' in content or '葡萄牙語' in content:
        language = 'pt'
    elif '俄文' in content or '俄語' in content:
        language = 'ru'
    elif '西班牙文' in content or '西班牙語' in content:
        language = 'es'
    elif '泰文' in content or '泰語' in content:
        language = 'th'
    elif '越南文' in content or '越南語' in content:
        language = 'vi'
    else:
        language = 'en'
        
    return language


# In[6]:


# load food list
def loadMenu():
    global Breakfast
    global Brunch
    global Lunch
    global Snack
    global Dessert
    global Dinner
    global MidnightSnack
    global Drink
    global Alcohol
    global Soup

    filename = 'food.csv'
    food_csv = pd.read_csv(filename, encoding='utf-8')
    food_csv = food_csv.fillna(0)

    list_Rice = food_csv['飯']
    list_Noodles = food_csv['麵']
    list_Pot = food_csv['鍋類']
    list_Wheat = food_csv['麵食']
    list_Chinese = food_csv['中式']
    list_Korea = food_csv['韓式']
    list_Japan = food_csv['日式']
    list_American = food_csv['美式']
    list_Bread = food_csv['麵包']
    list_Dessert = food_csv['甜點']
    list_Snack = food_csv['點心']
    list_SaltySoup = food_csv['鹹湯']
    list_Alcohol = food_csv['酒精飲料']
    list_Drink = food_csv['飲料']
    list_Others = food_csv['其他']
    list_Breakfast = food_csv['早餐']
    list_MidnightSnack = food_csv['宵夜']

    for i in list_Breakfast:
        if i != 0:
            Breakfast.append(i)
            Brunch.append(i)
    for i in list_Rice:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Noodles:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Pot:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Wheat:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Chinese:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Korea:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Japan:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_American:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Bread:
        if i != 0:
            Breakfast.append(i)
            Brunch.append(i)
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Others:
        if i != 0:
            Lunch.append(i)
            Dinner.append(i)
    for i in list_Dessert:
        if i != 0:
            Dessert.append(i)
    for i in list_Snack:
        if i != 0:
            Snack.append(i)
    for i in list_SaltySoup:
        if i != 0:
            Soup.append(i)
    for i in list_Alcohol:
        if i != 0:
            Alcohol.append(i)
    for i in list_Drink:
        if i != 0:
            Drink.append(i)
    for i in list_MidnightSnack:
        if i != 0:
            MidnightSnack.append(i)


loadMenu()


# get recommend food by specific type
def getRecFood(content):
    global Breakfast
    global Brunch
    global Lunch
    global Snack
    global Dessert
    global Dinner
    global MidnightSnack
    global Drink
    global Alcohol
    global Soup
    
    types = ['早餐', '早午餐', '午餐', '點心', '甜點', '晚餐', '宵夜', '飲料', '湯品', '酒類']
    target = ''
    for foodType in types:
        if foodType in content:
            target = foodType
            print(target)
            break
        else:
            pass

    if target == '早餐':
        return Breakfast[random.randint(0, len(Breakfast))]
    elif target == '早午餐':
        return Brunch[random.randint(0, len(Brunch))]
    elif target == '午餐':
        return Lunch[random.randint(0, len(Lunch))]
    elif target == '點心':
        return Snack[random.randint(0, len(Snack))]
    elif target == '甜點':
        return Dessert[random.randint(0, len(Dessert))]
    elif target == '晚餐':
        return Dinner[random.randint(0, len(Dinner))]
    elif target == '宵夜':
        return MidnightSnack[random.randint(0, len(MidnightSnack))]
    elif target == '飲料':
        return Drink[random.randint(0, len(Drink))]
    elif target == '湯品':
        return Soup[random.randint(0, len(Soup))]
    elif target == '酒類':
        return Alcohol[random.randint(0, len(Alcohol))]
    else:
        return ''

# In[7]:


if __name__ == '__main__':
    index = airQuality('臺中市', '西區', False)
    