# Version that using "LiveChatAsync" class with asyncio, but not working.
import pyttsx3 # pip install pyttsx3
import pytchat # pip install pytchat
import asyncio # 執行序同步執行

# Initialize tts engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150) # set the speed rate of speech (characters per minute)

# get_available_voices() # get all the voices
# english  = voices[1].id #Zira(English, Female)
english  = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
# japanese = voices[2].id #Haruka(Japanese, Female)
japanese = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_JA-JP_HARUKA_11.0'
# chinese  = voices[3].id #Hanhan(Chinese, Female)
chinese  = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ZH-TW_HANHAN_11.0'

language = english # Default language
tts_engine.setProperty('voice', language)

def get_available_voices():
    engine = pyttsx3.init()
    # 獲取所有可用語音
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        # print(f" - Languages: {voice.languages}")
        # print(f" - Gender: {voice.gender}")
        # print(f" - Age: {voice.age}")

def is_english(string):
    for char in string:
        if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
            return False
    return True
def is_chinese(string):
    for word in string:
        if ('\u4e00' <= word <= '\u9fff'):
            return True
    return False
def is_japanese(string):
    for word in string:
        if ('\u3040' <= word <= '\u30ff' or '\u3400' <= word <= '\u4dbf' or '\uf900' <= word <= '\ufaff'):
            return True
    return False

def detect_language(text):
    if   is_english(text) and not language==english:
        tts_engine.setProperty('voice', english)
    elif is_japanese(text) and not language==japanese:
        tts_engine.setProperty('voice', japanese)
    elif is_chinese(text) and not language==chinese:
        tts_engine.setProperty('voice', chinese)

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def enter_vid():
    id_available = False
    while not id_available:
        enter = input('Enter video/live ID or URL: ')
        if 'https://' in enter:
            if 'youtube.com' in enter:
                if 'v=' in enter:
                    video_id = enter.split('v=')[1]
                    id_available = True
                else:
                    print('Invalid YouTube URL: Please enter a live-stream URL.')
            else:
                print('Invalid URL: Please enter a YouTube video URL.')
        elif len(enter) == 11:
            video_id = enter
            id_available = True
        else:
            print('Invalid video ID: Please enter a valid YouTube video ID.')
    return video_id

async def main():
    video_id = enter_vid()
    print(f'Video ID: {video_id}')

    chat_room = pytchat.LiveChatAsync(video_id, callback = func)
    while chat_room.is_alive():
        await asyncio.sleep(3)
        #other background operation.

  # If you want to check the reason for the termination, 
  # you can use `raise_for_status()` function.
    try:
        chat_room.raise_for_status()
    except pytchat.ChatDataFinished:
        print("Chat data finished.")
    except Exception as e:
        print(type(e), str(e))
    chat_room.terminate()
    

#callback function is automatically called periodically.
async def func(chat_data):
    for chat_comment in chat_data.items:
        print(f"{chat_comment.datetime} [{chat_comment.author.name}]: {chat_comment.message}")
        text = f'{chat_comment.author.name}: {chat_comment.message}'
        detect_language(text)
        await speak_text(text)
        await chat_data.tick_async()


if __name__=='__main__':
  try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
  except asyncio.exceptions.CancelledError:
    pass