import pyttsx3 # pip install pyttsx3
import pytchat # pip install pytchat
import time

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

language = chinese # Default language
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
        if not (' ' <= char <= '~'):
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
        return english
    elif is_japanese(text) and not language==japanese:
        return japanese
    elif is_chinese(text) and not language==chinese:
        return chinese
    else:
        return language
def set_language(engine, language):
    engine.setProperty('voice', language)

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def play_speech(tts_engine, text, language):
    set_language(tts_engine, language)
    speak_text(tts_engine, text)

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

def main():
    global language
    video_id = enter_vid()
    print(f'Video ID: {video_id}')
    
    if   language == chinese:
        says_word = '說: '
    elif language == japanese:
        says_word = 'が: '
    else: 
        says_word = 'says: '

    try:
        chat_room = pytchat.create(video_id=video_id)
        while chat_room.is_alive():
            for chat_comment in chat_room.get().sync_items():
                print(f"{chat_comment.datetime} [{chat_comment.author.name}]說: {chat_comment.message}")

                detected_lang = detect_language(chat_comment.author.name)
                if detected_lang != language:
                    language = detected_lang
                    set_language(tts_engine, language)
                speak_text(chat_comment.author.name)

                detected_lang = detect_language(says_word)
                if detected_lang != language:
                    language = detected_lang
                    set_language(tts_engine, language)
                speak_text(says_word)

                detected_lang = detect_language(chat_comment.message)
                if detected_lang != language:
                    language = detected_lang
                    set_language(tts_engine, language)
                speak_text(chat_comment.message)

        chat_room.terminate()
        print("Chat connection ended.")

    except pytchat.exceptions.InvalidVideoIdException:
        print("Invalid video ID: ID dose not exist.")
        video_id = enter_vid()
    except KeyboardInterrupt:
        chat_room.terminate()
        print('Program has been shutdown by user.')
    # except Exception as error:
    #         print(f"Error: {error}")

if __name__ == "__main__":
    main()