import win32com
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
i=0
for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say('The quick brown fox jumped over the lazy dog.')
    engine.say('说中国话。我们唱歌、跳舞、做游戏！')
    print (i)
    i+=1
engine.runAndWait()