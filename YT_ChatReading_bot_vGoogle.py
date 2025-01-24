from gtts import gTTS # pip install gTTS
import pytchat        # pip install pytchat
from io import BytesIO
import pygame
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize tts engine
english  = 'en'
japanese = 'ja'
chinese  = 'zh-TW'
language = chinese # Default language

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
    global language
    if   is_english(text) and not language==english:
        language = english
    elif is_japanese(text) and not language==japanese:
        language = japanese
    elif is_chinese(text) and not language==chinese:
        language = chinese

def wait():
    while pygame.mixer.get_busy():
        time.sleep(1)
def speak_text(text, language=language):
    # speaks without saving the audio file
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fo)
    mp3_fo.seek(0)
    sound = pygame.mixer.Sound(mp3_fo)
    sound.play()
    wait()

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
                print(f"{chat_comment.datetime} [{chat_comment.author.name}]: {chat_comment.message}")
                # text = f'{chat_comment.author.name}說: {chat_comment.message}'
                detect_language(chat_comment.author.name)
                speak_text(chat_comment.author.name, language)
                detect_language(says_word)
                speak_text(says_word, language)
                detect_language(chat_comment.message)
                speak_text(chat_comment.message, language)

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