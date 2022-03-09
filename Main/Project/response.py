# In[1]:


import function as func
import information as info
import database as db
import random
import datetime
import time
import re

mark = ''


# In[2]:


# combine characteristic response sentences
def combine(content, pattern):
    # pattern f q r
    char = db.getChar()
    if pattern.find('f') != -1:
        if char == '活潑':
            content = '好滴,' + content
        elif char == '搞怪':
            content = '好喔,' + content
        elif char == '沉穩':
            content = '/' + content
        elif char == '傲嬌':
            content = '恨/,' + content
        elif char == '溫柔':
            content = '豪/,' + content
        elif char == '欠揍':
            content = '好哇,' + content
    if pattern.find('q') != -1:
        if char == '活潑':
            content += '鴨'
        elif char == '搞怪':
            content += '捏'
        elif char == '沉穩':
            content += '/'
        elif char == '傲嬌':
            content += '軋'
        elif char == '溫柔':
            content += 'ㄋ'
        elif char == '欠揍':
            content += '/'
    elif pattern.find('r') != -1:
        if char == '活潑':
            content += '優'
        elif char == '搞怪':
            content += '撸'
        elif char == '沉穩':
            content += '/'
        elif char == '傲嬌':
            content += 'ho'
        elif char == '溫柔':
            content += '/'
        elif char == '欠揍':
            content += '呵'
    return content


# In[2]:


# irregular greetings
def greeting():
    greetContent = ''
    char = db.getChar()
    if char == '活潑':
        greetContent = random.choice(['陪我玩啦,陪我玩啦', '和我聊天嘛', '想吃糖捏', '別忙了,休息一下嘛', '勇於迎接新挑戰',
                                 '說說話嘛,好不好', '活力滿滿 精神滿滿', '鬆口氣啦', '不向困境低頭', '人生充滿了美好'])
    elif char == '搞怪':
        greetContent = random.choice(['森七七,理我一下啦', '舉頭望明月,低頭滑手機', '心情怪美麗的', '討厭啦,人家害羞',
                                 '哼哼哼,哼哼哼', '唉呦喂,一把老骨的走不動啦', '來個碰碰', '旋轉跳躍,我閉著眼',
                                 '喔喔喔喔,你是我的花朵', '你是我的小阿小蘋果'])
    elif char == '沉穩':
        greetContent = random.choice(['有事需要我幫忙嗎', '累了嗎,休息一下吧', '家事永遠的避風港', '今日事,今日畢',
                                 '陪我聊天吧', '不要都不理我吧', '笑一個吧', '我也是有脾氣的', '說話吧', '要不要放鬆呢'])
    elif char == '傲嬌':
        greetContent = random.choice(['不喜歡就別理我', '不要迷戀我,我知道自己很好看', '我才不承認喜歡你',
                                 '哼,我才不說喜歡你', '到底是要讓我等多久', '厚又,我才不要再看到你', '人家我可是天生麗質的',
                                 '不要對我不理不才的悠', '再不理我 本寶寶可是會生氣的'])
    elif char == '溫柔':
        greetContent = random.choice(['想你了', '早點回來,不要讓我擔心', '早點休息,熬夜對身體不好', '累了嗎,要不要休息一下',
                                 '我愛你', '來陪陪我', '親愛的', '怎麼拉,要不要放鬆呢', '想聽你的聲音', '想要和你說話'])
    elif char == '欠揍':
        greetContent = random.choice(['有膽出去嗨', '老子就是睡不著', '怎樣啦', '是要不要理我', '就是無聊啦',
                                 '還不來看看我', '我都等到累了', '到底,怎麼那麼不爽啦', '看你看的不耐煩了', '來追我啊,追不到'])
    return greetContent


# get response content: warning
def warn(h, t, g):
    warnContent = ''
    if h is not None and t is not None:
        warnContent = '注意，現在室內'
        if t > 45:
            warnContent += '溫度過高，請立刻檢查住家狀況'
        else:
            if h > 80:
                warnContent += '太潮濕了'
            elif h < 40:
                warnContent += '太乾燥了'
            else:
                warnContent = ''
    if g is not None:
        if g == 'WARNING':
            warnContent += '/注意，現在室內危險氣體含量過高'
        elif g == 'DANGER':
            warnContent += '/警告，現在室內危險氣體含量超標'
        else:
            pass

    if warnContent != '':
        warnContent = combine(warnContent, 'r')
        return warnContent


# In[3]:


# get response content
def getResp(content, part):
    global mark
    resp = ''
    
    # True: first conversation
    if part:
        if content != '':
            if (content == '沒事'):
                return True, 'nothing'
            # indoor sensor
            elif ('室內' in content) or ('房間' in content):
                h, t = db.getHT()
                if ('溫度' in content):
                    tempMode = db.getTempMode()
                    if tempMode == 'C':
                        unit = '攝氏'
                        tempInner = t
                    else:
                        unit = '華氏'
                        tempInner = info.CtoF(t)
                    resp = '現在室內溫度是{}{}度'.format(unit, tempInner)
                elif ('濕度' in content):
                    if h == 'None':
                        resp = '感測器壞掉'
                    else:
                        resp = '現在室內濕度是{}%'.format(h)
            # current time and date
            elif ('時間' in content):
                hour = int('{}'.format(time.strftime('%H')))
                if hour == 12:
                    resp = '現在是{} 中午{}'.format(time.strftime(
                        '%Y年%m月%d號'), time.strftime('%H點%M分'))
                elif hour > 12:
                    hour = hour - 12
                    resp = '現在是{} 下午{}點{}'.format(time.strftime(
                        '%Y年%m月%d號'), hour, time.strftime('%M分'))
                else:
                    resp = '現在是{} 上午{}'.format(time.strftime(
                        '%Y年%m月%d號'), time.strftime('%H點%M分'))
            elif ('幾點' in content) or ('幾分' in content):
                hour = int('{}'.format(time.strftime('%H')))
                if hour == 12:
                    resp = '現在時間是中午{}'.format(time.strftime('%H點%M分'))
                elif hour > 12:
                    hour = hour - 12
                    resp = '現在時間是下午{}點{}'.format(hour, time.strftime('%M分'))
                else:
                    resp = '現在時間是上午{}'.format(time.strftime('%H點%M分'))
            elif ('幾號' in content):
                resp = '今天是{}'.format(time.strftime('%Y年%m月%d號'))
            elif ('星期幾' in content):
                week = '{}'.format(time.strftime('%a'))
                if week == 'Mon':
                    week = '一'
                elif week == 'Tue':
                    week = '二'
                elif week == 'Wed':
                    week = '三'
                elif week == 'Thu':
                    week = '四'
                elif week == 'Fri':
                    week = '五'
                elif week == 'Sat':
                    week = '六'
                else:
                    week = '日'
                resp = '今天是星期{}'.format(week)
            # set alarm and memo
            elif ('設定鬧鐘' in content):
                alarmNum = db.checkAlarm()
                if alarmNum < 20:
                    mark = 'setAlarm'
                    return True, 'set_alarm'
                else:
                    return True, 'toomuch_alarm'
            elif ('刪除鬧鐘' in content):
                alarmNum = db.checkAlarm()
                mark = 'deleteAlarm'
                resp = '目前總共有' + str(alarmNum) + '個鬧鐘，你要刪除哪一個'
                resp = combine(resp, 'fq')
                return False, resp
            elif ('提醒我' in content):
                memoNum = db.checkNote()
                if memoNum < 20:
                    mark = 'setMemo,' + content[3:]
                    return True, 'set_memo'
                else:
                    return True, 'toomuch_memo'
            elif ('刪除備忘' in content):
                memoNum = db.checkNote()
                mark = 'deleteMemo'
                resp = '目前總共有' + str(memoNum) + '個備忘錄，你要刪除哪一個'
                resp = combine(resp, 'fq')
                return False, resp
            # translate a word
            elif ('翻譯' in content) and ('文' in content or '語' in content):
                language = info.selectLanguage(content)
                mark = 'trans,' + language
                return True, 'translate'
            # listen musicFlag
            elif ('要聽' in content) or ('想聽' in content):
                mark = 'music'
                return True, 'ready_music'
            elif ('關閉音樂' in content) or ('關掉音樂' in content):
                mark = 'closeBrowser'
                return True, 'close_music'
            # recommend food
            elif ('推薦' in content):
                food = info.getRecFood(content)
                if food != '':
                    resp = food + '，你覺得怎麼樣'
                    resp = combine(resp, 'q')
                    return False, resp
                else:
                    return True, 'nofood'
            # air quality
            elif ('空氣品質' in content):
                city, dist = db.getLocation()
                index = info.airQuality(city, dist, False)
                if index == '不佳':
                    note = '敏感族群可考慮減少外出活動或配戴口罩'
                elif index == '不健康':
                    note = '外出活動時戴上口罩保護自己'
                elif (index == '非常不健康') or (index == '危害'):
                    note = '適度關閉門窗，別暴露在不良空氣中'
                else:
                    note = ''
                resp = '今天{}{}的空氣品質為{}，{}'.format(city, dist, index, note)
            # weather information
            else:
                keyword = ['天氣', '冷', '熱', '降雨機率',
                        '下雨', '傘', '溫度', '氣溫', '紫外線', '風速']
                for word in keyword:
                    if word in content:
                        resp = weatherResp(content, word)
                        break
                    else:
                        pass
    # False: second conversation
    else:
        if content != '':
            if 'trans' in mark:
                resp = content
                return False, resp
            else:
                # end the conversation
                if (content == '取消'):
                    return True, 'cancel'
                # datetime of alarm or memo
                elif ('點' in content):
                    result = func.datetimeProc(content)
                    target = 'set_failed'
                    if result:
                        if mark == 'setAlarm':
                            target = db.addAlarm(result)
                        elif 'setMemo' in mark:
                            text = mark.split(',')[1]
                            target = db.addMemo(result, text)
                    return True, target
                # delete alarm or memo
                elif ('第' in content) and ('個' in content):
                    result = func.numberProc(content)
                    target = 'delete_failed'
                    if result:
                        if mark == 'deleteAlarm':
                            target = db.deleteByNo('ALARM', result)
                        elif mark == 'deleteMemo':
                            target = db.deleteByNo('MEMO', result)
                    return True, target
                # wrong keyword
                else:
                    return True, 'donot_realize'
        else:
            return True, 'donot_hear'
    
    if resp != '':
        resp = combine(resp, 'r')
        return False, resp
    else:
        return True, 'donot_understand' 


# get response content : weather information
def weatherResp(content, cat):
    session = ['早上', '上午', '中午', '下午', '白天', '傍晚', '晚上', '半夜', '凌晨', '清晨']

    try:
        tmpData = ''
        resp_day = ''
        resp_session = ''
        resp_loc = ''
        resp = ''

        # get weather data by correct location if needed
        # otherwise by default location
        tarCity = ''
        tarDist = ''

        if '宜蘭市' in content:
            tarCity = '宜蘭縣'
            tarDist = '宜蘭市'
        elif '苗栗市' in content:
            tarCity = '苗栗縣'
            tarDist = '苗栗市'
        elif '彰化市' in content:
            tarCity = '彰化縣'
            tarDist = '彰化市'
        elif '南投市' in content:
            tarCity = '南投縣'
            tarDist = '南投市'
        elif ('台東市' in content) or ('臺東市' in content):
            tarCity = '臺東縣'
            tarDist = '臺東市'
        elif '花蓮市' in content:
            tarCity = '花蓮縣'
            tarDist = '花蓮市'
        elif '屏東市' in content:
            tarCity = '屏東縣'
            tarDist = '屏東市'
        elif '竹北市' in content:
            tarCity = '新竹縣'
            tarDist = '竹北市'
        elif '頭份市' in content:
            tarCity = '苗栗縣'
            tarDist = '頭份市'
        elif '員林市' in content:
            tarCity = '彰化縣'
            tarDist = '員林市'
        elif '斗六市' in content:
            tarCity = '雲林縣'
            tarDist = '斗六市'
        elif '太保市' in content:
            tarCity = '嘉義縣'
            tarDist = '太保市'
        elif '朴子市' in content:
            tarCity = '嘉義縣'
            tarDist = '朴子市'
        elif '馬公市' in content:
            tarCity = '澎湖縣'
            tarDist = '馬公市'
        elif '市' in content:
            s = content.partition('市')
            tarCity = s[0] + s[1]
        elif '縣' in content:
            s = content.partition('縣')
            tarCity = s[0] + s[1]

        if tarDist == '':
            content = content[content.find(tarCity)+len(tarCity):]
            if '鄉' in content:
                s = content.partition('鄉')
                tarDist = s[0] + s[1]
            elif '鎮' in content:
                s = content.partition('鎮')
                tarDist = s[0] + s[1]
            elif '區' in content:
                s = content.partition('區')
                tarDist = s[0] + s[1]

        if (tarCity == '') and (tarDist == ''):
            city, dist = db.getLocation()
            tarCity = city
            tarDist = dist
            resp_loc = '本地'
        elif (tarCity == '') and (tarDist != ''):
            tarCity = city
            resp_loc = tarDist
        else:
            resp_loc = tarCity + tarDist

        tarCity = tarCity.replace('台', '臺')
        tarDist = tarDist.replace('台', '臺')
        print(tarCity, tarDist)

        # modify weather data by correct time
        if '現在' in content:
            tmpData = info.weatherInfo(tarCity, tarDist, 0, tarDay)
            resp_session = '現在'
        else:
            today = datetime.date.today()
            if '今天' in content:
                tarDay = today
                resp_day = '今天'
            elif '明天' in content:
                tarDay = today + datetime.timedelta(days=1)
                resp_day = '明天'
            elif '後天' in content:
                tarDay = today + datetime.timedelta(days=2)
                resp_day = '後天'
            else:
                tarDay = today

            for s in session:
                if content.find(s) != -1:
                    resp_session = content.partition(s)[1]
                    break
                else:
                    continue

            if resp_session in session[:5]:
                tmpData = info.weatherInfo(tarCity, tarDist, 1, tarDay)
            elif resp_session in session[5:]:
                tmpData = info.weatherInfo(tarCity, tarDist, 2, tarDay)
            else:
                tmpData = info.weatherInfo(tarCity, tarDist, 3, tarDay)
        
        # get specific response
        if tmpData != '':
            tempMode = db.getTempMode()
            if (resp_day == '') and (resp_session == ''):
                resp_session = '目前'
            else:
                pass
        
            if cat == '天氣':
                if tempMode == 'C':
                    unit = '攝氏'
                    tempMax = tmpData['maxC']
                    tempMin = tmpData['minC']
                else:
                    unit = '華氏'
                    tempMax = CtoF(tmpData['maxC'])
                    tempMin = CtoF(tmpData['minC'])

                resp = '{}{}{}{}，{}，最高溫度來到{}{}度，最低溫{}度，降雨機率有{}%'.format(
                    resp_loc, resp_day, resp_session, tmpData['wx'], tmpData['ci'], unit, tempMax, tempMin, tmpData['pop'])
            elif (cat == '冷') or (cat == '熱'):
                resp = '{}{}{}是{}的'.format(
                    resp_loc, resp_day, resp_session, tmpData['ci'])
            elif (cat == '降雨機率') or (cat == '下雨') or (cat == '傘'):
                if int(tmpData['pop']) >= 70:
                    note = '別忘了帶傘'
                elif int(tmpData['pop']) >= 50:
                    note = '帶把傘以防萬一'
                elif int(tmpData['pop']) >= 10:
                    note = '我也不確定會不會下雨'
                else:
                    note = '應該不會下雨'
                resp = '{}{}{}的降雨機率為{}%，{}'.format(
                    resp_loc, resp_day, resp_session, tmpData['pop'], note)
            elif (cat == '溫度') or (cat == '氣溫'):
                if tempMode == 'C':
                    unit = '攝氏'
                    tempMax = tmpData['maxC']
                    tempMin = tmpData['minC']
                    tempAvg = tmpData['avgC']
                else:
                    unit = '華氏'
                    tempMax = CtoF(tmpData['maxC'])
                    tempMin = CtoF(tmpData['minC'])
                    tempAvg = CtoF(tmpData['avgC'])

                if '最高' in content:
                    resp = '{}{}{}的最高溫度為{}{}度'.format(
                        resp_loc, resp_day, resp_session, unit, tempMax)
                elif '最低' in content:
                    resp = '{}{}{}的最低溫度為{}{}度'.format(
                        resp_loc, resp_day, resp_session, unit, tempMin)
                elif '平均' in content:
                    resp = '{}{}{}的平均溫度為{}{}度'.format(
                        resp_loc, resp_day, resp_session, unit, tempAvg)
                else:
                    resp = '{}{}{}的溫度為{}{}度至{}度，平均溫度{}度'.format(
                        resp_loc, resp_day, resp_session, unit, tempMin, tempMax, tempAvg)
            elif cat == '紫外線':
                if tmpData['uv'] == '無':
                    return '找不到資料'
                elif (tmpData['uv'] == '低量級') or (tmpData['uv'] == '微量級'):
                    note = '不容易曬成小黑人'
                else:
                    note = '注意做好防曬'
                resp = '{}{}{}的紫外線指數為{}，{}'.format(
                    resp_loc, resp_day, resp_session, tmpData['uv'], note)
            elif cat == '風速':
                if int(tmpData['ws']) >= 18:
                    note = '外面風有一點大，小心安全'
                elif int(tmpData['ws']) >= 11:
                    note = '外頭強風，沒事別出門'
                else:
                    note = ''
                resp = '{}{}{}的最大風速為{}公尺每秒，{}'.format(
                    resp_loc, resp_day, resp_session, tmpData['ws'], note)
        else:
            resp = '很抱歉，我找不到這個時段的天氣資訊'
        return resp

    except:
        return '很抱歉，我不明白你想找哪個地區的天氣資訊'


if __name__ == '__main__':
    content = '推薦晚餐'
    result = info.getRecFood(content)
    print(result)
