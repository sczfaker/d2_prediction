import speech
import sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
  
while True:
    speech.say("请输入：")
    str = input("请输入：")
    speech.say("你输入的内容是: ")
    speech.say(str)