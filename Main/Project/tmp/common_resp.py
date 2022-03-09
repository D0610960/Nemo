from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import time, os

charlist = ['活潑', '搞怪', '沉穩', '傲嬌', '溫柔', '欠揍']
folderlist = ['active', 'funny', 'mature', 'tsundere', 'gentle', 'naughty']
def contentToAudio(resp, target, name):
    try:
        start = time.time()
        tts = gTTS(resp, lang='zh-TW', slow=False)
        tts.save("/home/pi/Music/resp.mp3")
        end = time.time()
        print('tts: ', end-start)
        
        start = time.time()
        sound = AudioSegment.from_mp3("/home/pi/Music/resp.mp3")
        targetFile = "/home/pi/Music/common_resp/" + target + "/" + name + ".wav"
        sound.export(targetFile, format="wav")
        end = time.time()
        print('export: ', end-start)
    except Exception as ex:
        print(ex)
 
def combine(char, content, pattern):
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

def playAudio(filename):
    cmd = 'omxplayer -o local /home/pi/Music/common_resp/active/' + filename + '.wav &'
    os.system(cmd)
    
if __name__ == '__main__':
    content = '我沒聽懂你想要我推薦什麼，但我覺得多喝水挺好'
    pattern = 'r'
    name = 'nofood'
    for i in range(6):
        resp = combine(charlist[i], content, pattern)
        contentToAudio(resp, folderlist[i], name)
    
    playAudio(name)